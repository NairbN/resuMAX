"""
Resume Optimizer Module

Uses SEMANTIC SIMILARITY (embeddings) to score and reorder resume bullets.
Goes beyond keyword matching to understand meaning and context.
"""

from typing import Dict, List, Tuple, Any
import re

# Import our semantic matcher and industry configs
from app.semantic_matcher import get_semantic_matcher
from app.industries import get_industry_config, detect_industry
from app.bullet_classifier import classify_bullets, balance_categories


def optimize_resume(
    parsed_resume: Dict[str, Any],
    job_keywords: Dict[str, Any],
    original_content: bytes,
    content_type: str,
    industry: str = None
) -> Tuple[bytes, Dict[str, Any]]:
    """
    Optimize resume using SEMANTIC SIMILARITY (not just keywords!).

    This is the CORE algorithm:
    1. Use sentence embeddings to compute true similarity
    2. Score bullets based on meaning, not just word matches
    3. Reorder bullets (most relevant first)
    4. Calculate before/after improvement score

    Args:
        parsed_resume: Parsed resume data
        job_keywords: Job description data (includes raw_text)
        original_content: Original resume file
        content_type: MIME type
        industry: Industry type (auto-detect if None)

    Returns:
        Tuple of (optimized_pdf, scores_with_comparison)
    """

    # Extract data
    bullets = parsed_resume.get("bullets", [])
    resume_text = parsed_resume.get("text", "")
    job_description = job_keywords.get("raw_text", "")

    # Auto-detect industry if not provided
    if not industry:
        industry = detect_industry(job_description)

    # Get industry config
    industry_config = get_industry_config(industry, job_description)

    # === STEP 1: Semantic Matching (THE KEY INNOVATION!) ===
    matcher = get_semantic_matcher()

    # Compute semantic similarity for each bullet
    semantic_results = matcher.compute_similarity(bullets, job_description)

    # === STEP 2: Classify bullets into categories ===
    categorized = classify_bullets(bullets)

    # === STEP 3: Enforce Length Constraint ===
    # CRITICAL: Output length ≤ Input length (can only reorder, not add!)
    original_bullet_count = len(bullets)

    # === STEP 4: Balance categories and select top bullets ===
    # But limit to original count!
    balanced_bullets = balance_categories(categorized, max_bullets=original_bullet_count)

    # === STEP 5: Reorder balanced bullets by semantic score ===
    # Create a score map
    score_map = {item["bullet"]: item["score"] for item in semantic_results}

    # Sort balanced bullets by semantic score (highest first)
    optimized_bullets = sorted(
        balanced_bullets,
        key=lambda b: score_map.get(b, 0),
        reverse=True
    )

    # Ensure we don't exceed original length
    optimized_bullets = optimized_bullets[:original_bullet_count]

    # === STEP 5: Calculate before/after comparison ===
    comparison = matcher.compare_before_after(
        original_bullets=bullets,
        optimized_bullets=optimized_bullets,
        job_description=job_description
    )

    # === STEP 6: Get improvement suggestions ===
    suggestions = matcher.suggest_improvements(bullets, job_description)

    # === STEP 7: Calculate overall resume-job match ===
    overall_score = matcher.compute_overall_score(resume_text, job_description)

    # === STEP 8: Generate new PDF ===
    optimized_pdf = generate_optimized_pdf(
        parsed_resume=parsed_resume,
        optimized_bullets=optimized_bullets,
        original_content=original_content
    )

    # === STEP 9: Return results ===
    scores = {
        # Overall metrics
        "overall_score": round(overall_score, 1),
        "industry": industry,
        "industry_name": industry_config.name,

        # Before/After comparison
        "comparison": comparison,

        # Top bullets with scores
        "top_bullets": [
            {
                "text": item["bullet"],
                "score": round(item["score"] * 100, 1),  # Convert to percentage
                "rank": item["rank"]
            }
            for item in semantic_results[:10]
        ],

        # Suggestions
        "suggestions": suggestions,

        # Category breakdown
        "category_stats": {
            category.value: len(bullets_list)
            for category, bullets_list in categorized.items()
        }
    }

    return optimized_pdf, scores


