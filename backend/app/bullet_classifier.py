"""
Bullet Point Classifier

Categorizes resume bullets into types:
- Skills/Tools
- Leadership/Management
- Achievements/Results
- Projects
- Responsibilities

This ensures optimized resumes have balanced content.
"""

import re
from typing import List, Dict
from enum import Enum


class BulletCategory(Enum):
    """Categories for resume bullet points"""
    ACHIEVEMENT = "achievement"      # Results, metrics, impact
    LEADERSHIP = "leadership"        # Team management, mentorship
    TECHNICAL = "technical"          # Technical skills, tools, implementation
    PROJECT = "project"              # Projects, initiatives
    RESPONSIBILITY = "responsibility" # Day-to-day duties
    EDUCATION = "education"          # Learning, training, certifications


# Keywords that indicate each category
CATEGORY_INDICATORS = {
    BulletCategory.ACHIEVEMENT: {
        "keywords": [
            "increased", "decreased", "improved", "reduced", "generated",
            "saved", "achieved", "exceeded", "delivered", "launched",
            "grew", "boosted", "optimized", "accelerated", "won"
        ],
        "patterns": [
            r'\d+%',           # Percentages (50% increase)
            r'\$\d+[kmb]?',    # Money ($500K, $2M)
            r'\d+x',           # Multiples (3x growth)
            r'\d+\s*(million|thousand|billion)',  # Large numbers
        ]
    },
    BulletCategory.LEADERSHIP: {
        "keywords": [
            "led", "managed", "supervised", "mentored", "coached",
            "directed", "coordinated", "guided", "trained", "hired",
            "onboarded", "team", "cross-functional", "stakeholder"
        ],
        "patterns": [
            r'team of \d+',
            r'led \d+ (engineers|developers|analysts|designers)',
        ]
    },
    BulletCategory.TECHNICAL: {
        "keywords": [
            "developed", "built", "implemented", "designed", "architected",
            "engineered", "coded", "programmed", "deployed", "integrated",
            "configured", "automated", "migrated", "refactored"
        ],
        "patterns": [
            r'\b(python|java|react|sql|aws|docker|kubernetes)\b',  # Tech keywords
            r'using (python|react|aws|docker)',
        ]
    },
    BulletCategory.PROJECT: {
        "keywords": [
            "project", "initiative", "campaign", "program", "product",
            "system", "platform", "application", "tool", "feature"
        ],
        "patterns": []
    },
    BulletCategory.RESPONSIBILITY: {
        "keywords": [
            "responsible for", "duties include", "maintained", "monitored",
            "supported", "assisted", "handled", "processed", "conducted",
            "performed", "ensured", "managed day-to-day"
        ],
        "patterns": []
    }
}


def classify_bullet(bullet: str) -> BulletCategory:
    """
    Classify a single bullet point into a category.

    Uses keyword matching and regex patterns.

    Args:
        bullet: Resume bullet point text

    Returns:
        BulletCategory enum

    Example:
        classify_bullet("Increased revenue by 50% through optimization")
        → BulletCategory.ACHIEVEMENT

        classify_bullet("Led team of 5 engineers to deliver new feature")
        → BulletCategory.LEADERSHIP
    """
    bullet_lower = bullet.lower()

    # Score each category
    scores = {category: 0 for category in BulletCategory}

    for category, indicators in CATEGORY_INDICATORS.items():
        # Check keywords
        for keyword in indicators["keywords"]:
            if keyword in bullet_lower:
                scores[category] += 1

        # Check patterns
        for pattern in indicators["patterns"]:
            if re.search(pattern, bullet_lower):
                scores[category] += 2  # Patterns are stronger signals

    # Return category with highest score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)

    # Default to responsibility if no strong signals
    return BulletCategory.RESPONSIBILITY


