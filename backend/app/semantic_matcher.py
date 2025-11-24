"""
Semantic Matching Engine

Uses sentence embeddings to measure true similarity between resume and job description.
Goes beyond keyword matching to understand MEANING.

Example:
    Resume: "Built RESTful API using Python and FastAPI"
    Job: "Develop backend services with Python"

    Keyword match: 1 word (Python)
    Semantic similarity: 0.87 (very similar meaning!)

Uses sentence-transformers for lightweight embeddings (no LLM needed).
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity


# Optional: Use sentence-transformers for better semantic matching
# If not installed, fallback to TF-IDF
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("Warning: sentence-transformers not installed. Using TF-IDF fallback.")


class SemanticMatcher:
    """
    Semantic similarity matcher using sentence embeddings.

    This is MUCH better than keyword matching because it understands context:
    - "Developed Python API" ≈ "Built backend services using Python"
    - "Led team of 5" ≈ "Managed engineering team"
    - "Increased revenue" ≈ "Drove business growth"
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize semantic matcher.

        Args:
            model_name: Sentence transformer model
                - "all-MiniLM-L6-v2" (default): 80MB, fast, good quality
                - "all-mpnet-base-v2": 420MB, slower, better quality
        """
        self.model_name = model_name

        if EMBEDDINGS_AVAILABLE:
            print(f"Loading semantic model: {model_name}...")
            self.model = SentenceTransformer(model_name)
            self.use_embeddings = True
        else:
            print("Sentence transformers not available, using TF-IDF fallback")
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.model = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),  # Unigrams and bigrams
                stop_words='english'
            )
            self.use_embeddings = False


    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Convert texts to embeddings.

        Args:
            texts: List of text strings

        Returns:
            Numpy array of embeddings (shape: [num_texts, embedding_dim])
        """
        if self.use_embeddings:
            return self.model.encode(texts)
        else:
            # TF-IDF fallback
            return self.model.fit_transform(texts).toarray()


    def compute_similarity(
        self,
        resume_bullets: List[str],
        job_description: str
    ) -> List[Dict[str, any]]:
        """
        Compute semantic similarity between resume bullets and job description.

        This is the CORE algorithm that makes resuMAX smart!

        Args:
            resume_bullets: List of resume bullet points
            job_description: Job description text

        Returns:
            List of dicts with bullet, score, and ranking

        Example:
            resume_bullets = [
                "Built Python API using FastAPI",
                "Managed team of 5 engineers",
                "Created Excel reports for finance team"
            ]

            job_description = "Backend Engineer - Python, APIs, microservices"

            Returns:
                [
                    {
                        "bullet": "Built Python API using FastAPI",
                        "score": 0.89,  ← Highest! Very relevant
                        "rank": 1
                    },
                    {
                        "bullet": "Managed team of 5 engineers",
                        "score": 0.54,  ← Medium relevance
                        "rank": 2
                    },
                    {
                        "bullet": "Created Excel reports for finance team",
                        "score": 0.21,  ← Low relevance
                        "rank": 3
                    }
                ]
        """

        if not resume_bullets:
            return []

        # Encode job description
        job_embedding = self.encode([job_description])

        # Encode all resume bullets
        bullet_embeddings = self.encode(resume_bullets)

        # Compute cosine similarity between each bullet and job description
        # Cosine similarity: 1.0 = identical, 0.0 = completely different
        similarities = cosine_similarity(bullet_embeddings, job_embedding).flatten()

        # Create results with scores
        results = []
        for i, (bullet, score) in enumerate(zip(resume_bullets, similarities)):
            results.append({
                "bullet": bullet,
                "original_index": i,
                "score": float(score),  # Convert numpy float to Python float
                "rank": 0  # Will be set after sorting
            })

        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)

        # Assign ranks
        for rank, result in enumerate(results, start=1):
            result["rank"] = rank

        return results


    def compute_overall_score(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Compute overall resume-job match score (0-100).

        This tells users: "Your resume is 78% aligned with this job"

        Args:
            resume_text: Full resume text
            job_description: Job description text

        Returns:
            Score from 0-100
        """

        # Encode both texts
        embeddings = self.encode([resume_text, job_description])

        # Compute cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

        # Convert to 0-100 scale
        # Note: Typical similarity scores range 0.3-0.9 for real resumes/jobs
        # We'll normalize to make 0.5 = 50%, 0.8 = 80%, etc.
        score = similarity * 100

        return float(score)


    def get_top_bullets(
        self,
        resume_bullets: List[str],
        job_description: str,
        top_n: int = 10
    ) -> List[str]:
        """
        Get top N most relevant bullets for job description.

        Args:
            resume_bullets: All resume bullets
            job_description: Job description
            top_n: Number of bullets to return

        Returns:
            List of top N bullets (sorted by relevance)
        """

        scored_bullets = self.compute_similarity(resume_bullets, job_description)

        # Return top N bullet texts
        return [item["bullet"] for item in scored_bullets[:top_n]]


    def compare_before_after(
        self,
        original_bullets: List[str],
        optimized_bullets: List[str],
        job_description: str
    ) -> Dict[str, any]:
        """
        Compare original vs optimized resume to show improvement.

        This is what you wanted! Shows user how much better their resume is.

        Args:
            original_bullets: Original resume bullets (unordered)
            optimized_bullets: Optimized resume bullets (reordered)
            job_description: Job description

        Returns:
            Comparison metrics

        Example output:
            {
                "original_score": 68.5,
                "optimized_score": 82.3,
                "improvement": 13.8,
                "improvement_percentage": 20.1,
                "original_top_3_avg": 0.65,
                "optimized_top_3_avg": 0.83,
                "message": "Your resume is now 20% more relevant!"
            }
        """

        # Score original bullets
        original_results = self.compute_similarity(original_bullets, job_description)

        # Score optimized bullets
        optimized_results = self.compute_similarity(optimized_bullets, job_description)

        # Calculate average score for top 3 bullets (what recruiter sees first)
        def avg_top_n(results, n=3):
            top_n_scores = [r["score"] for r in results[:n]]
            return sum(top_n_scores) / len(top_n_scores) if top_n_scores else 0

        original_top_avg = avg_top_n(original_results)
        optimized_top_avg = avg_top_n(optimized_results)

        # Calculate overall scores (0-100)
        original_score = original_top_avg * 100
        optimized_score = optimized_top_avg * 100

        improvement = optimized_score - original_score
        improvement_pct = (improvement / original_score * 100) if original_score > 0 else 0

        # Generate message
        if improvement > 10:
            message = f"🎉 Your resume is now {improvement_pct:.0f}% more relevant!"
        elif improvement > 5:
            message = f"✅ Your resume improved by {improvement_pct:.0f}%"
        elif improvement > 0:
            message = f"Slight improvement: +{improvement_pct:.0f}%"
        else:
            message = "Resume already well-optimized"

        return {
            "original_score": round(original_score, 1),
            "optimized_score": round(optimized_score, 1),
            "improvement": round(improvement, 1),
            "improvement_percentage": round(improvement_pct, 1),
            "original_top_3_avg": round(original_top_avg, 3),
            "optimized_top_3_avg": round(optimized_top_avg, 3),
            "message": message,
            "top_bullets_before": [r["bullet"] for r in original_results[:3]],
            "top_bullets_after": [r["bullet"] for r in optimized_results[:3]]
        }


    def suggest_improvements(
        self,
        resume_bullets: List[str],
        job_description: str,
        threshold: float = 0.5
    ) -> Dict[str, any]:
        """
        Suggest which bullets to keep/remove/improve.

        Args:
            resume_bullets: Resume bullets
            job_description: Job description
            threshold: Minimum score to keep a bullet (default: 0.5)

        Returns:
            Suggestions for improvement

        Example:
            {
                "keep": ["Built Python API", ...],  # Score > 0.7
                "improve": ["Managed team", ...],    # Score 0.5-0.7
                "remove": ["Created Excel reports", ...],  # Score < 0.5
                "suggestions": [
                    "Consider removing bullets with score < 50%",
                    "Add more bullets about Python and APIs"
                ]
            }
        """

        scored = self.compute_similarity(resume_bullets, job_description)

        keep = []
        improve = []
        remove = []

        for item in scored:
            if item["score"] > 0.7:
                keep.append(item["bullet"])
            elif item["score"] > threshold:
                improve.append(item["bullet"])
            else:
                remove.append(item["bullet"])

        # Generate suggestions
        suggestions = []
        if len(remove) > 0:
            suggestions.append(f"Consider removing {len(remove)} low-relevance bullets")
        if len(improve) > 0:
            suggestions.append(f"Try to strengthen {len(improve)} medium-relevance bullets")
        if len(keep) < 5:
            suggestions.append("Add more relevant experience to strengthen your resume")

        return {
            "keep": keep,
            "improve": improve,
            "remove": remove,
            "keep_count": len(keep),
            "improve_count": len(improve),
            "remove_count": len(remove),
            "suggestions": suggestions
        }


# Singleton instance (load model once)
_matcher_instance = None

def get_semantic_matcher() -> SemanticMatcher:
    """Get or create semantic matcher singleton"""
    global _matcher_instance
    if _matcher_instance is None:
        _matcher_instance = SemanticMatcher()
    return _matcher_instance
