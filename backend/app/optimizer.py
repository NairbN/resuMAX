"""
Resume Optimizer Module

Uses SEMANTIC SIMILARITY (embeddings) to score and reorder resume bullets.
Goes beyond keyword matching to understand meaning and context.
"""

from typing import Dict, Tuple, Any

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
        print(f"\n📝 Reordering bullets in {len(experiences)} experience entries...")
        for exp_idx, exp in enumerate(experiences):
            exp_bullets = exp.get("bullets", [])
            if exp_bullets:
                print(f"\n  Experience {exp_idx + 1}: {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')}")
                print(f"    Original bullet count: {len(exp_bullets)}")
                print(f"    First bullet before: {exp_bullets[0][:80]}...")
                
                # Sort this job's bullets by relevance score
                sorted_bullets = sorted(
                    exp_bullets,
                    key=lambda b: bullet_ranks.get(b, 0),
                    reverse=True
                )
                exp["bullets"] = sorted_bullets
                
                print(f"    First bullet after:  {sorted_bullets[0][:80]}...")
                print(f"    Scores: {[round(bullet_ranks.get(b, 0) * 100, 1) for b in sorted_bullets[:3]]}")
        # Update parsed resume with reordered bullets
        parsed_resume["experience"] = experiences

    # Reorder bullets within each project entry
    projects = parsed_resume.get("projects", [])
    if projects:
        print(f"\n📝 Reordering bullets in {len(projects)} project entries...")
        for proj_idx, proj in enumerate(projects):
            proj_bullets = proj.get("bullets", [])
            if proj_bullets:
                print(f"\n  Project {proj_idx + 1}: {proj.get('name', 'Unknown')}")
                print(f"    Original bullet count: {len(proj_bullets)}")
                
                # Sort this project's bullets by relevance score
                sorted_bullets = sorted(
                    proj_bullets,
                    key=lambda b: bullet_ranks.get(b, 0),
                    reverse=True
                )
                proj["bullets"] = sorted_bullets
                
                print(f"    Scores: {[round(bullet_ranks.get(b, 0) * 100, 1) for b in sorted_bullets[:3]]}")
        # Update parsed resume with reordered bullets
        parsed_resume["projects"] = projects

    # === STEP 9: Generate new PDF ===
    # Use the new HTML+CSS layout engine for deterministic one-page output
    from app.resume_layout_engine import generate_optimized_resume_html
    optimized_pdf = generate_optimized_resume_html(
        parsed_resume=parsed_resume,
        semantic_scores=semantic_results
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
