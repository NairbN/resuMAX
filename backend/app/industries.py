"""
Industry-Specific Skills and Configuration

Maintains dictionaries of skills, keywords, and scoring weights per industry.
This makes the optimizer universal across careers.
"""

from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class IndustryConfig:
    """Configuration for industry-specific optimization"""
    name: str
    skills: Set[str]
    soft_skills: Set[str]
    certifications: Set[str]
    synonyms: Dict[str, List[str]]  # Map canonical term to variations
    scoring_weights: Dict[str, float]
    section_priority: List[str]  # Preferred section order


# ========================================
# INDUSTRY SKILL DICTIONARIES
# ========================================

TECH_SKILLS = {
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "matlab",

    # Web Frameworks
    "react", "angular", "vue", "svelte", "next.js", "nuxt", "django", "flask",
    "fastapi", "express", "node.js", "spring", "asp.net",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "dynamodb", "firestore", "cassandra", "oracle",

    # Cloud & DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "circleci", "github actions", "ci/cd",

    # Data Science / ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "spark", "hadoop", "airflow",

    # Other
    "git", "api", "rest", "graphql", "microservices", "agile", "scrum"
}

FINANCE_SKILLS = {
    # Tools & Software
    "excel", "vba", "powerpoint", "tableau", "power bi", "bloomberg terminal",
    "factset", "capital iq", "refinitiv", "quickbooks",

    # Analysis & Modeling
    "financial modeling", "dcf", "lbo", "valuation", "forecasting",
    "budgeting", "variance analysis", "sensitivity analysis",

    # Accounting
    "gaap", "ifrs", "financial statements", "balance sheet", "income statement",
    "cash flow", "reconciliation", "journal entries", "accounts payable",
    "accounts receivable",

    # Investment
    "portfolio management", "asset allocation", "risk management",
    "derivatives", "fixed income", "equity research", "trading",

    # Certifications
    "cfa", "cpa", "frm", "series 7", "series 63"
}

HEALTHCARE_SKILLS = {
    # Clinical
    "patient care", "clinical assessment", "vital signs", "medication administration",
    "wound care", "iv therapy", "phlebotomy", "catheterization",

    # Systems & Compliance
    "ehr", "emr", "epic", "cerner", "meditech", "hipaa", "osha",
    "infection control", "quality assurance",

    # Specialties
    "emergency medicine", "pediatrics", "oncology", "cardiology",
    "surgery", "radiology", "laboratory", "pharmacy",

    # Certifications
    "rn", "lpn", "cna", "bls", "acls", "pals", "nrp"
}

DESIGN_SKILLS = {
    # Tools
    "figma", "sketch", "adobe xd", "invision", "photoshop", "illustrator",
    "after effects", "indesign", "blender", "cinema 4d",

    # Design Types
    "ui design", "ux design", "product design", "graphic design",
    "web design", "mobile design", "motion design", "3d design",

    # Processes
    "wireframing", "prototyping", "user research", "usability testing",
    "design systems", "style guides", "responsive design", "accessibility",

    # Skills
    "typography", "color theory", "layout", "branding", "visual design"
}

MARKETING_SKILLS = {
    # Digital Marketing
    "seo", "sem", "ppc", "google ads", "facebook ads", "instagram ads",
    "email marketing", "content marketing", "social media marketing",

    # Analytics
    "google analytics", "ga4", "mixpanel", "amplitude", "tableau",
    "data analysis", "a/b testing", "conversion optimization",

    # Tools
    "hubspot", "salesforce", "marketo", "mailchimp", "hootsuite",
    "buffer", "canva", "wordpress",

    # Strategy
    "brand strategy", "go-to-market", "customer acquisition",
    "growth hacking", "marketing automation", "crm"
}

SALES_SKILLS = {
    # Sales Process
    "prospecting", "cold calling", "lead generation", "pipeline management",
    "closing", "negotiation", "account management", "upselling", "cross-selling",

    # CRM & Tools
    "salesforce", "hubspot", "pipedrive", "zoho", "outreach", "salesloft",

    # Sales Types
    "b2b sales", "b2c sales", "saas sales", "enterprise sales",
    "inside sales", "outside sales", "consultative selling",

    # Metrics
    "quota attainment", "revenue generation", "conversion rate",
    "sales cycle", "customer retention"
}

# ========================================
# UNIVERSAL SOFT SKILLS (ALL INDUSTRIES)
# ========================================

