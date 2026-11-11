import re


def secondary_split(text: str, max_words: int = 400, overlap: int = 50, title: str = '') -> list:
    """Splits text into smaller overlapping word chunks if it exceeds max_words."""
    if title.lower() == 'rule 1 definitions':
        return parse_definitions(text)
    if title.lower() == '1. definitions':
        print('parsing cape')
        return parse_definitions_cape(text)

    words = text.split()
    if len(words) <= max_words:
        return [text]

    sub_chunks = []
    start = 0
    while start < len(words):
        end = start + max_words
        chunk = " ".join(words[start:end])
        sub_chunks.append(chunk)
        start += max_words - overlap
    return sub_chunks


def split_by_header_default(text: str, doc_name: str, max_words: int = 400) -> list:
    sections = []
    tag = "|||H3_SPLIT|||"
    processed = text.replace("\n### ", f"\n{tag}")

    for index, raw_section in enumerate(processed.strip().split(tag)):
        if not raw_section.strip():
            continue

        section_lines = raw_section.lstrip('#').strip().split('\n\n')
        raw_title = section_lines[0].strip() if section_lines else ""
        title = raw_title.lstrip('#').strip()

        # Extract valid raw lines matching default criteria
        raw_chunks = [
            line.strip() for line in section_lines
            if line.strip() and line.strip() != title.strip() and "Note" not in line
        ]

        # Process each chunk through secondary_split
        for i, content in enumerate(raw_chunks):
            sub_chunks = secondary_split(content, max_words=max_words, overlap=50)

            for idx, sub_content in enumerate(sub_chunks):
                sections.append({
                    'metadata': {
                        'company': doc_name,
                        'title': title,
                        'part': f"{index}.{i+1}.{idx + 1 if len(sub_chunks) > 1 else 1}"
                    },
                    'content': sub_content
                })

    return sections


def split_by_header_cape(text: str, doc_name: str, max_words: int = 400) -> list:
    sections = []
    tag = "|||H2_SPLIT|||"
    
    # Safe split fallback in case "1. Definitions" isn't present
    split_parts = re.split(r"(?=1\.\s*Definitions)", text.replace("\n## ", f"\n{tag}"))
    processed = split_parts[1] if len(split_parts) > 1 else split_parts[0]

    for index, raw_section in enumerate(processed.strip().split(tag)):
        if not raw_section.strip():
            continue

        pattern = r'(?<!\*)\*\*{1,2}(?:[a-z]\.\s+[A-Z]|[A-Z])'
        cleaned_section = re.sub(r'\d+\.\-\s', '', raw_section)
        cleaned_chunks = re.split(f'(?={pattern})', cleaned_section)

        section_lines = raw_section.strip().split('\n\n')
        raw_title = section_lines[0].strip() if section_lines else ""
        title = raw_title.lstrip('*').rstrip('*').strip()

        pattern_cleaning = r"[^a-zA-Z0-9\s.,\/#!$%\^&\*;:{}=\-_`~()\[\]?|\n\n]"

        raw_chunks = [
            re.sub(pattern_cleaning, "", line) 
            for line in cleaned_chunks 
            if line.strip() and line.strip().rstrip('-').strip().strip('*').strip() != title.strip()
        ]

        for i, content in enumerate(raw_chunks):
            sub_chunks = secondary_split(content, max_words=max_words, overlap=50, title=title)

            for idx, sub_content in enumerate(sub_chunks):
                sections.append({
                    'metadata': {
                        'company': doc_name,
                        'title': title,
                        'part': f"{index}.{i+1}.{idx + 1 if len(sub_chunks) > 1 else 1}"
                    },
                    'content': sub_content
                })

    return sections


def split_by_header_ua(text: str, doc_name: str, max_words: int = 400) -> list:
    sections = []
    tag = "|||H1_SPLIT|||"
    processed = text.replace("\n# ", f"\n{tag}")
    processed = processed.replace("## <u>Back to Top</u>", "")
    processed = processed.replace("## ", "")

    for index, raw_section in enumerate(processed.strip().split(tag)):
        if not raw_section.strip():
            continue

        section_lines = re.split(r'\n\n(?!\s*(?:(?:-\s*)?[a-z0-9]\.|-\s*<u>NOTE:))', raw_section.strip())
        raw_title = section_lines[0].strip() if section_lines else ""
        title = raw_title.lstrip('#').strip()

        if title in ('Table of Contents', '(revised May 11, 2026)'):
            continue

        rule_pattern = r'\bRule\s*\(?\d+\)?'
        clean_title = re.sub(rule_pattern, '', title).strip()

        raw_chunks = [
            line.replace(':', ' - ').replace(' means', ':').replace(' mean', ':') if title.lower() == 'rule 1 definitions' else line.strip()
            for line in section_lines
            if line.strip() and line.strip() != title.strip()
        ]

        # Process each chunk through secondary_split
        for i, content in enumerate(raw_chunks):
            sub_chunks = secondary_split(content, max_words=max_words, overlap=50, title=title)

            for idx, sub_content in enumerate(sub_chunks):
                sections.append({
                    'metadata': {
                        'company': doc_name,
                        'title': clean_title,
                        'part': f"{index - 2}.{i+1}.{idx + 1 if len(sub_chunks) > 1 else 1}"
                    },
                    'content': sub_content
                })

    return sections



