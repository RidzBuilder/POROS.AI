"""Universe Distribution Center — Cross-Platform Targeted (agnostic via adapters)."""
from __future__ import annotations

from .base import BaseAgent


class DistributionCenterAgent(BaseAgent):
    ROLE = "distributor"

    def run_distribute(self, task):
        artifacts = task.input.get("artifacts", [])
        platforms = self.inst.spec.config.get("platforms", ["tiktok", "instagram", "x"])
        best_hours = self.inst.spec.config.get("schedule", {}).get("best_hours", [11, 19, 21])
        plan = []
        for art in artifacts:
            for p in platforms:
                plan.append({
                    "artifact_id": art.get("id"),
                    "platform": p,
                    "account_handle": task.input.get("account_handle", f"@{self.inst.universe_id}"),
                    "scheduled_hour": best_hours[len(plan) % len(best_hours)],
                    "targeting": task.input.get("niche", "umum"),
                })
        self.remember("last_plan_size", len(plan))
        return self.produce(task, "repurpose", {"distribution_plan": plan})
