"""Evaluation & Evidence Engine -> Evolution Creator Loop."""
from __future__ import annotations

from ..core.models import BuzzMetric, Evaluation, EvolutionProposal


def aggregate_buzz(metrics: list[BuzzMetric]) -> float:
    if not metrics:
        return 0.0
    return round(sum(m.buzz_score for m in metrics) / len(metrics), 1)


def evaluate(cycle_no: int, goal: dict, metrics: list[BuzzMetric],
             per_platform: dict[str, list[BuzzMetric]]) -> Evaluation:
    avg = aggregate_buzz(metrics)
    target = goal.get("target_buzz", 80)
    best_platform = max(per_platform, key=lambda p: aggregate_buzz(per_platform[p]), default="-")
    if avg >= target:
        verdict = "grow"
    elif avg >= target * 0.6:
        verdict = "hold"
    elif avg >= target * 0.3:
        verdict = "fix"
    else:
        verdict = "kill"
    return Evaluation(
        cycle_no=cycle_no,
        summary={"avg_buzz": avg, "target": target, "best_platform": best_platform,
                 "n_distributions": len(metrics)},
        verdict=verdict,
        evidence_pack=[vars(m) for m in metrics],
    )


def propose_evolution(ev: Evaluation, agents: list) -> list[EvolutionProposal]:
    proposals = []
    avg = ev.summary["avg_buzz"]
    if ev.verdict in ("fix", "hold"):
        for a in agents:
            if a.spec.role.startswith("creator"):
                freq = a.spec.config.get("schedule", {}).get("posts_per_day", 3)
                delta = round((ev.summary["target"] - avg) / 50, 2)
                proposals.append(EvolutionProposal(
                    target_agent_id=a.id,
                    changes={"config": {"schedule": {"posts_per_day": freq + 1}},
                             "persona": {"tone": ["lebih berani"]}},
                    predicted_delta=delta,
                    reason=f"Buzz {avg} < target; naikkan volume + tegas tone.",
                ))
    if ev.verdict == "grow":
        proposals.append(EvolutionProposal(
            target_agent_id="factory",
            changes={"action": "clone_universe", "reason": "pola terbukti, perbanyak"},
            predicted_delta=1.0,
            reason="Verdict GROW: siapkan clone universe.",
        ))
    return proposals
