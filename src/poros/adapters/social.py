"""Integration Adapters — AGNOSTIC.

Port SocialAdapter: publish() & fetch_metrics().
Tambah platform baru = subclass baru. MVP: simulasi deterministik.
"""
from __future__ import annotations

import hashlib
from ..core.models import Distribution, BuzzMetric


class SocialAdapter:
    name = "base"
    def publish(self, plan: dict) -> Distribution:
        raise NotImplementedError
    def fetch_metrics(self, dist: Distribution) -> BuzzMetric:
        raise NotImplementedError


def _seed(*parts) -> int:
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)


class SimulatedSocialAdapter(SocialAdapter):
    """Mengemulasi semua platform sekaligus (agnostic simulation)."""

    def __init__(self, platform: str):
        self.name = platform

    def publish(self, plan: dict) -> Distribution:
        return Distribution(
            artifact_id=plan["artifact_id"],
            platform=self.name,
            account_handle=plan["account_handle"],
            external_id=f"{self.name}_{_seed(plan) % 10**8}",
        )

    def fetch_metrics(self, dist: Distribution) -> BuzzMetric:
        s = _seed(dist.external_id, dist.platform)
        reach = 500 + s % 9500
        likes = int(reach * (0.02 + (s >> 8) % 8 / 100))
        comments = int(likes * 0.15)
        shares = int(likes * 0.25)
        clicks = int(likes * (0.10 + (s >> 12) % 15 / 100))
        sentiment = round(-0.2 + ((s >> 16) % 120) / 100, 2)
        m = BuzzMetric(dist.id, reach, likes, comments, shares, clicks, sentiment)
        m.buzz_score = round(
            0.35 * min(100, reach / 100)
            + 0.25 * min(100, (likes + comments + shares) / 5)
            + 0.25 * min(100, clicks * 2)
            + 0.15 * (sentiment + 1) * 50, 1)
        return m


def get_adapter(platform: str) -> SocialAdapter:
    """Registry agnostic — produksi: load plugin dinamis."""
    return SimulatedSocialAdapter(platform)
