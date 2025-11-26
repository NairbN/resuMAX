"""
Smart Resume Parser

Intelligently parses resumes of ANY format by:
1. Detecting section headers (EDUCATION, EXPERIENCE, SKILLS, etc.)
2. Extracting bullets using multiple patterns
3. Identifying contact info, dates, locations
4. Handling varied formatting (bullets, dashes, numbers, indentation)

Works with:
- Traditional formatted resumes (like Ryley's)
- ATS-friendly resumes
- Creative formatted resumes
- Resumes with or without bullets
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SectionType(Enum):
    """Common resume sections"""
    EDUCATION = "education"
    EXPERIENCE = "experience"
    SKILLS = "skills"
    PROJECTS = "projects"
    CERTIFICATIONS = "certifications"
    SUMMARY = "summary"
    UNKNOWN = "unknown"


@dataclass
class ContactInfo:
    """Structured contact information"""
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None


# Common section header variations
SECTION_HEADERS = {
    SectionType.EDUCATION: [
        r'\b(EDUCATION|Education|ACADEMIC|Academic|DEGREES?|Degrees?)\b',
    ],
    SectionType.EXPERIENCE: [
        r'\b(EXPERIENCE|Experience|WORK HISTORY|Work History|EMPLOYMENT|Employment|PROFESSIONAL EXPERIENCE|Professional Experience)\b',
    ],
    SectionType.SKILLS: [
        r'\b(SKILLS?|Skills?|TECHNICAL SKILLS|Technical Skills|CORE COMPETENCIES|Core Competencies|TECHNOLOGIES|Technologies)\b',
    ],
    SectionType.PROJECTS: [
        r'\b(PROJECTS?|Projects?|PERSONAL PROJECTS|Personal Projects|PORTFOLIO|Portfolio)\b',
    ],
    SectionType.CERTIFICATIONS: [
        r'\b(CERTIFICATIONS?|Certifications?|LICENSES?|Licenses?|CREDENTIALS?|Credentials?)\b',
    ],
    SectionType.SUMMARY: [
        r'\b(SUMMARY|Summary|OBJECTIVE|Objective|PROFILE|Profile|ABOUT|About)\b',
    ]
}


def extract_contact_info(text: str) -> ContactInfo:
    """
    Extract contact information from resume text.

    Looks for:
    - Email (pattern matching)
    - Phone (various formats)
    - LinkedIn, GitHub, personal website
    - Location (city, state)
    """
    contact = ContactInfo()

    # Email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        contact.email = email_match.group()

    # Phone (multiple formats)
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (607)232-8826 or 607-232-8826
        r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # International
    ]
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            contact.phone = phone_match.group()
            break

    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/([^\s|]+)', text)
    if linkedin_match:
        contact.linkedin = f"linkedin.com/in/{linkedin_match.group(1)}"

    # GitHub
    github_match = re.search(r'github\.com/([^\s|]+)', text)
    if github_match:
        contact.github = f"github.com/{github_match.group(1)}"

    # Website (look for common TLDs but exclude email domains, linkedin, github)
    website_match = re.search(r'\b([a-z0-9-]+\.(com|net|org|io|dev|info|tech))\b', text, re.IGNORECASE)
    if website_match:
        potential_website = website_match.group()
        # Don't use if it's part of email, linkedin, or github
        email_domain = contact.email.split('@')[1] if contact.email else None
        if potential_website not in [email_domain, contact.linkedin, contact.github]:
            # Make sure it's not just coincidentally matching part of linkedin/github
            if contact.linkedin and potential_website in contact.linkedin:
                pass  # Skip
            elif contact.github and potential_website in contact.github:
                pass  # Skip
            else:
                contact.website = potential_website

    return contact


def detect_section(line: str) -> Optional[SectionType]:
    """
    Detect if a line is a section header.

    Args:
        line: Text line

    Returns:
        SectionType if detected, else None

    Examples:
        "EDUCATION" → SectionType.EDUCATION
        "Work Experience" → SectionType.EXPERIENCE
        "Skills:" → SectionType.SKILLS
    """
    line_clean = line.strip()

    for section_type, patterns in SECTION_HEADERS.items():
        for pattern in patterns:
            if re.match(pattern, line_clean, re.IGNORECASE):
                return section_type

    return None


def is_bullet_point(line: str) -> bool:
    """
    Check if a line is a bullet point.

    Detects:
    - Traditional bullets: •, -, *, ○, ▪
    - Numbered lists: 1., 2., etc.
    - Indented lines (4+ spaces or tab)
    - Lines starting with action verbs

    Args:
        line: Text line

    Returns:
        True if line appears to be a bullet point
    """
    line_stripped = line.strip()

    if not line_stripped:
        return False

    # Bullet characters (including all common Unicode bullets)
    bullet_chars = ['•', '-', '*', '○', '▪', '▫', '■', '□', '◦', '‣', '⁃', '●', '◉', '▸', '▹', '►', '▻', '⦿', '⦾']
    if any(line_stripped.startswith(char) for char in bullet_chars):
        return True

    # Numbered bullets
    if re.match(r'^\d+\.', line_stripped):
        return True

    # Indented lines (but not section headers)
    if line.startswith('    ') or line.startswith('\t'):
        if not detect_section(line):
            return True

    # Action verbs (common resume starter words)
    action_verbs = [
        'built', 'developed', 'created', 'designed', 'implemented', 'led',
        'managed', 'improved', 'increased', 'reduced', 'achieved', 'delivered',
        'launched', 'optimized', 'automated', 'engineered', 'architected',
        'integrated', 'deployed', 'maintained', 'refactored', 'contributed',
        'collaborated', 'coordinated', 'established', 'trained', 'mentored'
    ]

    first_word = line_stripped.split()[0].lower() if line_stripped.split() else ""
    if first_word in action_verbs:
        return True

    return False


def extract_bullets_from_text(text: str) -> List[str]:
    """
    Extract ALL bullet points from resume text.

    Uses multiple heuristics to catch various formatting styles.

    Args:
        text: Full resume text

    Returns:
        List of bullet point strings
    """
    lines = text.split('\n')
    bullets = []

    current_bullet = ""

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        if not line_stripped:
            # Empty line - end current bullet if any
            if current_bullet:
                bullets.append(current_bullet.strip())
                current_bullet = ""
            continue

        # Check if this is a new bullet
        if is_bullet_point(line):
            # Save previous bullet
            if current_bullet:
                bullets.append(current_bullet.strip())

            # Start new bullet (remove bullet character)
            cleaned = line_stripped.lstrip('•-*○▪▫■□◦‣⁃●◉▸▹►▻⦿⦾ ')
            cleaned = re.sub(r'^\d+\.\s*', '', cleaned)  # Remove numbers
            current_bullet = cleaned
        else:
            # Continuation of previous bullet (multiline)
            if current_bullet and not detect_section(line):
                current_bullet += " " + line_stripped

    # Add last bullet
    if current_bullet:
        bullets.append(current_bullet.strip())

    # Filter out very short bullets (likely noise)
    bullets = [b for b in bullets if len(b) > 15]

    return bullets


def parse_sections(text: str) -> Dict[str, str]:
    """
    Parse resume into sections.

    Args:
        text: Full resume text

    Returns:
        Dictionary mapping section names to content

    Example:
        {
            "education": "UNIVERSITY OF CALIFORNIA...",
            "experience": "OPEN SOURCE...",
            "skills": "Languages & Frameworks: Python...",
            "projects": "Video Platform..."
        }
    """
    lines = text.split('\n')
    sections = {}
    current_section = SectionType.UNKNOWN
    current_content = []

    for line in lines:
        # Check if this is a section header
        section_type = detect_section(line)

        if section_type:
            # Save previous section
            if current_section != SectionType.UNKNOWN and current_content:
                sections[current_section.value] = '\n'.join(current_content)

            # Start new section
            current_section = section_type
            current_content = []
        else:
            # Add to current section
            if line.strip():
                current_content.append(line)

    # Save last section
    if current_section != SectionType.UNKNOWN and current_content:
        sections[current_section.value] = '\n'.join(current_content)

    return sections


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract skills from resume, preserving categorization.

    Skills are often formatted as:
        "Languages & Frameworks: Python, Java, JavaScript"
        "Backend & Databases: SQL, MongoDB, Redis"

    We preserve this structure!

    Args:
        text: Resume text (or skills section)

    Returns:
        Dict mapping category -> list of skills

    Example:
        {
            "Languages & Frameworks": ["Python", "Java", "JavaScript", "FastAPI"],
            "Backend & Databases": ["REST APIs", "SQL", "PostgreSQL", "MongoDB"],
            "Cloud & DevOps": ["Docker", "Git", "AWS", "GCP"]
        }
    """
    skills_by_category = {}

    # Find skills section
    sections = parse_sections(text)
    skills_section = sections.get('skills', '')

    if not skills_section:
        # No explicit skills section
        return {}

    # Parse each line
    for line in skills_section.split('\n'):
        line_stripped = line.strip()

        if not line_stripped or ':' not in line_stripped:
            continue

        # Split by first colon
        parts = line_stripped.split(':', 1)
        if len(parts) != 2:
            continue

        category = parts[0].strip()
        skills_str = parts[1].strip()

        # Split skills by comma
        skills = [s.strip() for s in skills_str.split(',') if s.strip()]

        if skills:
            skills_by_category[category] = skills

    return skills_by_category