def score_bullet(bullet: str, job_skills: set, job_keywords: set) -> float:
    """
    Score a single bullet point based on job requirements.

    Uses a simple scoring algorithm:
        - +1.0 for each matching skill
        - +0.5 for each matching keyword
        - +0.3 for action verbs
        - +0.2 for quantifiable results (numbers, percentages)

    TODO: Improve with TF-IDF or cosine similarity using sentence embeddings
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        bullet_embedding = model.encode(bullet)
        job_embedding = model.encode(job_description)
        similarity = cosine_similarity(bullet_embedding, job_embedding)
    """

    score = 0.0
    bullet_lower = bullet.lower()

    # Check for skill matches
    for skill in job_skills:
        if skill in bullet_lower:
            score += 1.0

    # Check for keyword matches
    words = set(re.findall(r'\b\w+\b', bullet_lower))
    matching_keywords = words & job_keywords
    score += len(matching_keywords) * 0.5

    # Check for action verbs
    action_verbs = {
        'developed', 'built', 'created', 'designed', 'implemented',
        'managed', 'led', 'increased', 'reduced', 'improved',
        'optimized', 'automated', 'streamlined', 'launched',
        'delivered', 'achieved', 'collaborated', 'coordinated'
    }
    if any(verb in bullet_lower for verb in action_verbs):
        score += 0.3

    # Check for quantifiable results
    if re.search(r'\d+%|\d+x|\$\d+|\d+ [a-z]+', bullet_lower):
        score += 0.2

    return score


def calculate_overall_score(resume_text: str, job_keywords: Dict[str, Any]) -> float:
    """
    Calculate overall resume relevance score (0-100).

    Factors:
        - Percentage of job skills found in resume
        - Keyword overlap
        - Years of experience match
    """

    resume_lower = resume_text.lower()
    job_skills = set(job_keywords.get("skills", []))
    job_kws = set(job_keywords.get("keywords", []))

    if not job_skills:
        return 50.0  # Default if no skills detected

    # Count matching skills
    matching_skills = sum(1 for skill in job_skills if skill in resume_lower)
    skill_score = (matching_skills / len(job_skills)) * 100

    # Count matching keywords
    resume_words = set(re.findall(r'\b\w+\b', resume_lower))
    matching_kws = len(resume_words & job_kws)
    keyword_score = min((matching_kws / max(len(job_kws), 1)) * 100, 100)

    # Weighted average (skills matter more)
    overall = (skill_score * 0.7) + (keyword_score * 0.3)

    return round(overall, 2)


def extract_resume_skills(resume_text: str) -> set:
    """
    Extract skills from resume text.

    (Reuses logic from job_parser, but applied to resume)
    """

    from app.job_parser import extract_skills
    return extract_skills(resume_text.lower())


def generate_optimized_pdf(
    parsed_resume: Dict[str, Any],
    optimized_bullets: List[str],
    original_content: bytes
) -> bytes:
    """
    Generate a new PDF with optimized bullet order.

    TODO: Implement PDF generation using reportlab or weasyprint:

    Option 1: Using reportlab (pure PDF generation)
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

    Option 2: Using weasyprint (HTML to PDF)
        from weasyprint import HTML
        html_content = generate_html_resume(parsed_resume, bullet_scores)
        pdf_bytes = HTML(string=html_content).write_pdf()

    For now, just return the original content (no optimization applied)
    """

    # PLACEHOLDER: Return original content for now
    # TODO: Implement proper PDF generation with reordered bullets

    return original_content


def generate_html_resume(
    parsed_resume: Dict[str, Any],
    bullet_scores: List[Dict]
) -> str:
    """
    Generate HTML representation of optimized resume.

    This can be converted to PDF using weasyprint.

    TODO: Implement HTML template with proper styling
    """

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .section { margin-bottom: 20px; }
            .bullet { margin-left: 20px; margin-bottom: 10px; }
            .highlight { background-color: yellow; }
        </style>
    </head>
    <body>
        <h1>Optimized Resume</h1>
        <div class="section">
            <h2>Experience</h2>
    """

    for item in bullet_scores:
        html += f'<div class="bullet">• {item["bullet"]}</div>\n'

    html += """
        </div>
    </body>
    </html>
    """

    return html
