"""AI Creator Agents: Content, Affiliate, Live — sesuai niche masing-masing."""
from __future__ import annotations

from .base import BaseAgent


class CreatorContentAgent(BaseAgent):
    ROLE = "creator_content"

    def run_produce(self, task):
        caption = self.think(task, "caption")
        self.remember("last_topic", task.input.get("topic"))
        return self.produce(task, "content_draft", {
            "caption": caption,
            "format": task.input.get("format", "short_video"),
            "hooks": [caption.split(".")[0]],
        })


class CreatorAffiliateAgent(BaseAgent):
    ROLE = "creator_affiliate"

    def run_produce(self, task):
        hook = self.think(task, "affiliate_hook")
        return self.produce(task, "content_draft", {
            "hook": hook,
            "cta": "keranjang kuning",
            "link_type": "affiliate",
        })


class CreatorLiveAgent(BaseAgent):
    ROLE = "creator_live"

    def run_produce(self, task):
        script = self.think(task, "live_script")
        return self.produce(task, "live_script", {
            "script": script,
            "duration_min": task.input.get("duration_min", 30),
            "best_hours": self.inst.spec.config.get("schedule", {}).get("best_hours", [19, 21]),
        })
