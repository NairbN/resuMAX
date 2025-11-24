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

    # Website (look for common TLDs)
    website_match = re.search(r'\b([a-z0-9-]+\.(com|net|org|io|dev|info|tech))\b', text, re.IGNORECASE)
    if website_match and website_match.group() not in [contact.email, contact.linkedin, contact.github]:
        contact.website = website_match.group()

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

    # Bullet characters
    bullet_chars = ['•', '-', '*', '○', '▪', '▫', '■', '□', '◦', '‣', '⁃']
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
            cleaned = line_stripped.lstrip('•-*○▪▫■□◦‣⁃ ')
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
                "github": "github.com/ryleymao",
                "linkedin": "linkedin.com/in/ryley-mao",
                "website": "rymao.info"
            },
            "skills": ["Python", "Java", "JavaScript", ...],
            "bullet_count": 15
        }
    """

    # Extract contact info
    contact = extract_contact_info(text)

    # Parse sections
    sections = parse_sections(text)

    # Extract bullets
    bullets = extract_bullets_from_text(text)

    # Extract skills
    skills = extract_skills(text)

    return {
        "text": text,
        "bullets": bullets,
        "bullet_count": len(bullets),
        "sections": sections,
        "contact_info": {
            "email": contact.email,
            "phone": contact.phone,
            "github": contact.github,
            "linkedin": contact.linkedin,
            "website": contact.website
        },
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
