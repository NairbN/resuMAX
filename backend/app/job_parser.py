"""
Job Description Parser Module

Extracts keywords, skills, and requirements from job descriptions.
"""

from typing import List, Dict, Set
import re


def parse_job_description(job_text: str) -> Dict[str, any]:
    """
    Parse job description and extract relevant keywords and requirements.

    Args:
        job_text: Job description text

    Returns:
        Dictionary with:
            - keywords: List of important keywords
            - skills: List of technical skills
            - requirements: List of requirements
            - action_verbs: List of action verbs (led, managed, developed, etc.)

    TODO: Enhance with NLP using spaCy:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(job_text)
        # Extract entities (SKILLS, ORG, PRODUCT)
        # Extract noun phrases for key concepts
        # Use dependency parsing to find requirements
    """

    # Clean the text
    clean_text = job_text.lower().strip()

    # Extract keywords using simple heuristics (TODO: improve with NLP)
    keywords = extract_keywords(clean_text)

    # Extract technical skills
    skills = extract_skills(clean_text)

    # Extract action verbs
    action_verbs = extract_action_verbs(clean_text)

    # Extract requirements
    requirements = extract_requirements(job_text)

    return {
        "keywords": list(keywords),
        "skills": list(skills),
        "action_verbs": list(action_verbs),
        "requirements": requirements,
        "raw_text": job_text
    }


def extract_keywords(text: str) -> Set[str]:
    """
    Extract important keywords from job description.

    TODO: Implement TF-IDF or use spaCy for better keyword extraction
    """

    # Simple keyword extraction (replace with TF-IDF later)
    words = re.findall(r'\b\w+\b', text)

    # Filter out common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }

    keywords = {word for word in words if len(word) > 3 and word not in stop_words}

    return keywords


def extract_skills(text: str) -> Set[str]:
    """
    Extract technical skills from job description.

    TODO: Build comprehensive skills database or use pre-trained NER model
    """

    # Common technical skills to look for
    skill_patterns = [
        # Programming languages
        r'\bpython\b', r'\bjava\b', r'\bjavascript\b', r'\btypescript\b',
        r'\bc\+\+\b', r'\bc#\b', r'\bruby\b', r'\bgo\b', r'\brust\b', r'\bphp\b',
        r'\bswift\b', r'\bkotlin\b', r'\bscala\b',

        # Web frameworks
        r'\breact\b', r'\bangular\b', r'\bvue\b', r'\bdjango\b', r'\bflask\b',
        r'\bfastapi\b', r'\bnode\.?js\b', r'\bexpress\b', r'\bnext\.?js\b',

        # Databases
        r'\bsql\b', r'\bmysql\b', r'\bpostgresql\b', r'\bmongodb\b',
        r'\bredis\b', r'\belasticsearch\b', r'\bdynamodb\b', r'\bfirestore\b',

        # Cloud platforms
        r'\baws\b', r'\bgcp\b', r'\bazure\b', r'\bcloud\b', r'\bkubernetes\b',
        r'\bdocker\b', r'\bterraform\b',

        # Data science / ML
        r'\bmachine learning\b', r'\bdeep learning\b', r'\btensorflow\b',
        r'\bpytorch\b', r'\bscikit-learn\b', r'\bpandas\b', r'\bnumpy\b',

        # Other
        r'\bgit\b', r'\bapi\b', r'\brest\b', r'\bgraphql\b', r'\bagile\b',
        r'\bscrum\b', r'\bci/cd\b', r'\bdevops\b'
    ]

    skills = set()
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        skills.update(match.lower() for match in matches)

    return skills


def extract_action_verbs(text: str) -> Set[str]:
    """
    Extract action verbs commonly found in job descriptions.

    These are useful for rewriting resume bullets to match job language.
    """

    action_verbs = {
        'develop', 'build', 'create', 'design', 'implement', 'manage',
        'lead', 'coordinate', 'execute', 'deliver', 'optimize', 'improve',
        'analyze', 'evaluate', 'research', 'investigate', 'collaborate',
        'communicate', 'present', 'mentor', 'train', 'guide', 'support',
        'maintain', 'troubleshoot', 'debug', 'test', 'deploy', 'launch',
        'scale', 'architect', 'engineer', 'automate', 'streamline'
    }

    found_verbs = set()
    words = re.findall(r'\b\w+\b', text.lower())

    for word in words:
        if word in action_verbs:
            found_verbs.add(word)

    return found_verbs


def extract_requirements(text: str) -> List[str]:
    """
    Extract specific requirements from job description.

    Look for sections like:
        - "Requirements:", "Qualifications:", "Must have:"
        - Bullet points under these sections
        - Years of experience mentioned
    """

    requirements = []

    # Split into lines
    lines = text.split('\n')

    in_requirements_section = False

    for line in lines:
        line = line.strip()

        # Check if we're entering a requirements section
        if any(keyword in line.lower() for keyword in [
            'requirement', 'qualification', 'must have', 'responsibilities',
            'you will', 'we are looking for', 'ideal candidate'
        ]):
            in_requirements_section = True
            continue

        # Check if we're leaving the section
        if in_requirements_section and line and not line[0].isspace() and ':' in line:
            in_requirements_section = False

        # If in requirements section, extract bullets
        if in_requirements_section and line:
            # Remove bullet characters
            cleaned = line.lstrip('•-*○▪▫■□ ')
            if cleaned and len(cleaned) > 10:  # Ignore very short lines
                requirements.append(cleaned)

    return requirements
