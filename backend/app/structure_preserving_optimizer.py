"""
Structure-Preserving Resume Optimizer

CRITICAL RULES:
1. Output length ≤ Input length (can only remove, not add bullets)
2. Preserve hard-coded info (company names, dates, locations, education)
3. Only optimize: bullet points and skills
4. Skills are NOT bullets (comma-separated, categorized)

Example:
    INPUT:
        OPEN SOURCE    Remote
        Software Engineer     Sep 2025 – Nov 2025
        • Bullet 1
        • Bullet 2
        • Bullet 3

    OUTPUT:
        OPEN SOURCE    Remote              ← PRESERVED (hard-coded)
        Software Engineer     Sep 2025 – Nov 2025  ← PRESERVED
        • Best bullet (high score)         ← REORDERED
        • Second best bullet               ← REORDERED
        • Third best bullet                ← REORDERED (same count!)
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import re


@dataclass
class ResumeSection:
    """
    Represents a section of the resume.
    """
    type: str  # "experience", "education", "skills", "projects"
    header: str  # "EXPERIENCE", "EDUCATION", etc.
    content: List[str]  # Lines of content
    bullets: List[str]  # Extracted bullet points
    hard_coded: List[str]  # Company names, dates, locations (preserve these!)


def detect_hard_coded_lines(lines: List[str]) -> List[str]:
    """
    Detect lines that should NEVER be changed.

    Hard-coded lines include:
    - Company names (all caps, or followed by location)
    - Job titles
    - Dates (Sep 2025, 2020-2023, etc.)
    - Locations (Remote, San Francisco, CA, etc.)
    - Degree names (B.S., M.S., etc.)
    - University names

    Args:
        lines: List of text lines

    Returns:
        List of lines that are hard-coded (preserve exactly)
    """
    hard_coded = []

    for line in lines:
        line_stripped = line.strip()

        if not line_stripped:
            continue

        # Pattern 1: Company name + Location
        # Example: "OPEN SOURCE    Remote"
        # Example: "JPMORGAN CHASE (FORAGE)         Remote"
        if re.search(r'\b(Remote|[A-Z][a-z]+,\s*[A-Z]{2})\s*$', line_stripped):
            hard_coded.append(line)
            continue

        # Pattern 2: Job title + Date range
        # Example: "Software Engineer     Sep 2025 – Nov 2025"
        if re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}', line_stripped):
            hard_coded.append(line)
            continue

        # Pattern 3: Dates only
        # Example: "2020 - 2023"
        # Example: "Graduated Sep 2025"
        if re.search(r'\b(20\d{2}|19\d{2})\b', line_stripped):
            hard_coded.append(line)
            continue

        # Pattern 4: University names (usually contain "University", "College", "Institute")
        if re.search(r'\b(UNIVERSITY|University|COLLEGE|College|INSTITUTE|Institute)\b', line_stripped):
            hard_coded.append(line)
            continue

        # Pattern 5: Degree names
        # Example: "B.S. in Mathematics-Computer Science"
        if re.search(r'\b(B\.S\.|M\.S\.|Ph\.D\.|B\.A\.|M\.A\.|MBA)\b', line_stripped):
            hard_coded.append(line)
            continue

        # Pattern 6: All caps lines (likely company names or section headers)
        # Example: "JPMORGAN CHASE"
        if line_stripped.isupper() and len(line_stripped.split()) <= 5:
            hard_coded.append(line)
            continue

    return hard_coded


def parse_experience_entry(lines: List[str]) -> Dict[str, Any]:
    """
    Parse a single experience entry.

    Example input:
        OPEN SOURCE    Remote
        Software Engineer     Sep 2025 – Nov 2025
        Built scalable backend APIs...
        Developed and optimized...
        Refactored and maintained...

    Output:
        {
            "company_line": "OPEN SOURCE    Remote",
            "title_line": "Software Engineer     Sep 2025 – Nov 2025",
            "bullets": [
                "Built scalable backend APIs...",
                "Developed and optimized...",
                "Refactored and maintained..."
            ],
            "original_bullet_count": 3
        }
    """
    hard_coded_lines = []
    bullets = []

    for line in lines:
        if not line.strip():
            continue

        # Check if hard-coded
        if is_hard_coded_line(line):
            hard_coded_lines.append(line)
        else:
            # It's a bullet
            bullets.append(line.strip())

    return {
        "hard_coded_lines": hard_coded_lines,
        "bullets": bullets,
        "original_bullet_count": len(bullets)
    }


def is_hard_coded_line(line: str) -> bool:
    """Check if a single line is hard-coded (should not be modified)"""
    line_stripped = line.strip()

    if not line_stripped:
        return False

    # All caps (company names)
    if line_stripped.isupper():
        return True

    # Contains dates
    if re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}', line_stripped):
        return True

    if re.search(r'\b(20\d{2}|19\d{2})\b', line_stripped):
        return True

    # Contains location indicators
    if re.search(r'\b(Remote|[A-Z][a-z]+,\s*[A-Z]{2})\s*$', line_stripped):
        return True

    # University/College
    if re.search(r'\b(UNIVERSITY|University|COLLEGE|College)\b', line_stripped):
        return True

    # Degree
    if re.search(r'\b(B\.S\.|M\.S\.|Ph\.D\.|B\.A\.|M\.A\.|MBA)\b', line_stripped):
        return True

    return False


def optimize_bullets_with_length_constraint(
    original_bullets: List[str],
    scored_bullets: List[Dict[str, Any]],
    max_bullets: int
) -> List[str]:
    """
    Optimize bullets while respecting length constraint.

    RULE: Output length ≤ Input length

    Args:
        original_bullets: Original bullets from resume
        scored_bullets: Bullets with semantic scores
        max_bullets: Maximum number of bullets (from original)

    Returns:
        Reordered bullets (same or fewer than original)

    Example:
        original_bullets = 5 bullets
        scored_bullets = [bullet1 (0.9), bullet2 (0.8), bullet3 (0.3), ...]

        Output: Top 5 bullets by score (same count as original!)
    """
    # Sort by score (highest first)
    sorted_bullets = sorted(scored_bullets, key=lambda x: x['score'], reverse=True)

    # Take top N (where N = original count)
    optimized = sorted_bullets[:max_bullets]

    # Return just the bullet texts
    return [b['bullet'] for b in optimized]


def optimize_skills_section(
    skills_section: str,
    job_keywords: List[str]
) -> str:
    """
    Optimize skills section by reordering skill categories.

    Skills are typically formatted as:
        "Languages & Frameworks: Python, Java, JavaScript, FastAPI"
        "Backend & Databases: REST APIs, SQL, MongoDB"

    We want to:
    1. Keep the same format (category: skills)
    2. Reorder categories based on job relevance
    3. Within each category, prioritize relevant skills

    Args:
        skills_section: Original skills section text
        job_keywords: Keywords from job description

    Returns:
        Optimized skills section (same format, reordered)

    Example:
        Input:
            "Languages: Python, Java, C++
             Databases: MongoDB, PostgreSQL
             Cloud: AWS, Azure"

        Job: "Backend Engineer - Python, MongoDB, AWS"

        Output:
            "Languages: Python, Java, C++  ← Python matches!
             Cloud: AWS, Azure              ← AWS matches! (moved up)
             Databases: MongoDB, PostgreSQL ← MongoDB matches!"
    """
    lines = skills_section.split('\n')
    categories = []

    # Parse each category
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or ':' not in line_stripped:
            continue

        # Split category and skills
        parts = line_stripped.split(':', 1)
        category_name = parts[0].strip()
        skills_str = parts[1].strip()

        # Split skills by comma
        skills = [s.strip() for s in skills_str.split(',')]

        # Score this category by counting keyword matches
        matches = sum(
            1 for skill in skills
            for keyword in job_keywords
            if keyword.lower() in skill.lower()
        )

        categories.append({
            'category': category_name,
            'skills': skills,
            'original_line': line_stripped,
            'match_score': matches
        })

    # Sort categories by match score (highest first)
    categories.sort(key=lambda x: x['match_score'], reverse=True)

    # Reconstruct skills section
    optimized_lines = []
    for cat in categories:
        # Within each category, prioritize matching skills
        prioritized_skills = []
        other_skills = []

        for skill in cat['skills']:
            if any(keyword.lower() in skill.lower() for keyword in job_keywords):
                prioritized_skills.append(skill)
            else:
                other_skills.append(skill)

        # Combine: matching skills first, then others
        all_skills = prioritized_skills + other_skills

        # Reconstruct line
        optimized_lines.append(f"{cat['category']}: {', '.join(all_skills)}")

    return '\n'.join(optimized_lines)


def reconstruct_resume(
    original_text: str,
    optimized_bullets: Dict[str, List[str]],
    optimized_skills: str
) -> str:
    """
    Reconstruct the resume with optimized bullets and skills.

    PRESERVES:
    - All hard-coded lines (company, dates, locations, education)
    - Section headers
    - Formatting (indentation, spacing)
    - Order of sections

    CHANGES:
    - Order of bullets within each experience/project
    - Order of skills categories

    Args:
        original_text: Original resume text
        optimized_bullets: Map of section -> optimized bullets
        optimized_skills: Optimized skills section

    Returns:
        Optimized resume text
    """
    lines = original_text.split('\n')
    output_lines = []

    current_section = None
    bullet_index = 0

    for line in lines:
        line_stripped = line.strip()

        # Check if this is a section header
        if line_stripped.upper() in ['EXPERIENCE', 'PROJECTS', 'SKILLS', 'EDUCATION']:
            current_section = line_stripped.lower()
            output_lines.append(line)
            bullet_index = 0
            continue

        # If in SKILLS section, use optimized skills
        if current_section == 'skills' and ':' in line_stripped:
            if bullet_index == 0:
                # First skills line - output entire optimized section
                output_lines.append(optimized_skills)
                bullet_index += 1
            # Skip remaining original skills lines
            continue

        # If hard-coded line, preserve exactly
        if is_hard_coded_line(line):
            output_lines.append(line)
            bullet_index = 0
            continue

        # If bullet point
        if current_section in optimized_bullets:
            bullets = optimized_bullets[current_section]
            if bullet_index < len(bullets):
                # Use optimized bullet (preserve original indentation)
                indent = len(line) - len(line.lstrip())
                output_lines.append(' ' * indent + bullets[bullet_index])
                bullet_index += 1
            # Skip if we've used all optimized bullets (length constraint!)
            continue

        # Otherwise, preserve line as-is
        output_lines.append(line)

    return '\n'.join(output_lines)


def get_original_bullet_counts(parsed_resume: Dict[str, Any]) -> Dict[str, int]:
    """
    Get the original bullet count for each section.

    This enforces the length constraint: output ≤ input

    Args:
        parsed_resume: Parsed resume data

    Returns:
        Dict mapping section -> bullet count

    Example:
        {
            "experience": 7,  # 7 bullets in experience section
            "projects": 10,   # 10 bullets in projects section
        }
    """
    sections = parsed_resume.get('sections', {})
    bullet_counts = {}

    for section_name, section_text in sections.items():
        if section_name in ['experience', 'projects']:
            # Count bullets in this section
            lines = section_text.split('\n')
            count = sum(1 for line in lines if line.strip() and not is_hard_coded_line(line))
            bullet_counts[section_name] = count

    return bullet_counts
