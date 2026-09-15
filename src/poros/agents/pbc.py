"""Universe PBC — Personal Branding Creator.

Tugas: merumuskan brief brand/persona, membaca sinyal tren niche,
lalu memicu Creator Content / Affiliate / Live secara proaktif (agentic).
"""
from __future__ import annotations

from .base import BaseAgent


class PBCAgent(BaseAgent):
    ROLE = "pbc"

    def run_brief(self, task):
        niche = task.input.get("niche", "umum")
        trend = self.detect_trend(niche)
        self.remember("niche", niche)
        self.remember("last_trend", trend)
        brief = self.think(task, "brief", {"trend": trend, "niche": niche})
        return self.produce(task, "brief", {
            "brief": brief,
            "trend": trend,
            "assignments": [
                {"role": "creator_content", "topic": trend, "goal_ref": task.input.get("goal_ref")},
                {"role": "creator_affiliate", "topic": trend, "goal_ref": task.input.get("goal_ref")},
                {"role": "creator_live", "topic": trend, "goal_ref": task.input.get("goal_ref")},
            ],
        })

    def detect_trend(self, niche: str) -> str:
        """Proaktif: sinyal pasar sederhana (di produksi: search_trends tool)."""
        trends = {
            "skincare": "sunscreen hybrid moisturizer",
            "gadget": "powerbank mini 10000mAh",
            "kuliner": "rice bowl frozen 5 menit",
            "fashion": "oversized shirt earth tone",
        }
        return trends.get(niche, f"tren terbaru {niche}")
