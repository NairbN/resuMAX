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

    # DEBUG: Log what we extracted
    print(f"\n🔍 DEBUG - Optimization Input:")
    print(f"  - Found {len(bullets)} bullets in resume")
    print(f"  - Resume text length: {len(resume_text)} chars")
    print(f"  - Job description length: {len(job_description)} chars")
    if bullets:
        print(f"  - First bullet: {bullets[0][:100]}...")
    else:
        print(f"  - ⚠️  WARNING: No bullets found!")

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

    # === STEP 8: Reorder bullets within each job AND project ===
    # Create a ranking map for all bullets
    bullet_ranks = {item["bullet"]: item["score"] for item in semantic_results}

    # Reorder bullets within each experience entry
    experiences = parsed_resume.get("experience", [])
    if experiences:
        for exp in experiences:
            exp_bullets = exp.get("bullets", [])
            if exp_bullets:
                # Sort this job's bullets by relevance score
                exp["bullets"] = sorted(
                    exp_bullets,
                    key=lambda b: bullet_ranks.get(b, 0),
                    reverse=True
                )
        # Update parsed resume with reordered bullets
        parsed_resume["experience"] = experiences

    # Reorder bullets within each project entry
    projects = parsed_resume.get("projects", [])
    if projects:
        for proj in projects:
            proj_bullets = proj.get("bullets", [])
            if proj_bullets:
                # Sort this project's bullets by relevance score
                proj["bullets"] = sorted(
                    proj_bullets,
                    key=lambda b: bullet_ranks.get(b, 0),
                    reverse=True
                )
        # Update parsed resume with reordered bullets
        parsed_resume["projects"] = projects

    # === STEP 9: Generate new PDF ===
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

    # DEBUG: Log what we're returning
    print(f"\n📊 DEBUG - Optimization Results:")
    print(f"  - Overall score: {scores['overall_score']}")
    print(f"  - Comparison: {comparison}")
    print(f"  - Optimized {len(optimized_bullets)} bullets")
    print(f"  - Top bullet score: {scores['top_bullets'][0]['score'] if scores['top_bullets'] else 'N/A'}")

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
    Generate a professional, ATS-friendly PDF resume with optimized bullets.

    Creates a complete, job-ready resume that preserves all original information
    but reorders bullets for maximum relevance to the job.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from io import BytesIO
    import textwrap

    # Create PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Define colors for a professional look
    dark_blue = HexColor('#1a1a2e')
    light_blue = HexColor('#0f3460')
    text_color = HexColor('#2d2d2d')

    # Starting position
    y = height - 0.75 * inch
    margin_left = 0.75 * inch
    margin_right = width - 0.75 * inch
    content_width = margin_right - margin_left

    # === HEADER: Name and Contact ===
    contact_info = parsed_resume.get("contact_info", {})

    # Name (large, bold)
    c.setFillColor(dark_blue)
    c.setFont("Helvetica-Bold", 24)
    name = contact_info.get("name", "YOUR NAME")
    c.drawString(margin_left, y, name)
    y -= 0.35 * inch

    # Contact info (single line)
    c.setFillColor(text_color)
    c.setFont("Helvetica", 9)
    contact_parts = []
    if contact_info.get("email"):
        contact_parts.append(contact_info["email"])
    if contact_info.get("phone"):
        contact_parts.append(contact_info["phone"])
    if contact_info.get("linkedin"):
        contact_parts.append(contact_info["linkedin"])
    if contact_info.get("location"):
        contact_parts.append(contact_info["location"])

    if contact_parts:
        contact_line = " | ".join(contact_parts)
        c.drawString(margin_left, y, contact_line)
        y -= 0.15 * inch

    # Horizontal line separator
    c.setStrokeColor(light_blue)
    c.setLineWidth(1.5)
    c.line(margin_left, y, margin_right, y)
    y -= 0.3 * inch

    # === SUMMARY (if available) ===
    summary = parsed_resume.get("summary", "")
    if summary:
        c.setFillColor(dark_blue)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left, y, "PROFESSIONAL SUMMARY")
        y -= 0.2 * inch

        c.setFillColor(text_color)
        c.setFont("Helvetica", 9)
        # Wrap summary text
        wrapped = textwrap.fill(summary, width=100)
        for line in wrapped.split('\n'):
            c.drawString(margin_left + 0.1 * inch, y, line)
            y -= 0.15 * inch
        y -= 0.15 * inch

    # === EXPERIENCE SECTION ===
    c.setFillColor(dark_blue)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_left, y, "PROFESSIONAL EXPERIENCE")
    y -= 0.25 * inch

    # Get experience entries from parsed resume
    experiences = parsed_resume.get("experience", [])

    if experiences:
        for exp in experiences:
            # Check if we need a new page
            if y < 2 * inch:
                c.showPage()
                y = height - 0.75 * inch

            # Company/Title/Date
            c.setFillColor(text_color)
            c.setFont("Helvetica-Bold", 10)
            title_line = exp.get("title", "")
            if exp.get("company"):
                title_line += f" - {exp['company']}"
            c.drawString(margin_left + 0.1 * inch, y, title_line)

            # Date (right-aligned)
            if exp.get("date"):
                c.setFont("Helvetica-Oblique", 9)
                date_width = c.stringWidth(exp["date"], "Helvetica-Oblique", 9)
                c.drawString(margin_right - date_width, y, exp["date"])

            y -= 0.2 * inch

            # Bullets for this job
            job_bullets = exp.get("bullets", [])
            c.setFont("Helvetica", 9)
            for bullet in job_bullets:
                if y < 1 * inch:
                    c.showPage()
                    y = height - 0.75 * inch

                # Word wrap bullets
                wrapped = textwrap.fill(bullet, width=95)
                lines = wrapped.split('\n')
                for i, line in enumerate(lines):
                    if i == 0:
                        c.drawString(margin_left + 0.2 * inch, y, f"• {line}")
                    else:
                        c.drawString(margin_left + 0.3 * inch, y, line)
                    y -= 0.13 * inch
                y -= 0.03 * inch

            y -= 0.15 * inch
    else:
        # No structured experience, just use optimized bullets
        c.setFont("Helvetica", 9)
        c.setFillColor(text_color)
        for bullet in optimized_bullets:
            if y < 1 * inch:
                c.showPage()
                y = height - 0.75 * inch

            # Word wrap
            wrapped = textwrap.fill(bullet, width=95)
            lines = wrapped.split('\n')
            for i, line in enumerate(lines):
                if i == 0:
                    c.drawString(margin_left + 0.2 * inch, y, f"• {line}")
                else:
                    c.drawString(margin_left + 0.3 * inch, y, line)
                y -= 0.13 * inch
            y -= 0.03 * inch

    # === PROJECTS ===
    projects = parsed_resume.get("projects", [])
    if projects:
        if y < 2 * inch:
            c.showPage()
            y = height - 0.75 * inch

        y -= 0.2 * inch
        c.setFillColor(dark_blue)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left, y, "PROJECTS")
        y -= 0.25 * inch

        for proj in projects:
            # Check if we need a new page
            if y < 2 * inch:
                c.showPage()
                y = height - 0.75 * inch

            # Project name and tech stack
            c.setFillColor(text_color)
            c.setFont("Helvetica-Bold", 10)
            project_line = proj.get("name", "")
            if proj.get("tech_stack"):
                project_line += f" | {proj['tech_stack']}"
            c.drawString(margin_left + 0.1 * inch, y, project_line)
            y -= 0.2 * inch

            # Project bullets
            proj_bullets = proj.get("bullets", [])
            c.setFont("Helvetica", 9)
            for bullet in proj_bullets:
                if y < 1 * inch:
                    c.showPage()
                    y = height - 0.75 * inch

                # Word wrap bullets
                wrapped = textwrap.fill(bullet, width=95)
                lines = wrapped.split('\n')
                for i, line in enumerate(lines):
                    if i == 0:
                        c.drawString(margin_left + 0.2 * inch, y, f"• {line}")
                    else:
                        c.drawString(margin_left + 0.3 * inch, y, line)
                    y -= 0.13 * inch
                y -= 0.03 * inch

            y -= 0.15 * inch

    # === EDUCATION ===
    education = parsed_resume.get("education", [])
    if education:
        if y < 2 * inch:
            c.showPage()
            y = height - 0.75 * inch

        y -= 0.2 * inch
        c.setFillColor(dark_blue)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left, y, "EDUCATION")
        y -= 0.2 * inch

        c.setFillColor(text_color)
        c.setFont("Helvetica", 9)
        for edu in education:
            if isinstance(edu, dict):
                edu_line = edu.get("degree", "")
                if edu.get("school"):
                    edu_line += f" - {edu['school']}"
                if edu.get("year"):
                    c.setFont("Helvetica-Oblique", 9)
                    year_width = c.stringWidth(edu["year"], "Helvetica-Oblique", 9)
                    c.drawString(margin_right - year_width, y, edu["year"])
                    c.setFont("Helvetica", 9)
                c.drawString(margin_left + 0.1 * inch, y, edu_line)
            else:
                c.drawString(margin_left + 0.1 * inch, y, str(edu))
            y -= 0.15 * inch

    # === SKILLS ===
    skills = parsed_resume.get("skills", {})
    if skills:
        if y < 2 * inch:
            c.showPage()
            y = height - 0.75 * inch

        y -= 0.2 * inch
        c.setFillColor(dark_blue)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left, y, "SKILLS")
        y -= 0.2 * inch

        c.setFillColor(text_color)
        c.setFont("Helvetica", 9)
        for category, skill_list in skills.items():
            if y < 1 * inch:
                c.showPage()
                y = height - 0.75 * inch

            skill_text = f"{category}: {', '.join(skill_list) if isinstance(skill_list, list) else skill_list}"
            wrapped = textwrap.fill(skill_text, width=95)
            for line in wrapped.split('\n'):
                c.drawString(margin_left + 0.1 * inch, y, line)
                y -= 0.13 * inch
            y -= 0.02 * inch

    c.save()
    buffer.seek(0)
    return buffer.read()


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