def extract_experience_entries(text: str) -> List[Dict[str, Any]]:
    """
    Extract structured experience entries with company, title, dates, and bullets.
    Handles various formats:
    - Company | Location
    - Title | Date
    - Company    Location
    - Title    Date
    - Company (Location)
    """
    sections = parse_sections(text)
    experience_text = sections.get('experience', '')

    if not experience_text:
        return []

    entries = []
    lines = experience_text.split('\n')
    current_entry = None
    current_bullets = []

    # Date pattern: Month Year - Month Year, Present, etc.
    date_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}.*?(?:Present|Current|Now|\d{4}))'
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if not is_bullet_point(line):
            # Save previous entry
            if current_entry and current_bullets:
                current_entry['bullets'] = current_bullets
                entries.append(current_entry)

            # Start new entry
            # Strategy: 
            # 1. First line is usually Company + Location (or Title + Date)
            # 2. Second line is usually Title + Date (or Company + Location)
            
            # Helper to split line into left/right parts
            def split_line(text_line):
                # Try splitting by pipe or bullet char first
                if '|' in text_line:
                    parts = text_line.rsplit('|', 1)
                    return parts[0].strip(), parts[1].strip()
                if '•' in text_line:
                    parts = text_line.rsplit('•', 1)
                    return parts[0].strip(), parts[1].strip()
                if '   ' in text_line:  # 3+ spaces
                    parts = re.split(r'\s{3,}', text_line)
                    if len(parts) >= 2:
                        return parts[0].strip(), parts[-1].strip()
                
                # Check for date at end
                date_match = re.search(date_pattern, text_line, re.IGNORECASE)
                if date_match:
                    date_str = date_match.group(1)
                    # Make sure date is at the end
                    if text_line.endswith(date_str):
                        return text_line[:-len(date_str)].strip(' -|•,'), date_str
                
                # Check for common locations at end (Remote, City, State)
                loc_pattern = r'\b(Remote|CA|NY|TX|WA|USA|United States|[A-Z][a-z]+,\s*[A-Z]{2})$'
                loc_match = re.search(loc_pattern, text_line)
                if loc_match:
                     loc_str = loc_match.group(1)
                     if text_line.endswith(loc_str):
                         return text_line[:-len(loc_str)].strip(' -|•,'), loc_str

                return text_line, ""

            # Parse first line (Company/Location)
            part1, part2 = split_line(line)
            
            # Guess if part1 is company or title based on keywords
            # (Simple heuristic: Companies often capitalized, Titles have "Engineer", "Manager", etc.)
            
            company = part1
            location = part2
            title = ""
            date = ""

            # Check next line for Title/Date
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if not is_bullet_point(next_line) and next_line:
                    n_part1, n_part2 = split_line(next_line)
                    title = n_part1
                    date = n_part2
                    i += 1  # Consume next line

            # Swap if it looks like Title came first
            # Heuristic: Dates usually go with Title line
            if re.search(date_pattern, location, re.IGNORECASE) and not date:
                # First line had date, so it was probably Title | Date
                # Second line is likely Company | Location
                real_title = company
                real_date = location
                real_company = title
                real_location = date
                
                company = real_company
                location = real_location
                title = real_title
                date = real_date

            current_entry = {
                "company": company,
                "title": title,
                "date": date,
                "location": location,
            }
            current_bullets = []

        # It's a bullet
        elif is_bullet_point(line):
            # Clean bullet
            cleaned = line.strip().lstrip('•-*○▪▫■□◦‣⁃●◉▸▹►▻⦿⦾ ')
            cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
            if cleaned:  # Only add non-empty bullets
                current_bullets.append(cleaned)

        i += 1

    # Save last entry
    if current_entry and current_bullets:
        current_entry['bullets'] = current_bullets
        entries.append(current_entry)

    return entries


