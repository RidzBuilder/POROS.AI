"""Universe TENTOR HOS — kurasi, penilaian kualitas, topik lanjutan."""
from __future__ import annotations

from .base import BaseAgent


class TentorHosAgent(BaseAgent):
    ROLE = "tentor_hos"

    def run_curate(self, task):
        artifacts = task.input.get("artifacts", [])
        scores = {}
        for art in artifacts:
            # Penilaian heuristik (produksi: LLM premium + rubric)
            body = str(art.get("body", ""))
            score = min(10, 6 + len(body) // 60)
            scores[art.get("id", "?")] = score
        critique = self.think(task, "curate", {"buzz": task.input.get("avg_buzz", 0)})
        self.remember("last_scores", scores)
        return self.produce(task, "curated_content", {
            "scores": scores,
            "critique": critique,
            "passed": [aid for aid, s in scores.items() if s >= 7],
            "next_topics": [task.input.get("topic", ""), "versi untuk pemula", "mitos vs fakta"],
        })