SOFT_SKILLS = {
    "leadership", "communication", "teamwork", "collaboration",
    "problem solving", "critical thinking", "time management",
    "project management", "stakeholder management", "presentation",
    "analytical", "detail-oriented", "strategic thinking", "adaptability",
    "mentorship", "coaching", "conflict resolution"
}

# ========================================
# SYNONYM MAPPING
# ========================================

TECH_SYNONYMS = {
    "javascript": ["js", "javascript", "ecmascript"],
    "typescript": ["ts", "typescript"],
    "python": ["python", "py"],
    "aws": ["amazon web services", "aws"],
    "gcp": ["google cloud platform", "gcp", "google cloud"],
    "kubernetes": ["k8s", "kubernetes"],
    "machine learning": ["ml", "machine learning"],
    "artificial intelligence": ["ai", "artificial intelligence"],
    "ci/cd": ["continuous integration", "continuous deployment", "ci/cd", "cicd"],
}

FINANCE_SYNONYMS = {
    "excel": ["microsoft excel", "excel", "spreadsheet"],
    "financial modeling": ["financial model", "financial modeling", "modeling"],
    "gaap": ["generally accepted accounting principles", "gaap"],
    "cfa": ["chartered financial analyst", "cfa"],
    "portfolio management": ["portfolio mgmt", "portfolio management", "pm"]
}

HEALTHCARE_SYNONYMS = {
    "ehr": ["electronic health record", "ehr", "electronic medical record", "emr"],
    "hipaa": ["health insurance portability and accountability act", "hipaa"],
    "patient care": ["patient care", "clinical care", "bedside care"],
    "medication administration": ["med admin", "medication administration", "drug administration"]
}

DESIGN_SYNONYMS = {
    "ui": ["user interface", "ui"],
    "ux": ["user experience", "ux"],
    "figma": ["figma"],
    "photoshop": ["adobe photoshop", "photoshop", "ps"]
}

# ========================================
# INDUSTRY SCORING WEIGHTS
# ========================================

TECH_WEIGHTS = {
    "skills": 1.0,          # Technical skills are crucial
    "keywords": 0.5,        # General keywords
    "action_verbs": 0.5,    # Action verbs important
    "numbers": 0.4,         # Metrics very important (scale, performance)
    "soft_skills": 0.3,     # Less weight on soft skills
    "certifications": 0.6,  # Certifications matter
}

FINANCE_WEIGHTS = {
    "skills": 1.0,          # Tools and methods critical
    "keywords": 0.4,
    "action_verbs": 0.4,
    "numbers": 0.7,         # Numbers are KING in finance (ROI, revenue, etc.)
    "soft_skills": 0.4,     # Presentation and leadership matter
    "certifications": 0.8,  # CFA, CPA very important
}

HEALTHCARE_WEIGHTS = {
    "skills": 1.0,          # Clinical skills essential
    "keywords": 0.4,
    "action_verbs": 0.4,
    "numbers": 0.5,         # Patient outcomes, but not as emphasized
    "soft_skills": 0.6,     # Patient care, teamwork critical
    "certifications": 0.9,  # Licenses/certs absolutely critical
}

DESIGN_WEIGHTS = {
    "skills": 1.0,          # Tools (Figma, Photoshop)
    "keywords": 0.4,
    "action_verbs": 0.3,    # Less emphasis on "managed, led"
    "numbers": 0.2,         # Design is more qualitative
    "soft_skills": 0.5,     # Collaboration, communication
    "certifications": 0.3,  # Less common in design
}

MARKETING_WEIGHTS = {
    "skills": 1.0,          # SEO, analytics tools
    "keywords": 0.5,
    "action_verbs": 0.5,    # "Drove growth", "launched campaign"
    "numbers": 0.7,         # Conversion rates, ROI critical
    "soft_skills": 0.5,     # Creativity, communication
    "certifications": 0.4,  # Google Ads cert, etc.
}

SALES_WEIGHTS = {
    "skills": 0.8,          # CRM tools
    "keywords": 0.4,
    "action_verbs": 0.6,    # "Closed deals", "exceeded quota"
    "numbers": 0.9,         # Revenue, quota attainment MOST important
    "soft_skills": 0.7,     # Communication, negotiation crucial
    "certifications": 0.3,  # Less common
}

# ========================================
# SECTION PRIORITY (ORDER OF SECTIONS)
# ========================================

TECH_SECTION_PRIORITY = [
    "skills",
    "experience",
    "projects",
    "education",
    "certifications"
]

FINANCE_SECTION_PRIORITY = [
    "experience",
    "education",
    "certifications",
    "skills"
]