def extract_project_entries(text: str) -> List[Dict[str, Any]]:
    """
    Extract structured project entries.
    Handles formats:
    - Project Name | Tech Stack
    - Project Name - Tech Stack
    - Project Name (Tech Stack)
    - Project Name
    """
    sections = parse_sections(text)
    projects_text = sections.get('projects', '')

    if not projects_text:
        return []

    entries = []
    lines = projects_text.split('\n')
    current_entry = None
    current_bullets = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Check if this is a project header
        # Heuristic: Not a bullet, and either has separator OR is followed by bullets
        is_header = False
        
        if not is_bullet_point(line):
            # If it has a separator, it's definitely a header
            if '|' in line or ' – ' in line or ' - ' in line:
                is_header = True
            # If it's just text and next line is a bullet, it's likely a header
            elif i + 1 < len(lines) and is_bullet_point(lines[i+1]):
                is_header = True
            # If it's the very first line of the section, it's a header
            elif current_entry is None and not is_bullet_point(line):
                is_header = True

        if is_header:
            # Save previous entry
            if current_entry and current_bullets:
                current_entry['bullets'] = current_bullets
                entries.append(current_entry)

            # Parse project header
            name = line
            tech_stack = ""
            link = ""
            
            # Check for link at end
            link_match = re.search(r'(\(link\)|\[link\]|http[s]?://\S+|www\.\S+)$', line, re.IGNORECASE)
            if link_match:
                link = link_match.group(1)
                line = line[:-len(link)].strip()
                name = line # Update name to exclude link
            
            # Try to split by common separators
            for sep in ['|', ' – ', ' - ']:
                if sep in line:
                    parts = line.split(sep, 1)
                    name = parts[0].strip()
                    tech_stack = parts[1].strip()
                    break
            
            # Handle parentheses: "Project Name (Tech Stack)"
            if not tech_stack and '(' in name and name.endswith(')'):
                match = re.search(r'(.*?)\s*\((.*?)\)$', name)
                if match:
                    name = match.group(1).strip()
                    tech_stack = match.group(2).strip()

            current_entry = {
                "name": name,
                "tech_stack": tech_stack,
                "link": link
            }
            current_bullets = []

        # It's a bullet
        elif is_bullet_point(line):
            # Clean bullet
            cleaned = line.strip().lstrip('•-*○▪▫■□◦‣⁃●◉▸▹►▻⦿⦾ ')
            cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
            if cleaned:
                current_bullets.append(cleaned)

        i += 1

    # Save last entry
    if current_entry and current_bullets:
        current_entry['bullets'] = current_bullets
        entries.append(current_entry)

    return entries


