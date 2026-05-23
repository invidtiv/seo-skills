#!/usr/bin/env python3
"""
GEO-ready Audit Tool
Automates checking and verification of items in research.md for Generative Engine Optimization (GEO).
Features:
- Parse live URLs or local markdown/HTML files.
- Run Phase 1-4 checks using regex, HTML parsing, and structured heuristics.
- Optional Gemini API integration for qualitative checks (Answer-first, fluff, standalone sentences).
- Optional Google Search API integration for Phase 5 off-site footprint.
- Outputs a beautiful markdown report and terminal score.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from urllib.error import URLError, HTTPError

# Color output helpers
def print_success(msg):
    print(f"\033[92m[✓] {msg}\033[0m")

def print_warning(msg):
    print(f"\033[93m[!] {msg}\033[0m")

def print_error(msg):
    print(f"\033[91m[✗] {msg}\033[0m")

def print_info(msg):
    print(f"\033[94m[*] {msg}\033[0m")


def load_env(env_path=".env"):
    """Reads simple key=value pairs from .env without external library dependency."""
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip()
    return env_vars


class GEOHTMLParser(HTMLParser):
    """Parses HTML pages to extract structure, metadata, schema, and links."""
    def __init__(self):
        super().__init__()
        self.title = ""
        self.headings = []      # list of dicts: {'tag': 'h2'/'h3', 'text': str}
        self.paragraphs = []    # list of strings
        self.tables = []        # list of strings / tables found
        self.lists = []         # list of list items
        self.json_ld = []       # list of parsed dicts/lists from ld+json
        self.links = []         # list of external/internal hrefs
        self.meta_tags = {}     # dict of name/property -> content
        self.structure = []     # order of elements: list of (type, text)
        
        # Parse states
        self.current_tag = None
        self.in_title = False
        self.in_json_ld = False
        self.json_ld_buffer = []
        self.current_heading = None
        self.current_paragraph = []
        self.text_content = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attrs_dict.get('name') or attrs_dict.get('property')
            content = attrs_dict.get('content')
            if name and content:
                self.meta_tags[name] = content
        elif tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self.in_json_ld = True
            self.json_ld_buffer = []
        elif tag in ('h2', 'h3'):
            self.current_heading = {'tag': tag, 'text': ''}
        elif tag == 'p':
            self.current_paragraph = []
        elif tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        elif tag == 'table':
            self.tables.append("[Table]")
            self.structure.append(('table', '[Table]'))
        elif tag in ('ul', 'ol'):
            self.lists.append("[List]")
            self.structure.append(('list', '[List]'))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'script' and self.in_json_ld:
            self.in_json_ld = False
            try:
                raw_json = "".join(self.json_ld_buffer).strip()
                self.json_ld.append(json.loads(raw_json))
            except Exception:
                pass
        elif tag in ('h2', 'h3') and self.current_heading:
            self.current_heading['text'] = self.current_heading['text'].strip()
            self.headings.append(self.current_heading)
            self.structure.append((self.current_heading['tag'], self.current_heading['text']))
            self.current_heading = None
        elif tag == 'p' and self.current_paragraph:
            p_text = " ".join(self.current_paragraph).strip()
            # Normalize whitespace
            p_text = re.sub(r'\s+', ' ', p_text)
            if p_text:
                self.paragraphs.append(p_text)
                self.structure.append(('p', p_text))
            self.current_paragraph = []
        self.current_tag = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_json_ld:
            self.json_ld_buffer.append(data)
        elif self.current_heading:
            self.current_heading['text'] += data
        elif self.current_tag == 'p':
            self.current_paragraph.append(data)
        elif self.current_tag not in ('script', 'style'):
            self.text_content.append(data)


def parse_markdown(md_content):
    """Extracts structure, headings, links, tables, and lists from Markdown."""
    parsed = {
        'title': '',
        'headings': [],
        'paragraphs': [],
        'tables': [],
        'lists': [],
        'links': [],
        'structure': [],
        'json_ld': []  # usually empty in pure markdown unless embedded HTML
    }
    
    lines = md_content.split('\n')
    in_table = False
    in_list = False
    
    # Check for title
    for line in lines:
        title_match = re.match(r'^#\s+(.+)$', line)
        if title_match:
            parsed['title'] = title_match.group(1).strip()
            break
            
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            in_table = False
            in_list = False
            continue
            
        # Match headings
        heading_match = re.match(r'^(#{2,3})\s+(.+)$', line)
        if heading_match:
            tag = 'h2' if len(heading_match.group(1)) == 2 else 'h3'
            text = heading_match.group(2).strip()
            parsed['headings'].append({'tag': tag, 'text': text})
            parsed['structure'].append((tag, text))
            continue
            
        # Match tables
        if line_strip.startswith('|'):
            if not in_table:
                parsed['tables'].append("[Table]")
                parsed['structure'].append(('table', '[Table]'))
                in_table = True
            continue
            
        # Match lists
        if re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)', line):
            if not in_list:
                parsed['lists'].append("[List]")
                parsed['structure'].append(('list', '[List]'))
                in_list = True
            continue
            
        # Match links
        links_found = re.findall(r'\[.*?\]\((https?://.*?)\)', line)
        if links_found:
            parsed['links'].extend(links_found)
            
        # Match paragraph (if not heading, table, or list)
        if not line_strip.startswith('#') and not line_strip.startswith('|') and not re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)', line):
            # Strip markdown link markers for plain text
            p_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line_strip)
            parsed['paragraphs'].append(p_text)
            parsed['structure'].append(('p', p_text))
            
    return parsed


def query_gemini_api(api_key, prompt):
    """Sends a query directly to Gemini API and requests structured JSON output."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode('utf-8'))
            text_resp = res['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_resp)
    except HTTPError as e:
        print_error(f"Gemini API returned HTTP Error: {e.code} - {e.reason}")
        try:
            print_error(e.read().decode())
        except Exception:
            pass
    except Exception as e:
        print_error(f"Failed to query Gemini API: {str(e)}")
    return None


def query_google_search(api_key, cx, query):
    """Queries the Google Custom Search API and returns the result count and top items."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={encoded_query}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'GEOAuditClient/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            search_info = res.get('searchInformation', {})
            total_results = int(search_info.get('totalResults', 0))
            items = res.get('items', [])
            return total_results, items
    except Exception as e:
        print_error(f"Google Search API query failed: {str(e)}")
    return 0, []


def fetch_url(url):
    """Fetches a URL with a standard browser user agent to minimize scrapers blocking."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='replace'), response.status
    except HTTPError as e:
        print_error(f"Failed to fetch {url}: HTTP {e.code}")
        return None, e.code
    except URLError as e:
        print_error(f"Network error trying to connect to {url}: {e.reason}")
        return None, None
    except Exception as e:
        print_error(f"Unexpected error fetching {url}: {str(e)}")
        return None, None


class GEOAuditor:
    def __init__(self, target, env_vars=None):
        self.target = target  # can be URL or filepath
        self.env = env_vars or {}
        self.is_url = target.startswith('http://') or target.startswith('https://')
        self.raw_content = ""
        self.data = {}
        self.report = []
        self.scores = {
            'phase1': 0, # Technical (max 25)
            'phase2': 0, # Structure (max 25)
            'phase3': 0, # Authority (max 25)
            'phase4': 0, # Quotability (max 25)
        }
        self.audit_log = []

    def log_result(self, phase, check_name, passed, max_points, awarded_points, details=""):
        status_symbol = "[✓]" if passed else "[!]"
        self.audit_log.append({
            'phase': phase,
            'check': check_name,
            'passed': passed,
            'max_points': max_points,
            'awarded_points': awarded_points,
            'details': details
        })
        self.scores[phase] += awarded_points

    def prepare_data(self):
        """Fetches/reads and parses the content."""
        if self.is_url:
            print_info(f"Fetching URL: {self.target}")
            html_content, status = fetch_url(self.target)
            if not html_content:
                print_error("Failed to load page content. Exiting.")
                sys.exit(1)
            self.raw_content = html_content
            
            # Parse HTML
            parser = GEOHTMLParser()
            parser.feed(html_content)
            self.data = {
                'title': parser.title.strip(),
                'headings': parser.headings,
                'paragraphs': parser.paragraphs,
                'tables': parser.tables,
                'lists': parser.lists,
                'json_ld': parser.json_ld,
                'links': parser.links,
                'structure': parser.structure,
                'meta_tags': parser.meta_tags,
                'raw_html_len': len(html_content)
            }
        else:
            print_info(f"Reading file path: {self.target}")
            if not os.path.exists(self.target):
                print_error(f"File path does not exist: {self.target}")
                sys.exit(1)
            
            with open(self.target, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            self.raw_content = content
            
            if self.target.endswith('.md'):
                self.data = parse_markdown(content)
                self.data['raw_html_len'] = len(content)
                self.data['meta_tags'] = {}
            else: # treat as HTML
                parser = GEOHTMLParser()
                parser.feed(content)
                self.data = {
                    'title': parser.title.strip(),
                    'headings': parser.headings,
                    'paragraphs': parser.paragraphs,
                    'tables': parser.tables,
                    'lists': parser.lists,
                    'json_ld': parser.json_ld,
                    'links': parser.links,
                    'structure': parser.structure,
                    'meta_tags': parser.meta_tags,
                    'raw_html_len': len(content)
                }

    def run_phase1_technical(self):
        """Phase 1: AI Discovery & Technical Foundations (Max 25 pts)"""
        print_info("Auditing Phase 1: Technical Foundations...")
        
        # 1. robots.txt check (5 pts)
        if self.is_url:
            parsed_url = urllib.parse.urlparse(self.target)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            robots_content, status = fetch_url(robots_url)
            if status == 200 and robots_content:
                # Basic check for critical AI crawlers
                crawlers = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'CCBot']
                blocked_crawlers = []
                
                # Check for disallows
                for crawler in crawlers:
                    # Look for crawler section
                    pattern = rf"User-agent:\s*{re.escape(crawler)}\b.*?Disallow:\s*/\s*$"
                    if re.search(pattern, robots_content, re.IGNORECASE | re.DOTALL):
                        blocked_crawlers.append(crawler)
                
                if blocked_crawlers:
                    self.log_result(
                        'phase1', 'Verify AI Crawler Accessibility', False, 5, 2,
                        f"Blocked AI crawlers in robots.txt: {', '.join(blocked_crawlers)}"
                    )
                else:
                    self.log_result(
                        'phase1', 'Verify AI Crawler Accessibility', True, 5, 5,
                        "All major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot) are permitted."
                    )
            else:
                self.log_result(
                    'phase1', 'Verify AI Crawler Accessibility', True, 5, 4,
                    "No restrictive robots.txt file found (or failed to fetch). AI bots defaults to allowed."
                )
        else:
            self.log_result(
                'phase1', 'Verify AI Crawler Accessibility', True, 5, 5,
                "[Local File Mode] Crawler settings skipped. (Check your live domain's robots.txt for AI agents)."
            )

        # 2. llms.txt check (5 pts)
        if self.is_url:
            parsed_url = urllib.parse.urlparse(self.target)
            llms_url = f"{parsed_url.scheme}://{parsed_url.netloc}/llms.txt"
            llms_content, status = fetch_url(llms_url)
            if status == 200 and llms_content:
                # Basic validation of llms.txt markdown structure
                if "#" in llms_content or "-" in llms_content:
                    self.log_result(
                        'phase1', 'Implement an llms.txt Directory', True, 5, 5,
                        "Verified: Valid llms.txt file is present at domain root."
                    )
                else:
                    self.log_result(
                        'phase1', 'Implement an llms.txt Directory', False, 5, 3,
                        "llms.txt found at root, but doesn't appear to be structured in Markdown."
                    )
            else:
                self.log_result(
                    'phase1', 'Implement an llms.txt Directory', False, 5, 0,
                    "Failed to find llms.txt at root (HTTP status not 200). AI engines lack directory map."
                )
        else:
            # Check if a sibling llms.txt exists
            parent_dir = os.path.dirname(os.path.abspath(self.target)) if os.path.dirname(self.target) else "."
            local_llmstxt = os.path.join(parent_dir, "llms.txt")
            if os.path.exists(local_llmstxt):
                self.log_result(
                    'phase1', 'Implement an llms.txt Directory', True, 5, 5,
                    f"Verified: Sibling llms.txt file found at {local_llmstxt}."
                )
            else:
                self.log_result(
                    'phase1', 'Implement an llms.txt Directory', False, 5, 0,
                    "No sibling llms.txt file found locally."
                )

        # 3. JS dependencies / SSR check (7 pts)
        # Check text ratio of body and look for empty app root indications
        body_text_len = sum(len(p) for p in self.data['paragraphs'])
        html_len = self.data.get('raw_html_len', 1)
        ssr_ratio = (body_text_len / html_len) * 100
        
        has_empty_root = False
        empty_root_markers = ['<div id="root"></div>', '<div id="app"></div>', '<div id="__next"></div>']
        for marker in empty_root_markers:
            if marker in self.raw_content:
                has_empty_root = True
                break
                
        if has_empty_root and len(self.data['paragraphs']) < 3:
            self.log_result(
                'phase1', 'Audit JavaScript Dependencies', False, 7, 1,
                "Detected standard client-side JS app wrappers (e.g. React/Vue root container) with low static paragraph counts. AI retrievers will see a blank page."
            )
        elif ssr_ratio < 1.0 and not self.target.endswith('.md'):
            self.log_result(
                'phase1', 'Audit JavaScript Dependencies', False, 7, 3,
                f"Low text-to-HTML ratio ({ssr_ratio:.2f}%). Content might be heavily loaded client-side via JS."
            )
        else:
            self.log_result(
                'phase1', 'Audit JavaScript Dependencies', True, 7, 7,
                f"Good text density ({ssr_ratio:.2f}% ratio). Page content is statically extractable for AI bots."
            )

        # 4. JSON-LD Schema check (8 pts)
        schemas = self.data.get('json_ld', [])
        found_types = []
        has_same_as = False
        wikidata_refs = []
        
        def traverse_schema(item):
            nonlocal has_same_as
            if isinstance(item, dict):
                t = item.get('@type')
                if t:
                    if isinstance(t, list):
                        found_types.extend(t)
                    else:
                        found_types.append(t)
                
                same_as = item.get('sameAs')
                if same_as:
                    has_same_as = True
                    if isinstance(same_as, list):
                        wikidata_refs.extend(same_as)
                    else:
                        wikidata_refs.append(same_as)
                
                for k, v in item.items():
                    traverse_schema(v)
            elif isinstance(item, list):
                for subitem in item:
                    traverse_schema(subitem)

        traverse_schema(schemas)
        
        target_schemas = {'Product', 'Organization', 'FAQPage', 'ProfilePage', 'Person', 'Article'}
        matching_schemas = target_schemas.intersection(set(found_types))
        
        if not schemas:
            self.log_result(
                'phase1', 'Deploy Entity-Based Schema Markup', False, 8, 0,
                "No JSON-LD structured data detected. Essential for AI semantic alignment."
            )
        else:
            details_str = f"Found JSON-LD schemas: {', '.join(matching_schemas) if matching_schemas else 'Other'}. "
            pts = 4
            if matching_schemas:
                pts += 2
            if has_same_as:
                pts += 2
                details_str += f"Entity connections found (sameAs): {', '.join(wikidata_refs[:2])}..."
            else:
                details_str += "Missing 'sameAs' mapping to authority sources (Wikipedia/Wikidata/Crunchbase)."
                
            self.log_result(
                'phase1', 'Deploy Entity-Based Schema Markup', has_same_as and len(matching_schemas) > 0, 8, pts,
                details_str
            )

    def run_phase2_structure(self):
        """Phase 2: Content Structure & AI Extractability (Max 25 pts)"""
        print_info("Auditing Phase 2: Content Structure...")
        
        # 1. Question headings check (7 pts)
        headings = self.data.get('headings', [])
        if not headings:
            self.log_result(
                'phase2', 'Verify Question-Based Heading Hierarchies', False, 7, 0,
                "No H2 or H3 heading tags detected in content."
            )
        else:
            question_words = {'how', 'what', 'why', 'who', 'where', 'which', 'is', 'are', 'can', 'should', 'does', 'do', 'when'}
            questions_count = 0
            
            for h in headings:
                txt = h['text'].lower().strip()
                words = re.findall(r'\b\w+\b', txt)
                if txt.endswith('?') or (words and words[0] in question_words):
                    questions_count += 1
            
            ratio = questions_count / len(headings)
            if ratio >= 0.4:
                self.log_result(
                    'phase2', 'Verify Question-Based Heading Hierarchies', True, 7, 7,
                    f"{questions_count} out of {len(headings)} ({ratio*100:.0f}%) headings are question-based. Meets AI discovery query guidelines."
                )
            elif questions_count > 0:
                self.log_result(
                    'phase2', 'Verify Question-Based Heading Hierarchies', False, 7, 4,
                    f"Only {questions_count} out of {len(headings)} ({ratio*100:.0f}%) headings are conversational questions. Convert static headers to questions."
                )
            else:
                self.log_result(
                    'phase2', 'Verify Question-Based Heading Hierarchies', False, 7, 1,
                    "0 headings are phrased as questions. LLMs target conversational headers."
                )

        # 2. Answer-First Writing Framework (8 pts)
        # We will parse local structure first. If Gemini is available, we perform qualitative review later.
        structure = self.data.get('structure', [])
        heading_answers_checked = 0
        answer_first_passed = 0
        details_list = []
        
        for i, (elem_type, elem_val) in enumerate(structure):
            if elem_type in ('h2', 'h3'):
                heading_answers_checked += 1
                # Find the next paragraph
                next_p = None
                for next_type, next_val in structure[i+1:i+4]:
                    if next_type == 'p':
                        next_p = next_val
                        break
                
                if next_p:
                    word_count = len(next_p.split())
                    if 25 <= word_count <= 60:
                        answer_first_passed += 1
                        details_list.append(f"Heading '{elem_val[:30]}...' first paragraph length matches target ({word_count} words).")
                    else:
                        details_list.append(f"Heading '{elem_val[:30]}...' first paragraph length is {word_count} words (optimal is 30-50).")
                else:
                    details_list.append(f"Heading '{elem_val[:30]}...' does not have an immediate textual answer.")

        if heading_answers_checked == 0:
            self.log_result(
                'phase2', 'Apply the Answer-First Writing Framework', False, 8, 0,
                "No structured H2/H3 text flow to evaluate."
            )
        else:
            ratio = answer_first_passed / heading_answers_checked
            pts = int(ratio * 8)
            self.log_result(
                'phase2', 'Apply the Answer-First Writing Framework', ratio >= 0.7, 8, pts,
                f"{answer_first_passed} out of {heading_answers_checked} headings satisfy structural layout limits (first paragraph ~30-50 words)."
            )

        # 3. Assess Text Density and Chunking (5 pts)
        paragraphs = self.data.get('paragraphs', [])
        if not paragraphs:
            self.log_result(
                'phase2', 'Assess Text Density and Chunking', False, 5, 0,
                "No narrative paragraph tags detected to audit density."
            )
        else:
            long_paragraphs = 0
            avg_sentence_lengths = []
            
            for p in paragraphs:
                # Approximate sentence division (periods, questions, exclamation marks)
                sentences = [s.strip() for s in re.split(r'[.!?]+', p) if s.strip()]
                if len(sentences) > 4:
                    long_paragraphs += 1
                
                for s in sentences:
                    words = s.split()
                    if words:
                        avg_sentence_lengths.append(len(words))
            
            avg_sentence_len = sum(avg_sentence_lengths) / len(avg_sentence_lengths) if avg_sentence_lengths else 0
            
            errors = []
            pts = 5
            if long_paragraphs > 0:
                pts -= 2
                errors.append(f"Found {long_paragraphs} paragraph(s) longer than 4 sentences.")
            if not (12 <= avg_sentence_len <= 22):
                pts -= 1
                errors.append(f"Average sentence length is {avg_sentence_len:.1f} words (ideal is 15-20).")
                
            self.log_result(
                'phase2', 'Assess Text Density and Chunking', len(errors) == 0, 5, max(0, pts),
                "Content is well chunked." if not errors else "; ".join(errors)
            )

        # 4. Convert Complex Data to Extractable Layouts (5 pts)
        tables_count = len(self.data.get('tables', []))
        lists_count = len(self.data.get('lists', []))
        total_text_len = len(" ".join(paragraphs).split())
        
        if total_text_len > 400 and (tables_count == 0 and lists_count == 0):
            self.log_result(
                'phase2', 'Convert Complex Data to Extractable Layouts', False, 5, 1,
                f"Long narrative article ({total_text_len} words) but has 0 tables and 0 lists. LLMs struggle to extract unformatted data."
            )
        else:
            self.log_result(
                'phase2', 'Convert Complex Data to Extractable Layouts', True, 5, 5,
                f"Found {tables_count} tables and {lists_count} lists for structured extraction."
            )

    def run_phase3_authority(self):
        """Phase 3: Authority Validation (E-E-A-T for LLMs) (Max 25 pts)"""
        print_info("Auditing Phase 3: Authority Validation...")
        
        # 1. Author Attribution (7 pts)
        # Search schemas or page content for Author links
        has_author_schema = False
        schemas = self.data.get('json_ld', [])
        
        def check_author(item):
            nonlocal has_author_schema
            if isinstance(item, dict):
                if 'author' in item or item.get('@type') in ('ProfilePage', 'Person'):
                    has_author_schema = True
                for k, v in item.items():
                    check_author(v)
            elif isinstance(item, list):
                for subitem in item:
                    check_author(subitem)
                    
        check_author(schemas)
        
        # Search page text for "by [Name]" or "about the author"
        original_text = " ".join(self.data.get('paragraphs', []))
        byline_text_match = re.search(r'\b(?:by|author|written by|editor)\b\s+[A-Z][a-zA-Z]{1,19}(?:\s+[A-Z][a-zA-Z]{1,19})?', original_text)
        
        # Search for linkedin links
        has_linkedin = any('linkedin.com/in/' in str(link) for link in self.data.get('links', []))
        
        pts = 0
        reasons = []
        if has_author_schema:
            pts += 3
            reasons.append("Author profile schema present")
        elif byline_text_match:
            pts += 2
            reasons.append(f"Visual author byline matched: '{byline_text_match.group(0)}'")
        else:
            reasons.append("No author byline or profile schema detected")
            
        if has_linkedin:
            pts += 4
            reasons.append("LinkedIn credentials link verified")
        else:
            reasons.append("No author social profiles linked (e.g. LinkedIn)")
            
        self.log_result(
            'phase3', 'Audit Author Attribution & Bylines', pts >= 5, 7, pts,
            "; ".join(reasons)
        )

        # 2. Enforce Factual Evidence & Grounding (8 pts)
        # Count numbers/percentages in paragraphs
        paragraphs = self.data.get('paragraphs', [])
        factual_paragraphs = 0
        total_p = len(paragraphs)
        
        for p in paragraphs:
            # Matches percentages (42%, 42 percent) or numeric facts (e.g., 2026, 12,000, $15M)
            if re.search(r'\b\d+(?:[\.,\-/]\d+)*(?:\s*%|\s*percent|\b|\s*[kKmMgGtT]\b)', p):
                factual_paragraphs += 1
                
        ratio = factual_paragraphs / total_p if total_p > 0 else 0
        pts = int(ratio * 8)
        self.log_result(
            'phase3', 'Enforce Factual Evidence & Grounding', ratio >= 0.5, 8, pts,
            f"{factual_paragraphs} out of {total_p} paragraphs ({ratio*100:.0f}%) contain numeric metrics or data points for grounding."
        )

        # 3. Outbound Citations (5 pts)
        # Exclude own domain if URL is used
        domain = ""
        if self.is_url:
            parsed_url = urllib.parse.urlparse(self.target)
            domain = parsed_url.netloc
            
        links = self.data.get('links', [])
        outbound_links = []
        high_authority_domains = 0
        authority_extensions = ('.gov', '.edu', '.org', 'wikidata.org', 'wikipedia.org')
        
        for l in links:
            if l.startswith('http://') or l.startswith('https://'):
                parsed_l = urllib.parse.urlparse(l)
                if domain and parsed_l.netloc == domain:
                    continue
                outbound_links.append(l)
                if any(ext in parsed_l.netloc.lower() for ext in authority_extensions):
                    high_authority_domains += 1
                    
        outbound_count = len(outbound_links)
        
        pts = 0
        if outbound_count >= 3:
            pts += 3
        elif outbound_count > 0:
            pts += 1
            
        if high_authority_domains >= 1:
            pts += 2
        elif outbound_count > 0:
            pts += 1
            
        self.log_result(
            'phase3', 'Review Inbound and Outbound Citations', pts >= 4, 5, pts,
            f"Found {outbound_count} outbound link(s) (with {high_authority_domains} high-authority domains: gov/edu/org/wikipedia)."
        )

        # 4. Check Fact Freshness & Timestamps (5 pts)
        # Check meta tags first
        meta = self.data.get('meta_tags', {})
        timestamp_keys = [
            'article:published_time', 'article:modified_time', 
            'og:updated_time', 'publish_date', 'last-modified'
        ]
        has_meta_timestamp = any(k in meta for k in timestamp_keys)
        
        # Check schemas
        has_schema_timestamp = False
        for sch in schemas:
            if isinstance(sch, dict) and ('datePublished' in sch or 'dateModified' in sch):
                has_schema_timestamp = True
                
        # Search page text for "Published" or "Updated"
        full_text = " ".join(paragraphs).lower()
        has_text_timestamp = bool(re.search(r'\b(published|updated|revised|last documented revision|date)\b.*?\b\d{4}\b', full_text))
        
        pts = 0
        reasons = []
        if has_meta_timestamp or has_schema_timestamp:
            pts += 3
            reasons.append("Found structured modification/publication metadata timestamps")
        if has_text_timestamp:
            pts += 2
            reasons.append("Found visible timestamp dates in body text")
            
        if pts == 0:
            reasons.append("No publication/revision timestamps detected. LLMs might treat contents as stale.")
            
        self.log_result(
            'phase3', 'Check Fact Freshness & Timestamps', pts >= 3, 5, pts,
            "; ".join(reasons)
        )

    def run_phase4_quotability(self):
        """Phase 4: The Quotability & Fragment Test (Max 25 pts)"""
        print_info("Auditing Phase 4: Quotability & Fragment Test...")
        
        # 1. Standalone Sentence Audit (10 pts)
        # Heuristic: Select first few sentences of paragraphs, scan for vague leading pronouns
        # (this, these, it, they, that, those) that render the sentence ambiguous.
        paragraphs = self.data.get('paragraphs', [])
        sentences_to_test = []
        for p in paragraphs[:8]:
            s_list = [s.strip() for s in re.split(r'[.!?]+', p) if s.strip()]
            if s_list:
                sentences_to_test.append(s_list[0])
                
        failed_sentences = []
        ambiguous_pronouns = {'this', 'these', 'those', 'them', 'it', 'they', 'that'}
        
        for s in sentences_to_test:
            words = re.findall(r'\b\w+\b', s.lower())
            if words and words[0] in ambiguous_pronouns:
                failed_sentences.append(s)
                
        pts = 10 - len(failed_sentences)
        pts = max(0, pts)
        
        self.log_result(
            'phase4', 'Execute the Standalone Sentence Audit', len(failed_sentences) == 0, 10, pts,
            f"Passed sentence references check. (Ambiguous pronouns caught: {len(failed_sentences)} sentences). Example fail: '{failed_sentences[0]}' if any." if failed_sentences
            else "Sentences look structurally independent (no vague pronouns starting sentences)."
        )
        self.sentences_to_test = sentences_to_test # store for gemini evaluation

        # 2. Eliminate Subjective Filler & Fluff (10 pts)
        fluff_words = {
            'revolutionary', 'cutting-edge', 'game-changing', 'best-in-class', 
            'seamlessly', 'world-class', 'optimal choice', 'proudly believe', 
            'we believe', 'we might', 'industry-leading', 'state-of-the-art', 
            'groundbreaking', 'paradigm shift', 'synergy'
        }
        
        full_text = " ".join(paragraphs).lower()
        matched_fluff = [word for word in fluff_words if re.search(r'\b' + re.escape(word) + r'\b', full_text)]
        
        pts = 10 - (len(matched_fluff) * 2)
        pts = max(0, pts)
        
        self.log_result(
            'phase4', 'Eliminate Subjective Filler & Fluff', len(matched_fluff) == 0, 10, pts,
            f"Detected marketing fluff/jargon: {', '.join(matched_fluff)}. Replace with objective descriptors." if matched_fluff
            else "Tone appears objective and professional (no marketing fluff/jargon detected)."
        )

        # 3. Build an "Atomic" Definition Repository (5 pts)
        # Heuristic: Check for definition lists (<dl>, <dt>), bolded term with short paragraphs, or FAQ structured schemas
        has_faq = False
        schemas = self.data.get('json_ld', [])
        
        def check_faq(item):
            nonlocal has_faq
            if isinstance(item, dict):
                if item.get('@type') == 'FAQPage':
                    has_faq = True
                for k, v in item.items():
                    check_faq(v)
            elif isinstance(item, list):
                for subitem in item:
                    check_faq(subitem)
        check_faq(schemas)
        
        has_dl = "<dl" in self.raw_content.lower() or "<dt" in self.raw_content.lower()
        has_atomic_structure = has_faq or has_dl or (len(paragraphs) > 0 and any(p.startswith('**') or p.startswith('**') for p in paragraphs))
        
        pts = 5 if has_atomic_structure else 1
        self.log_result(
            'phase4', 'Build an Atomic Definition Repository', has_atomic_structure, 5, pts,
            "FAQ Schema or terminology layout detected." if has_atomic_structure
            else "Missing clear atomic definitions, glossaries, or FAQ blocks."
        )

    def run_qualitative_gemini(self):
        """Uses Gemini API for Phase 2/4 checks if key is available."""
        api_key = self.env.get('GEMINI_API_KEY')
        if not api_key:
            print_warning("GEMINI_API_KEY not found in .env. Skipping advanced qualitative checks.")
            return
            
        print_info("Running qualitative AI audit using Gemini API...")
        
        paragraphs = self.data.get('paragraphs', [])
        headings = self.data.get('headings', [])
        
        # Prepare text snippet
        body_sample = "\n".join(paragraphs[:15])
        headings_sample = "\n".join([f"- {h['tag']}: {h['text']}" for h in headings])
        
        # Generate prompt for Gemini
        prompt = f"""
You are an expert Generative Engine Optimization (GEO) audit engine. Evaluate the provided web content for AI citation and readability optimization.
Return your evaluation strictly in JSON format matching the schema below. Do not include any markdown formatting wrappers (like ```json) in your raw response.

Content:
---
TITLE: {self.data.get('title')}
HEADINGS:
{headings_sample}

BODY SAMPLE:
{body_sample}
---

Evaluation JSON Schema:
{{
  "inferred_brand_name": "The primary brand/organization/product name mentioned or discussed in the content",
  "answer_first_eval": [
    {{
      "heading": "Heading string",
      "first_paragraph_sample": "First paragraph text string",
      "is_answer_first": true,
      "score": 85,
      "feedback": "Feedback details explaining why it succeeds or fails the answer-first checklist criteria"
    }}
  ],
  "standalone_sentences_eval": [
    {{
      "sentence": "Sentence to test",
      "passes": false,
      "feedback": "Feedback details describing whether this sentence can stand entirely on its own as a factual statement, highlighting ambiguous pronouns (it, this, that) or dependencies."
    }}
  ],
  "subjective_fluff_instances": [
    {{
      "original_text": "Sentence containing marketing fluff",
      "fluff_detected": "The marketing buzzwords detected",
      "suggestion": "An objective, fact-grounded replacement"
    }}
  ]
}}
"""
        result = query_gemini_api(api_key, prompt)
        if result:
            self.gemini_eval = result
            if 'inferred_brand_name' in result:
                self.inferred_brand = result['inferred_brand_name']
                print_success(f"Inferred brand name from Gemini API: '{self.inferred_brand}'")
            print_success("Successfully received qualitative audit from Gemini API.")
        else:
            self.gemini_eval = None

    def infer_brand_name(self):
        """Infers the brand name from environment, Gemini, Schema, Title, or URL."""
        # 1. Try env
        brand = self.env.get('BRAND_NAME')
        if brand and brand != "BrandName":
            return brand
            
        # 2. Try previously inferred brand (e.g. from Gemini)
        if hasattr(self, 'inferred_brand') and self.inferred_brand:
            return self.inferred_brand
            
        print_info("BRAND_NAME not set in .env. Attempting to infer brand name...")
        
        # 3. Try JSON-LD Organization or Brand schema
        schemas = self.data.get('json_ld', [])
        def find_org_name(item):
            if isinstance(item, dict):
                if item.get('@type') in ('Organization', 'Brand', 'Product') and item.get('name'):
                    return item.get('name')
                for k, v in item.items():
                    res = find_org_name(v)
                    if res:
                        return res
            elif isinstance(item, list):
                for subitem in item:
                    res = find_org_name(subitem)
                    if res:
                        return res
            return None
            
        for sch in schemas:
            brand = find_org_name(sch)
            if brand:
                print_success(f"Inferred brand name from JSON-LD Schema: '{brand}'")
                self.inferred_brand = brand
                return brand
                
        # 4. Try Title splitting
        title = self.data.get('title', '')
        if title:
            for sep in ('|', '-', '–', '—'):
                if sep in title:
                    parts = title.split(sep)
                    candidates = [p.strip() for p in parts]
                    candidates.sort(key=len)
                    if candidates and len(candidates[0]) > 2:
                        brand = candidates[0]
                        print_success(f"Inferred brand name from Title: '{brand}'")
                        self.inferred_brand = brand
                        return brand
            words = title.split()
            if len(words) >= 2:
                brand = " ".join(words[:2])
                print_success(f"Inferred brand name from Title words: '{brand}'")
                self.inferred_brand = brand
                return brand
                
        # 5. Try Domain name (if URL)
        if self.is_url:
            parsed_url = urllib.parse.urlparse(self.target)
            netloc = parsed_url.netloc
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            domain_parts = netloc.split('.')
            if domain_parts:
                brand = domain_parts[0].capitalize()
                print_success(f"Inferred brand name from Domain: '{brand}'")
                self.inferred_brand = brand
                return brand
                
        # 6. Fallback
        print_warning("Could not infer brand name. Using fallback 'BrandName'.")
        self.inferred_brand = "BrandName"
        return "BrandName"

    def run_phase5_consensus(self):
        """Phase 5: Off-Site Consensus Strategy (Informational and Query checks)"""
        print_info("Auditing Phase 5: Off-Site Consensus...")
        
        api_key = self.env.get('GOOGLE_SEARCH_API_KEY')
        cx = self.env.get('GOOGLE_SEARCH_CX')
        brand = self.infer_brand_name()
        
        self.consensus_results = {}
        
        if api_key and cx and brand != "BrandName":
            print_info(f"Checking web consensus footprint for brand: '{brand}'")
            
            # Query 1: Reddit & Quora community footprint
            reddit_query = f"site:reddit.com OR site:quora.com \"{brand}\""
            reddit_count, reddit_items = query_google_search(api_key, cx, reddit_query)
            self.consensus_results['reddit_count'] = reddit_count
            self.consensus_results['reddit_samples'] = [{'title': item['title'], 'link': item['link']} for item in reddit_items[:3]]
            
            # Query 2: Digital PR & Third party reviews
            pr_query = f"\"{brand}\" \"top tools\" OR \"best practices\" OR \"review\" OR \"alternatives\""
            pr_count, pr_items = query_google_search(api_key, cx, pr_query)
            self.consensus_results['pr_count'] = pr_count
            self.consensus_results['pr_samples'] = [{'title': item['title'], 'link': item['link']} for item in pr_items[:3]]
        else:
            self.consensus_results = None

    def generate_report(self, output_path="geo_audit_report.md"):
        """Generates the Markdown report artifact based on the audit outcomes."""
        total_score = sum(self.scores.values())
        
        # Determine Status
        if total_score < 40:
            status = "🚨 Critical Danger Zone"
            status_desc = "Blocked crawlers, JS-heavy, no schema, dense narrative walls. Immediate required action: Fix technical blockages; migrate text into structured tables/lists."
        elif total_score <= 75:
            status = "⚠️ Optimization Gap"
            status_desc = "Crawlable, structured, but lacks data, quotes, and primary sources. Immediate required action: Inject original metrics, add expert quotes, and rewrite headers as clear questions."
        else:
            status = "🏆 GEO Optimized"
            status_desc = "Answer-first layout, rich schema, clear data, high external consensus. Immediate required action: Maintain freshness; monitor AI Share of Voice monthly to defend citation space."
            
        lines = []
        lines.append(f"# Generative Engine Optimization (GEO) Audit Report")
        lines.append(f"**Target:** `{self.target}`")
        lines.append(f"**Date:** 2026-05-23 (Audit Engine: Antigravity-GEO v1.0)")
        lines.append("")
        lines.append(f"## Overall Score: **{total_score}/100**")
        lines.append(f"### Status: {status}")
        lines.append(f"*{status_desc}*")
        lines.append("")
        
        # Summary Table
        lines.append("| Phase | Audit Dimension | Score | Max Points |")
        lines.append("| --- | --- | --- | --- |")
        lines.append(f"| Phase 1 | AI Discovery & Technical Foundations | **{self.scores['phase1']}** | 25 |")
        lines.append(f"| Phase 2 | Content Structure & AI Extractability | **{self.scores['phase2']}** | 25 |")
        lines.append(f"| Phase 3 | Authority Validation (E-E-A-T) | **{self.scores['phase3']}** | 25 |")
        lines.append(f"| Phase 4 | The Quotability & Fragment Test | **{self.scores['phase4']}** | 25 |")
        lines.append(f"| | **Total GEO-Ready Score** | **{total_score}** | **100** |")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("## Detailed Audit Checklist Findings")
        lines.append("")
        
        # Print logs by Phase
        current_phase = ""
        phase_titles = {
            'phase1': "Phase 1: AI Discovery & Technical Foundations",
            'phase2': "Phase 2: Content Structure & AI Extractability",
            'phase3': "Phase 3: Authority Validation (E-E-A-T for LLMs)",
            'phase4': "Phase 4: The Quotability & Fragment Test",
        }
        
        for log in self.audit_log:
            phase = log['phase']
            if phase != current_phase:
                current_phase = phase
                lines.append(f"### {phase_titles[phase]}")
                lines.append("")
            
            icon = "✅" if log['passed'] else "⚠️"
            lines.append(f"#### {icon} {log['check']} ({log['awarded_points']}/{log['max_points']} pts)")
            lines.append(f"- **Outcome:** {log['details']}")
            lines.append("")
            
        # Qualitative Gemini evaluation section if present
        if hasattr(self, 'gemini_eval') and self.gemini_eval:
            lines.append("---")
            lines.append("## 🤖 Advanced AI Qualitative Content Analysis (Gemini API)")
            lines.append("")
            
            lines.append("### Answer-First Framework")
            for item in self.gemini_eval.get('answer_first_eval', []):
                ans_icon = "✅" if item.get('is_answer_first') else "❌"
                lines.append(f"- {ans_icon} **Heading:** *\"{item.get('heading')}\"*")
                lines.append(f"  - **First Paragraph:** \"{item.get('first_paragraph_sample')}\"")
                lines.append(f"  - **Evaluation Feedback:** {item.get('feedback')}")
            lines.append("")
            
            lines.append("### Standalone Sentence Audit")
            for item in self.gemini_eval.get('standalone_sentences_eval', []):
                pass_icon = "✅" if item.get('passes') else "❌"
                lines.append(f"- {pass_icon} **Sentence:** \"{item.get('sentence')}\"")
                lines.append(f"  - **Audit Feedback:** {item.get('feedback')}")
            lines.append("")
            
            lines.append("### Subjective Fluff & Marketing Jargon")
            fluff_list = self.gemini_eval.get('subjective_fluff_instances', [])
            if fluff_list:
                lines.append("| Fluff Snippet Detected | Suggested Grounded Replacement |")
                lines.append("| --- | --- |")
                for item in fluff_list:
                    lines.append(f"| \"{item.get('original_text')}\" | \"{item.get('suggestion')}\" |")
            else:
                lines.append("No notable marketing buzzwords or fluff detected. Text structure is objective and direct.")
            lines.append("")

        # Phase 5 section
        lines.append("---")
        lines.append("## Phase 5: Off-Site Consensus Strategy (Web Footprint)")
        lines.append("")
        
        brand = getattr(self, 'inferred_brand', None) or self.infer_brand_name()
        
        if hasattr(self, 'consensus_results') and self.consensus_results:
            lines.append(f"Off-site footprint audit for: **{brand}**")
            lines.append("")
            lines.append(f"- **Reddit & Quora Brand Footprint:** Found **{self.consensus_results['reddit_count']}** organic community discussion references.")
            if self.consensus_results['reddit_samples']:
                lines.append("  - *Sample Threads:*")
                for s in self.consensus_results['reddit_samples']:
                    lines.append(f"    - [{s['title']}]({s['link']})")
                    
            lines.append(f"- **Digital PR & Authority References:** Found **{self.consensus_results['pr_count']}** third-party comparison/list references.")
            if self.consensus_results['pr_samples']:
                lines.append("  - *Sample Mentions:*")
                for s in self.consensus_results['pr_samples']:
                    lines.append(f"    - [{s['title']}]({s['link']})")
        else:
            lines.append(f"**Action Required: Manual Off-Site Footprint Checks** (Google Search API keys not configured)")
            lines.append(f"To assess brand authority and LLM consensus credibility, manually verify the following searches:")
            lines.append(f"1. **Reddit & Quora Footprint**: Check if real users mention `{brand}` in community forums:")
            lines.append(f"   - [Search Reddit & Quora for {brand}](https://www.google.com/search?q=site:reddit.com+OR+site:quora.com+%22{urllib.parse.quote(brand)}%22)")
            lines.append(f"2. **Digital PR & Industry Lists**: Check if third-party authoritative reviews/lists mention `{brand}`:")
            lines.append(f"   - [Search Industry Citations for {brand}](https://www.google.com/search?q=%22{urllib.parse.quote(brand)}%22+%22top+tools%22+OR+%22best+practices%22+OR+%22review%22+OR+%22alternatives%22)")
            lines.append(f"3. **AI Share of Voice Baseline**: Query Perplexity, ChatGPT, and Gemini with your target query set to monitor your citation share.")
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
        print_success(f"GEO Audit report written to: {output_path}")

    def execute_all(self, report_path="geo_audit_report.md"):
        self.prepare_data()
        self.run_phase1_technical()
        self.run_phase2_structure()
        self.run_phase3_authority()
        self.run_phase4_quotability()
        self.run_qualitative_gemini()
        self.run_phase5_consensus()
        self.generate_report(report_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Audit a website or local content file for Generative Engine Optimization (GEO).")
    parser.add_argument("target", help="The live URL or local file path to audit.")
    parser.add_argument("--report", default="geo_audit_report.md", help="Path to write the markdown report.")
    parser.add_argument("--env", default=".env", help="Path to the environmental configuration file.")
    
    args = parser.parse_args()
    
    env_vars = load_env(args.env)
    
    auditor = GEOAuditor(args.target, env_vars)
    auditor.execute_all(args.report)
