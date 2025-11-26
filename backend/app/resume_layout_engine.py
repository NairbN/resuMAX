"""
Deterministic Resume Layout Engine

Architecture:
1. ResumeNormalizer: Standardize data + merge semantic scores
2. OverflowManager: Iteratively remove low-priority bullets until fits on 1 page
3. TemplateRenderer: Generate HTML/CSS → PDF

Why HTML+CSS instead of ReportLab:
- Auto text wrapping
- Automatic spacing
- Consistent layout
- CSS handles typography
- No manual font measurement needed
"""

from typing import Dict, List, Any
import tempfile
from pathlib import Path


class ResumeNormalizer:
    """
    Normalize and enrich resume data with semantic scores.

    Input:
        - parsed_resume (dict with experience, projects, education, skills)
        - semantic_scores (list of {bullet, score, rank})

    Output:
        - normalized_data (dict with bullets sorted by score within each section)
    """

    def normalize(
        self,
        parsed_resume: Dict[str, Any],
        semantic_scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merge semantic scores with resume data and sort bullets.

        Returns normalized structure:
        {
            "name": "...",
            "contact": {...},
            "experience": [
                {
                    "title": "...",
                    "company": "...",
                    "date": "...",
                    "bullets": [
                        {"text": "...", "score": 0.85},  # Sorted by score
                        {"text": "...", "score": 0.72},
                        ...
                    ]
                }
            ],
            "projects": [...],  # Same structure
            "education": [...],
            "skills": {...}
        }
        """
        # Create score map
        score_map = {item["bullet"]: item["score"] for item in semantic_scores}

        # Normalize experience
        normalized_experience = []
        for exp in parsed_resume.get("experience", []):
            bullets_with_scores = [
                {
                    "text": bullet,
                    "score": score_map.get(bullet, 0)
                }
                for bullet in exp.get("bullets", [])
            ]
            # Sort by score (highest first)
            bullets_with_scores.sort(key=lambda b: b["score"], reverse=True)

            normalized_experience.append({
                "title": exp.get("title", ""),
                "company": exp.get("company", ""),
                "location": exp.get("location", ""),
                "date": exp.get("date", ""),
                "bullets": bullets_with_scores
            })

        # Normalize projects
        normalized_projects = []
        for proj in parsed_resume.get("projects", []):
            bullets_with_scores = [
                {
                    "text": bullet,
                    "score": score_map.get(bullet, 0)
                }
                for bullet in proj.get("bullets", [])
            ]
            bullets_with_scores.sort(key=lambda b: b["score"], reverse=True)

            normalized_projects.append({
                "name": proj.get("name", ""),
                "tech_stack": proj.get("tech_stack", ""),
                "link": proj.get("link", ""),
                "bullets": bullets_with_scores
            })

        return {
            "name": parsed_resume.get("contact_info", {}).get("name", ""),
            "contact": parsed_resume.get("contact_info", {}),
            "experience": normalized_experience,
            "projects": normalized_projects,
            "education": parsed_resume.get("education", []),
            "skills": parsed_resume.get("skills", {}),
        }


class TemplateRenderer:
    """
    Render resume as HTML with professional CSS.

    CSS handles all layout:
    - Text wrapping
    - Line spacing
    - Section spacing
    - Typography
    - Page constraints
    """

    TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: letter;
            margin: 0.5in 0.6in;
        }

        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 10.5pt;
            line-height: 1.15;
            margin: 0;
            padding: 0;
        }

        /* Header - centered */
        .header {
            text-align: center;
            margin-bottom: 0.15in;
        }

        .name {
            font-size: 16pt;
            font-weight: normal;
            margin: 0 0 0.08in 0;
        }

        .contact {
            font-size: 10.5pt;
            margin: 0;
        }

        /* Section headers - bold 10.5pt */
        .section-header {
            font-size: 10.5pt;
            font-weight: bold;
            margin-top: {{ section_margin_top }};
            margin-bottom: {{ section_margin_bottom }};
            border-bottom: 1pt solid #000;
            padding-bottom: 0.02in;
        }

        /* Experience/Project entries */
        .entry {
            margin-bottom: {{ entry_margin_bottom }};
            page-break-inside: avoid;
        }

        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.02in;
        }

        .entry-left {
            font-size: 9pt;
            font-weight: bold;
            flex: 0 1 auto;
        }

        .entry-right {
            font-size: 9pt;
            font-style: italic;
            text-align: right;
            white-space: nowrap;
            flex: 0 0 auto;
            margin-left: auto;
        }
        
        .entry .entry-header:last-of-type {
            margin-bottom: 0.05in;
        }

        /* Bullets - compact */
        .bullets {
            margin: 0;
            padding-left: 0.15in;
            list-style-type: disc;
        }

        .bullets li {
            font-size: 8.5pt;
            margin-bottom: 0.03in;
            padding-left: 0.05in;
        }

        /* Education */
        .education-entry {
            margin-bottom: 0.08in;
        }

        .education-header {
            display: flex;
            justify-content: space-between;
            font-size: 9pt;
            margin-bottom: 0.04in;
        }

        .education-degree {
            font-size: 9pt;
        }

        /* Skills */
        .skill-category {
            font-size: 8.5pt;
            margin-bottom: 0.04in;
        }

        .skill-category strong {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <!-- HEADER -->
    <div class="header">
        <div class="name">{{ name }}</div>
        <div class="contact">{{ contact_line }}</div>
    </div>

    <!-- SKILLS -->
    {% if skills %}
    <div class="section-header">SKILLS</div>
    {% for category, skill_list in skills.items() %}
    <div class="skill-category">
        <strong>{{ category }}:</strong> {{ skill_list|join(', ') if skill_list is iterable and skill_list is not string else skill_list }}
    </div>
    {% endfor %}
    {% endif %}

    <!-- EXPERIENCE -->
    {% if experience %}
    <div class="section-header">EXPERIENCE</div>
    {% for exp in experience %}
    <div class="entry">
        <div class="entry-header">
            <div class="entry-left">{{ exp.company }}</div>
            <div class="entry-right">{{ exp.location }}</div>
        </div>
        <div class="entry-header">
            <div class="entry-left">{{ exp.title }}</div>
            <div class="entry-right">{{ exp.date }}</div>
        </div>
        <ul class="bullets">
            {% for bullet in exp.bullets %}
            <li>{{ bullet.text }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endfor %}
    {% endif %}

    <!-- PROJECTS -->
    {% if projects %}
    <div class="section-header">PROJECTS</div>
    {% for proj in projects %}
    <div class="entry">
        <div class="entry-header">
            <div class="entry-left">{{ proj.name }}{% if proj.tech_stack %} | {{ proj.tech_stack }}{% endif %}</div>
            <div class="entry-right">
                {% if proj.link %}
                    {% if proj.link.startswith('http') %}
                    <a href="{{ proj.link }}" style="color: #0066cc; text-decoration: none;">(Link)</a>
                    {% else %}
                    <span style="color: #0066cc;">{{ proj.link }}</span>
                    {% endif %}
                {% endif %}
            </div>
        </div>
        <ul class="bullets">
            {% for bullet in proj.bullets %}
            <li>{{ bullet.text }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endfor %}
    {% endif %}

    <!-- EDUCATION -->
    {% if education %}
    <div class="section-header">EDUCATION</div>
    {% for edu in education %}
    <div class="education-entry">
        <div class="entry-header">
            <div class="entry-left">{{ edu.school }}</div>
            <div class="entry-right">{{ edu.location }}</div>
        </div>
        <div class="entry-header">
            <div class="entry-left">{{ edu.degree }}</div>
            <div class="entry-right">{{ edu.year }}</div>
        </div>
    </div>
    {% endfor %}
    {% endif %}
</body>
</html>
    """

    def render_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML from normalized data."""
        from jinja2 import Template

        # Determine spacing based on mode
        spacing_mode = data.get('_spacing_mode', 'balanced')
        if spacing_mode == 'balanced':
            # More generous spacing to fill the page
            section_margin_top = '0.2in'
            section_margin_bottom = '0.12in'
            entry_margin_bottom = '0.2in'
        else:
            # Compact spacing
            section_margin_top = '0.12in'
            section_margin_bottom = '0.08in'
            entry_margin_bottom = '0.1in'

        # Build contact line - deduplicate and format properly
        contact = data.get("contact", {})
        contact_parts = []
        seen = set()
        
        # Add contact info in order, avoiding duplicates
        if contact.get("email") and contact.get("email") not in seen:
            contact_parts.append(contact.get("email"))
            seen.add(contact.get("email"))
        
        if contact.get("phone") and contact.get("phone") not in seen:
            contact_parts.append(contact.get("phone"))
            seen.add(contact.get("phone"))
        
        if contact.get("website") and contact.get("website") not in seen:
            # Only add if not already part of email/linkedin/github
            website = contact.get("website")
            if not any(website in str(v) for v in seen):
                contact_parts.append(website)
                seen.add(website)
        
        if contact.get("linkedin") and contact.get("linkedin") not in seen:
            linkedin = contact.get("linkedin")
            if not any(linkedin in str(v) for v in seen):
                contact_parts.append(linkedin)
                seen.add(linkedin)
        
        if contact.get("github") and contact.get("github") not in seen:
            github = contact.get("github")
            if not any(github in str(v) for v in seen):
                contact_parts.append(github)
                seen.add(github)
        
        contact_line = " | ".join(contact_parts)

        # Render template
        template = Template(self.TEMPLATE)
        return template.render(
            name=data.get("name", ""),
            contact_line=contact_line,
            experience=data.get("experience", []),
            projects=data.get("projects", []),
            education=data.get("education", []),
            skills=data.get("skills", {}),
            section_margin_top=section_margin_top,
            section_margin_bottom=section_margin_bottom,
            entry_margin_bottom=entry_margin_bottom
        )


class OverflowManager:
    """
    Ensure resume fits on ONE page by iteratively removing lowest-scored bullets.

    Algorithm:
    1. Render HTML
    2. Convert to PDF and measure page count
    3. If > 1 page: remove lowest-scored bullet across all sections
    4. Repeat until fits

    This is deterministic because:
    - Bullets are pre-sorted by score
    - We always remove the globally lowest-scored bullet
    - PDF rendering is deterministic
    """

    def __init__(self):
        self.renderer = TemplateRenderer()

    def fit_to_one_page(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove bullets until resume fits on exactly 1 page.
        Then adjust spacing to fill the page evenly.

        Returns the trimmed data that fits.
        """
        max_iterations = 50  # Safety limit

        for iteration in range(max_iterations):
            # Render current state
            html = self.renderer.render_html(normalized_data)

            # Check if it fits
            page_count = self._count_pages(html)

            print(f"  Iteration {iteration + 1}: {page_count} page(s)")

            if page_count <= 1:
                print(f"  ✅ Fits on 1 page!")
                # Now adjust spacing to fill the page better
                normalized_data['_spacing_mode'] = 'balanced'
                return normalized_data

            # Find and remove lowest-scored bullet
            if not self._remove_lowest_bullet(normalized_data):
                # No more bullets to remove
                print(f"  ⚠️  Warning: Cannot fit on 1 page even after removing all bullets")
                normalized_data['_spacing_mode'] = 'compact'
                return normalized_data

        print(f"  ⚠️  Warning: Reached max iterations ({max_iterations})")
        normalized_data['_spacing_mode'] = 'compact'
        return normalized_data

    def _count_pages(self, html: str) -> int:
        """Render HTML to PDF and count pages."""
        try:
            from weasyprint import HTML, CSS

            # Render to PDF in memory
            pdf_bytes = HTML(string=html).write_pdf()

            # Count pages using PyPDF2
            from PyPDF2 import PdfReader
            from io import BytesIO

            reader = PdfReader(BytesIO(pdf_bytes))
            return len(reader.pages)

        except ImportError:
            # Fallback: estimate based on character count
            # This is rough but better than nothing
            char_count = len(html)
            # Assume ~3000 chars per page (very rough)
            return max(1, char_count // 3000)

    def _remove_lowest_bullet(self, data: Dict[str, Any]) -> bool:
        """
        Remove the globally lowest-scored bullet.

        Returns True if a bullet was removed, False if none left.
        """
        lowest_bullet = None
        lowest_score = float('inf')
        lowest_section = None
        lowest_entry_idx = None
        lowest_bullet_idx = None

        # Search experience
        for exp_idx, exp in enumerate(data.get("experience", [])):
            for bullet_idx, bullet in enumerate(exp.get("bullets", [])):
                if bullet["score"] < lowest_score:
                    lowest_score = bullet["score"]
                    lowest_bullet = bullet
                    lowest_section = "experience"
                    lowest_entry_idx = exp_idx
                    lowest_bullet_idx = bullet_idx

        # Search projects
        for proj_idx, proj in enumerate(data.get("projects", [])):
            for bullet_idx, bullet in enumerate(proj.get("bullets", [])):
                if bullet["score"] < lowest_score:
                    lowest_score = bullet["score"]
                    lowest_bullet = bullet
                    lowest_section = "projects"
                    lowest_entry_idx = proj_idx
                    lowest_bullet_idx = bullet_idx

        # Remove if found
        if lowest_bullet:
            if lowest_section == "experience":
                removed = data["experience"][lowest_entry_idx]["bullets"].pop(lowest_bullet_idx)
            elif lowest_section == "projects":
                removed = data["projects"][lowest_entry_idx]["bullets"].pop(lowest_bullet_idx)

            print(f"    Removed bullet (score={lowest_score:.3f}): {removed['text'][:60]}...")
            return True

        return False


def generate_optimized_resume_html(
    parsed_resume: Dict[str, Any],
    semantic_scores: List[Dict[str, Any]]
) -> bytes:
    """
    Main function: Generate a 1-page optimized resume PDF.

    Pipeline:
    1. Normalize data + merge scores
    2. Remove bullets until fits on 1 page
    3. Render final PDF

    Returns PDF bytes.
    """
    print("\n📄 Generating optimized resume...")

    # Step 1: Normalize
    print("  Step 1: Normalizing data...")
    normalizer = ResumeNormalizer()
    normalized_data = normalizer.normalize(parsed_resume, semantic_scores)

    # Step 2: Fit to one page
    print("  Step 2: Fitting to one page...")
    overflow_manager = OverflowManager()
    fitted_data = overflow_manager.fit_to_one_page(normalized_data)

    # Step 3: Render final PDF
    print("  Step 3: Rendering final PDF...")
    renderer = TemplateRenderer()
    final_html = renderer.render_html(fitted_data)

    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=final_html).write_pdf()
        print("  ✅ PDF generated successfully!")
        return pdf_bytes
    except ImportError:
        print("  ⚠️  WeasyPrint not installed, returning HTML instead")
        # Fallback: return HTML as bytes
        return final_html.encode('utf-8')