HEALTHCARE_SECTION_PRIORITY = [
    "licenses",
    "certifications",
    "experience",
    "education",
    "skills"
]

DESIGN_SECTION_PRIORITY = [
    "portfolio",
    "experience",
    "skills",
    "education"
]

# ========================================
# INDUSTRY CONFIGURATIONS
# ========================================

INDUSTRIES: Dict[str, IndustryConfig] = {
    "tech": IndustryConfig(
        name="Technology & Software",
        skills=TECH_SKILLS,
        soft_skills=SOFT_SKILLS,
        certifications={"aws certified", "gcp certified", "azure certified", "cissp", "ceh"},
        synonyms=TECH_SYNONYMS,
        scoring_weights=TECH_WEIGHTS,
        section_priority=TECH_SECTION_PRIORITY
    ),
    "finance": IndustryConfig(
        name="Finance & Accounting",
        skills=FINANCE_SKILLS,
        soft_skills=SOFT_SKILLS,
        certifications={"cfa", "cpa", "frm", "cma"},
        synonyms=FINANCE_SYNONYMS,
        scoring_weights=FINANCE_WEIGHTS,
        section_priority=FINANCE_SECTION_PRIORITY
    ),
    "healthcare": IndustryConfig(
        name="Healthcare & Medical",
        skills=HEALTHCARE_SKILLS,
        soft_skills=SOFT_SKILLS,
        certifications={"rn", "lpn", "md", "do", "pa", "np", "bls", "acls"},
        synonyms=HEALTHCARE_SYNONYMS,
        scoring_weights=HEALTHCARE_WEIGHTS,
        section_priority=HEALTHCARE_SECTION_PRIORITY
    ),
    "design": IndustryConfig(
        name="Design & Creative",
        skills=DESIGN_SKILLS,
        soft_skills=SOFT_SKILLS,
        certifications=set(),
        synonyms=DESIGN_SYNONYMS,
        scoring_weights=DESIGN_WEIGHTS,
        section_priority=DESIGN_SECTION_PRIORITY
    ),
    "marketing": IndustryConfig(
        name="Marketing & Growth",
        skills=MARKETING_SKILLS,
        soft_skills=SOFT_SKILLS,
        certifications={"google ads certified", "hubspot certified", "facebook blueprint"},
        synonyms={},
        scoring_weights=MARKETING_WEIGHTS,
        section_priority=["experience", "skills", "education"]
    ),
    "sales": IndustryConfig(
        name="Sales & Business Development",
        skills=SALES_SKILLS,
        soft_skills=SOFT_SKILLS,
        certifications=set(),
        synonyms={},
        scoring_weights=SALES_WEIGHTS,
        section_priority=["experience", "achievements", "skills", "education"]
    ),
}


def detect_industry(job_description: str) -> str:
    """
    Auto-detect industry from job description.

    Counts skill matches per industry and returns the best match.

    Args:
        job_description: Job description text

    Returns:
        Industry key (e.g., "tech", "finance", "healthcare")
    """
    job_lower = job_description.lower()

    scores = {}
    for industry_key, config in INDUSTRIES.items():
        # Count skill matches
        matches = sum(1 for skill in config.skills if skill in job_lower)
        scores[industry_key] = matches

    # Return industry with most matches (default to tech)
    return max(scores, key=scores.get) if scores else "tech"


def get_industry_config(industry: str = None, job_description: str = None) -> IndustryConfig:
    """
    Get industry configuration.

    Args:
        industry: Industry key (optional, will auto-detect if not provided)
        job_description: Job description for auto-detection

    Returns:
        IndustryConfig object
    """
    if not industry and job_description:
        industry = detect_industry(job_description)

    return INDUSTRIES.get(industry, INDUSTRIES["tech"])


def expand_keyword_with_synonyms(keyword: str, synonyms: Dict[str, List[str]]) -> Set[str]:
    """
    Expand a keyword to include all its synonyms.

    Args:
        keyword: Original keyword
        synonyms: Synonym mapping

    Returns:
        Set of keyword + all synonyms

    Example:
        expand_keyword_with_synonyms("javascript", TECH_SYNONYMS)
        → {"javascript", "js", "ecmascript"}
    """
    keyword_lower = keyword.lower()

    # Check if keyword is a canonical term
    if keyword_lower in synonyms:
        return set(synonyms[keyword_lower])

    # Check if keyword is a synonym of a canonical term
    for canonical, variants in synonyms.items():
        if keyword_lower in [v.lower() for v in variants]:
            return set(variants)

    # No synonyms found, return original
    return {keyword_lower}
