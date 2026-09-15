"""LLM Router — lapisan AGNOSTIC.

Port: cukup implementasikan `generate(task_type, context) -> str`.
Router memilih provider berdasarkan budget_tier agen:
  - frugal    -> produksi massal (caption, varian)
  - standard  -> repurposing, script live
  - premium   -> kurasi TENTOR HOS, evaluasi, evolution reasoning
"""
from __future__ import annotations

import hashlib
from typing import Protocol


class LLMProvider(Protocol):
    name: str
    def generate(self, task_type: str, context: dict) -> str: ...


class MockLLM:
    """Provider lokal deterministik untuk MVP — tanpa jaringan, tanpa biaya."""

    def __init__(self, name: str = "mockllm"):
        self.name = name

    def generate(self, task_type: str, context: dict) -> str:
        niche = context.get("niche", "umum")
        topic = context.get("topic", niche)
        persona_tone = (context.get("persona") or {}).get("tone", ["netral"])
        tone = persona_tone[0] if isinstance(persona_tone, list) else str(persona_tone)

        templates = {
            "brief": (
                f"[BRIEF PBC] Niche '{niche}'. Angle: edukasi ringan + bukti sosial. "
                f"Tone {tone}. Target: 3 konten/hari. Sinyal tren: {context.get('trend', 'stabil')}."
            ),
            "caption": (
                f"[{niche.upper()}] 3 hal soal {topic} yang jarang dibahas — no. 2 bikin kaget. "
                f"Komen 'MAU' untuk checklist lengkapnya. #JALANURIYAH #{niche.replace(' ', '')}"
            ),
            "affiliate_hook": (
                f"[HOOK AFFILIATE] Berapa lama kamu pakai {topic} yang salah? "
                f"Cek keranjang kuning — aku taruh yang worth it (link affiliate)."
            ),
            "live_script": (
                f"[LIVE SCRIPT] Opening 10 detik: 'Stop scroll! {topic} versi hemat tapi aman.' "
                f"Demo -> bukti before/after -> jawab 3 komen -> CTA affiliate."
            ),
            "curate": (
                f"[TENTOR HOS] Nilai konten: relevansi niche {niche}=8/10, kejujuran klaim=9/10, "
                f"CTA=6/10. Saran: perkuat bukti + CTA. Topik lanjutan: '{topic} untuk pemula'."
            ),
            "repurpose": (
                f"[REPURPOSE] Pecah jadi: 1 carousel edukasi, 1 short video, 1 thread X. "
                f"Fokus pada '{topic}' dengan angle {tone}."
            ),
            "evaluate": (
                f"[EVAL] Buzz {context.get('buzz', 0):.1f}/100 vs target "
                f"{context.get('target', 80)}. {context.get('note', 'lanjutkan pola saat ini')}."
            ),
        }
        base = templates.get(task_type, f"[{task_type}] konten niche {niche} tentang {topic}.")
        h = int(hashlib.md5(str(sorted(context.items())).encode()).hexdigest(), 16)
        return f"{base} (ref:{h % 10000:04d})"


class OpenAICompatible:
    """Contoh provider nyata (agnostic) — aktifkan saat fase produksi."""

    def __init__(self, name: str, base_url: str, api_key_env: str, model: str):
        self.name = name
        self.base_url = base_url
        self.api_key_env = api_key_env
        self.model = model

    def generate(self, task_type: str, context: dict) -> str:
        raise NotImplementedError("Aktifkan saat fase produksi; MVP memakai MockLLM.")


TIER_ROUTE = {"frugal": "mock-frugal", "standard": "mock-standard", "premium": "mock-premium"}


class LLMRouter:
    def __init__(self, providers: dict[str, LLMProvider] | None = None):
        self.providers = providers or {
            "mock-frugal": MockLLM("mock-frugal"),
            "mock-standard": MockLLM("mock-standard"),
            "mock-premium": MockLLM("mock-premium"),
        }

    def generate(self, task_type: str, context: dict, budget_tier: str = "standard") -> str:
        provider = self.providers[TIER_ROUTE.get(budget_tier, "mock-standard")]
        return provider.generate(task_type, context)
