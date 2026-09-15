"""Model inti POROS.AI — netral vendor, hanya stdlib.

Semua konfigurasi agent bersifat declarative (dict) agar AGNOSTIC:
bisa dipindah antar LLM, platform, dan runtime.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


def new_id() -> str:
    return str(uuid.uuid4())[:8]


@dataclass
class Message:
    msg_id: str = field(default_factory=new_id)
    sender: str = ""
    receiver: str = ""
    type: str = "brief"
    goal_ref: str = ""
    payload: dict = field(default_factory=dict)
    deadline: Optional[str] = None
    evidence_refs: list = field(default_factory=list)


@dataclass
class AgentSpec:
    role: str
    persona: dict = field(default_factory=dict)
    config: dict = field(default_factory=dict)
    budget_tier: str = "standard"


@dataclass
class AgentInstance:
    spec: AgentSpec
    id: str = field(default_factory=new_id)
    universe_id: str = ""
    status: str = "idle"
    memory: dict = field(default_factory=dict)
    spec_version: int = 1


@dataclass
class Universe:
    kind: str
    goal: dict = field(default_factory=dict)
    id: str = field(default_factory=new_id)
    ecosystem_id: str = ""
    spec_version: int = 1


@dataclass
class Task:
    type: str
    input: dict = field(default_factory=dict)
    id: str = field(default_factory=new_id)
    agent_id: str = ""
    universe_id: str = ""
    status: str = "queued"
    idempotency_key: str = ""


@dataclass
class Artifact:
    kind: str
    body: dict = field(default_factory=dict)
    id: str = field(default_factory=new_id)
    task_id: str = ""
    agent_id: str = ""
    evidence_refs: list = field(default_factory=list)


@dataclass
class Distribution:
    artifact_id: str
    platform: str
    account_handle: str
    id: str = field(default_factory=new_id)
    external_id: str = ""


@dataclass
class BuzzMetric:
    distribution_id: str
    impressions: int
    likes: int
    comments: int
    shares: int
    clicks: int
    sentiment: float
    buzz_score: float = 0.0


@dataclass
class Evaluation:
    cycle_no: int
    summary: dict
    verdict: str
    evidence_pack: list = field(default_factory=list)
    id: str = field(default_factory=new_id)


@dataclass
class EvolutionProposal:
    changes: dict
    predicted_delta: float
    target_agent_id: str = ""
    status: str = "pending"
    reason: str = ""
    id: str = field(default_factory=new_id)


def dump(obj: Any) -> dict:
    return asdict(obj)