def classify_bullets(bullets: List[str]) -> Dict[BulletCategory, List[Dict]]:
    """
    Classify all bullets into categories.

    Args:
        bullets: List of resume bullet points

    Returns:
        Dictionary mapping categories to lists of bullets with metadata

    Example:
        classify_bullets([
            "Increased revenue by 50%",
            "Built Python API using FastAPI",
            "Led team of 3 engineers"
        ])
        →
        {
            BulletCategory.ACHIEVEMENT: [
                {"text": "Increased revenue by 50%", "index": 0}
            ],
            BulletCategory.TECHNICAL: [
                {"text": "Built Python API using FastAPI", "index": 1}
            ],
            BulletCategory.LEADERSHIP: [
                {"text": "Led team of 3 engineers", "index": 2}
            ]
        }
    """
    categorized = {category: [] for category in BulletCategory}

    for index, bullet in enumerate(bullets):
        category = classify_bullet(bullet)
        categorized[category].append({
            "text": bullet,
            "index": index,
            "category": category.value
        })

    return categorized


def balance_categories(
    categorized_bullets: Dict[BulletCategory, List[Dict]],
    max_bullets: int = 10
) -> List[str]:
    """
    Select balanced set of bullets across categories.

    Ensures resume shows diverse skills (not all achievements or all responsibilities).

    Args:
        categorized_bullets: Bullets grouped by category
        max_bullets: Maximum number of bullets to return

    Returns:
        List of selected bullet texts

    Strategy:
        1. Prioritize achievements (results matter most)
        2. Include leadership if available
        3. Include technical/project bullets
        4. Minimize pure responsibilities
    """
    selected = []

    # Priority order
    priority_order = [
        BulletCategory.ACHIEVEMENT,
        BulletCategory.LEADERSHIP,
        BulletCategory.TECHNICAL,
        BulletCategory.PROJECT,
        BulletCategory.RESPONSIBILITY,
        BulletCategory.EDUCATION
    ]

    # Target distribution (% of total)
    target_distribution = {
        BulletCategory.ACHIEVEMENT: 0.40,    # 40% achievements
        BulletCategory.LEADERSHIP: 0.20,     # 20% leadership
        BulletCategory.TECHNICAL: 0.25,      # 25% technical
        BulletCategory.PROJECT: 0.10,        # 10% projects
        BulletCategory.RESPONSIBILITY: 0.05, # 5% responsibilities
        BulletCategory.EDUCATION: 0.00       # Usually in separate section
    }

    # Calculate target counts
    target_counts = {
        cat: int(max_bullets * target_distribution[cat])
        for cat in BulletCategory
    }

    # Select bullets per category (up to target)
    for category in priority_order:
        available = categorized_bullets.get(category, [])
        target = target_counts[category]

        # Take up to target count
        selected.extend(available[:target])

    # Fill remaining slots with any category (priority order)
    remaining = max_bullets - len(selected)
    if remaining > 0:
        for category in priority_order:
            available = categorized_bullets.get(category, [])
            # Skip already selected bullets
            available = [b for b in available if b not in selected]

            take = min(remaining, len(available))
            selected.extend(available[:take])
            remaining -= take

            if remaining == 0:
                break

    # Return bullet texts only
    return [bullet["text"] for bullet in selected[:max_bullets]]


def get_category_stats(categorized_bullets: Dict[BulletCategory, List[Dict]]) -> Dict[str, any]:
    """
    Get statistics about bullet distribution.

    Useful for showing users their resume breakdown.

    Args:
        categorized_bullets: Bullets grouped by category

    Returns:
        Statistics dictionary

    Example output:
        {
            "total_bullets": 15,
            "achievement_bullets": 6,
            "leadership_bullets": 3,
            "technical_bullets": 5,
            "project_bullets": 1,
            "responsibility_bullets": 0,
            "achievement_percentage": 40.0
        }
    """
    total = sum(len(bullets) for bullets in categorized_bullets.values())

    stats = {"total_bullets": total}

    for category, bullets in categorized_bullets.items():
        count = len(bullets)
        stats[f"{category.value}_bullets"] = count
        stats[f"{category.value}_percentage"] = round((count / total * 100) if total > 0 else 0, 1)

    return stats