def parse_definitions(text_or_lines: str | list[str]) -> list[str]:
    """
    Splits contract definition blocks into individual 'Term: Definition' strings.
    Ignores abbreviation periods (e.g., 'No.', 'e.g.') when detecting term boundaries.
    """
    # 1. Normalize input into a single clean string
    if isinstance(text_or_lines, list):
        text = " ".join([str(x).strip() for x in text_or_lines if str(x).strip()])
    else:
        text = str(text_or_lines).strip()

    if not text:
        return []

    text = re.sub(r'\s+', ' ', text)

    # 2. Pre-normalize alternative syntaxes ('means', 'is the') to colons
    text = re.sub(r'\s+means?\s+', ': ', text)
    text = re.sub(r'(\.\s+|^)([A-Z0-9\(\)“\"\'][^:]*?)\s+is\s+(?:the|a|an)\s+', r'\1\2: ', text)

    # 3. Split on colon
    splitted = text.strip().split(":")

    if len(splitted) <= 1:
        return [text] if text else []

    results = []
    current_term = splitted[0].strip()

    # Abbreviations that end with a period but should NOT be treated as sentence boundaries
    abbrev_pattern = r'\b(?:No|e\.g|i\.e|vs|Inc|Ltd|Dr|Mr|Mrs|Ms)\.$'

    # 4. Unpack [Definition N + Next Term] offset
    for i in range(1, len(splitted)):
        part = splitted[i].strip()

        if i == len(splitted) - 1:
            # Final chunk is purely the last definition
            definition = part
            if current_term and definition:
                results.append(f"{current_term}: {definition}")
        else:
            # Find all candidate sentence endings (. ! ?) followed by spaces
            matches = list(re.finditer(r'([\.\?!][)"”\'’\]]*)\s+', part))
            definition = ""
            next_term = ""
            found_boundary = False

            # Search backwards for the last TRUE sentence boundary (not an abbreviation like 'No.')
            for m in reversed(matches):
                punct_end_idx = m.start(1) + 1
                text_up_to_punct = part[:punct_end_idx]

                if not re.search(abbrev_pattern, text_up_to_punct, re.IGNORECASE):
                    definition = part[:m.end(1)].strip()
                    next_term = part[m.end():].strip()
                    found_boundary = True
                    break

            # Fallback if no non-abbreviation sentence end was found
            if not found_boundary:
                last_space = part.rfind(' ')
                if last_space != -1:
                    definition = part[:last_space].strip()
                    next_term = part[last_space:].strip()
                else:
                    definition = part
                    next_term = ""

            if current_term and definition:
                results.append(f"{current_term}: {definition}")

            current_term = next_term


    return results


def parse_definitions_cape(text: str | list[str]) -> list[str]:
    """
    Parses Cape Air markdown definition blocks into a list of 'Term: Definition' strings.
    Preserves internal bullet lists (-) and hyphenated terms (e.g., Non-Ambulatory).
    """
    if isinstance(text, list):
        full_text = "\n".join([str(x) for x in text if x is not None])
    else:
        full_text = str(text) if text is not None else ""

    if not full_text.strip():
        return []

    # Anchor strictly on Markdown bold tags **...**
    pattern = r"\*\*(.*?)\*\*"
    matches = list(re.finditer(pattern, full_text, re.DOTALL))
    results = []

    for i, match in enumerate(matches):
        raw_inside = match.group(1).strip()

        # Extract text body between this **...** tag and the next **...** tag
        start_body = match.end()
        end_body = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        raw_body = full_text[start_body:end_body]

        # Handle embedded definitions inside ** (e.g., **IATA: International Air Transport Association**)
        body_is_empty = not raw_body.strip() or bool(re.match(r"^[\s\-\.\:]+$", raw_body.strip()))

        if ":" in raw_inside and body_is_empty:
            term_part, def_part = raw_inside.split(":", 1)
            term = term_part.strip()
            definition = def_part.strip()
        else:
            term = raw_inside.strip()
            definition = raw_body

        # Clean term: strip trailing colons, dots, and spaces (do NOT strip hyphens)
        term = re.sub(r"[\:\.\s]+$", "", term).strip()

        # Clean definition: strip leading colons, dots, and spaces (preserve leading '-' for bullet lists)
        definition = re.sub(r"^[\:\.\s]+", "", definition).strip()

        # Strip only the trailing orphan bullet marker (the '-' that precedes the NEXT term)
        definition = re.sub(r"(?:\n|\r\n?)\s*[\-\–\—]\s*$", "", definition).strip()
        definition = re.sub(r"[\s\-\–\—]+$", "", definition).strip()

        if term and definition:
            results.append(f"{term} {'|||DELIMITER|||'} {definition}")

    print(results)

    return results


def get_string_to_embed(data: dict) -> str:
    metadata = data.get('metadata', {})
    return (
        f"Company: {metadata.get('company', 'N/A')}\n"
        f"Section: {metadata.get('title', 'N/A')}\n"
        f"Index: {metadata.get('part', 'N/A')}\n"
        f"Content: {data.get('content', '')}"
    )


def get_key_value(company: str, content: str) -> tuple[str, str]:
    pattern = r"^(.*?)\|\|\|DELIMITER\|\|\|(.*)$"
    
    match company.lower().strip():
        case "frontier":
            pattern = r"^-\s*(?:[A-Z]\.\s*)?(.*?)\s*(?:–|—|\s+-\s+)\s*(.*)$"
        case "united airlines":
            pattern = r"^(?:-\s*)?(?:\*\*)?(.*?)(?:\*\*)?\s*:\s*(.*)$"
        
    match = re.search(pattern, content.strip(), re.MULTILINE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", ""