def extract_education_entries(text: str) -> List[Dict[str, Any]]:
    """
    Extract structured education entries.
    Handles formats:
    - School | Location
    - Degree | Date
    - School    Location
    - Degree    Date
    """
    sections = parse_sections(text)
    education_text = sections.get('education', '')

    if not education_text:
        return []

    entries = []
    lines = education_text.split('\n')

    # Date pattern: Month Year - Month Year, Present, etc.
    # Also capture "Graduated" or "Expected" prefix
    date_pattern = r'((?:Graduated|Expected|Est\.?)?\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}.*?(?:Present|Current|Now|\d{4})?)'
    
    # Helper to split line
    def split_line(text_line):
        # Try splitting by pipe or bullet char first
        if '|' in text_line:
            parts = text_line.rsplit('|', 1)
            return parts[0].strip(), parts[1].strip()
        if '•' in text_line:
            parts = text_line.rsplit('•', 1)
            return parts[0].strip(), parts[1].strip()
        if '   ' in text_line:  # 3+ spaces
            parts = re.split(r'\s{3,}', text_line)
            if len(parts) >= 2:
                return parts[0].strip(), parts[-1].strip()
        
        # Check for date at end
        date_match = re.search(date_pattern, text_line, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(1)
            if text_line.endswith(date_str):
                return text_line[:-len(date_str)].strip(' -|•,'), date_str
        
        # Check for common locations at end
        # Allow multiple words for city (e.g. "La Jolla, CA", "New York, NY")
        loc_pattern = r'\b((?:[A-Z][a-z]+\s+)+[A-Z]{2}|(?:[A-Z][a-z]+\s*)+,\s*[A-Z]{2}|Remote|USA|United States)$'
        loc_match = re.search(loc_pattern, text_line)
        if loc_match:
                loc_str = loc_match.group(0) # Use group 0 to get full match
                if text_line.endswith(loc_str):
                    return text_line[:-len(loc_str)].strip(' -|•,'), loc_str

        return text_line, ""

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # School line (usually has location at end)
        school, location = split_line(line)

        # Next line is degree and date
        degree = ""
        year = ""
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line:
                degree, year = split_line(next_line)
                i += 1

        entries.append({
            "school": school,
            "degree": degree,
            "year": year,
            "location": location
        })

        i += 1

    return entries


def parse_resume_smart(text: str) -> Dict[str, Any]:
    """
    Smart resume parser that handles ANY format.

    This is the main parsing function!

    Args:
        text: Full resume text

    Returns:
        Structured resume data

    Example output:
        {
            "text": "full resume text...",
            "bullets": ["Built scalable backend...", "Developed and optimized..."],
            "sections": {
                "education": "UNIVERSITY OF CALIFORNIA...",
                "experience": "OPEN SOURCE...",
                "skills": "Languages & Frameworks...",
                "projects": "Video Platform..."
            },
            "contact_info": {
                "email": "rymao_@outlook.com",
                "phone": "(607)232-8826",
                "name": "Ryley Mao",
                "github": "github.com/ryleymao",
                "linkedin": "linkedin.com/in/ryley-mao",
                "website": "rymao.info"
            },
            "experience": [...],  # Structured entries
            "education": [...],   # Structured entries
            "skills": {"Languages & Frameworks": ["Python", ...]},
            "bullet_count": 15
        }
    """

    # Extract contact info
    contact = extract_contact_info(text)

    # Try to extract name from first few lines
    name = ""
    first_lines = text.split('\n')[:3]
    for line in first_lines:
        line_clean = line.strip()
        # Name is usually the first line, short, and has capital letters
        if line_clean and len(line_clean) < 50 and not '@' in line and not 'http' in line:
            # Check if it looks like a name (has spaces, mostly letters)
            words = line_clean.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                name = line_clean
                break

    # Parse sections
    sections = parse_sections(text)

    # Extract bullets (flat list)
    bullets = extract_bullets_from_text(text)

    # Extract structured experience
    experience = extract_experience_entries(text)

    # Extract structured projects
    projects = extract_project_entries(text)

    # Extract structured education
    education = extract_education_entries(text)

    # Extract skills
    skills = extract_skills(text)

    return {
        "text": text,
        "bullets": bullets,
        "bullet_count": len(bullets),
        "sections": sections,
        "contact_info": {
            "name": name,
            "email": contact.email,
            "phone": contact.phone,
            "github": contact.github,
            "linkedin": contact.linkedin,
            "website": contact.website,
            "location": contact.location
        },
        "experience": experience,  # Structured experience entries
        "projects": projects,       # NEW: Structured project entries
        "education": education,     # Structured education entries
        "skills": skills,
        "has_education": 'education' in sections,
        "has_experience": 'experience' in sections,
        "has_projects": 'projects' in sections
    }


# Example usage
if __name__ == "__main__":
    # Test with Ryley's resume
    sample_text = """
Ryley Mao
rymao_@outlook.com | (607)232-8826 | github.com/ryleymao | linkedin.com/in/ryley-mao | rymao.info

EDUCATION
UNIVERSITY OF CALIFORNIA, SAN DIEGO    La Jolla, CA
B.S. in Mathematics-Computer Science    Graduated Sep 2025

SKILLS
Languages & Frameworks: Python, Java, JavaScript, FastAPI, Node.js, Express.js, Next.js, React
Backend & Databases: REST APIs, Async Services, Microservices, SQL (PostgreSQL), NoSQL (MongoDB, Redis), Kafka

EXPERIENCE
OPEN SOURCE    Remote
Software Engineer     Sep 2025 – Nov 2025
Built scalable backend APIs and authentication systems using Python + FastAPI, improving performance for 1k+ users.
Developed and optimized automated test suites and CI/CD workflows, reducing pipeline runtime by 35%.
"""

    result = parse_resume_smart(sample_text)

    print(f"Bullets found: {result['bullet_count']}")
    print("\nBullets:")
    for i, bullet in enumerate(result['bullets'][:3], 1):
        print(f"{i}. {bullet}")

    print(f"\nContact: {result['contact_info']}")
    print(f"\nSkills: {result['skills'][:5]}")
