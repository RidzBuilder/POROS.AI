"""Base class agent POROS.AI — agentic: punya memori, goal, self-report."""
from __future__ import annotations

from ..core.models import AgentInstance, Task, Artifact, Message
from ..core.llm_router import LLMRouter


class BaseAgent:
    ROLE = "base"

    def __init__(self, instance: AgentInstance, router: LLMRouter):
        self.inst = instance
        self.router = router

    # -- agentic primitives ------------------------------------------------
    def remember(self, key: str, value):
        """Memori jangka panjang agent (agent_memory di produksi)."""
        self.inst.memory[key] = value

    def recall(self, key: str, default=None):
        return self.inst.memory.get(key, default)

    def receive(self, msg: Message) -> Task:
        """Terima envelope -> jadikan Task. Agent 'paham goal_ref'."""
        self.inst.status = "working"
        return Task(
            type=msg.type if msg.type in ("brief", "produce", "curate", "repurpose", "distribute", "evaluate") else "produce",
            input={"goal_ref": msg.goal_ref, "sender": msg.sender, **msg.payload},
            agent_id=self.inst.id,
            universe_id=self.inst.universe_id,
            idempotency_key=msg.msg_id,
        )

    def think(self, task: Task, task_type: str, extra: dict | None = None) -> str:
        ctx = {
            "niche": task.input.get("niche", self.recall("niche", "umum")),
            "topic": task.input.get("topic", self.recall("topic", "")),
            "persona": self.inst.spec.persona,
            "memory": {k: v for k, v in list(self.inst.memory.items())[-5:]},
        }
        if extra:
            ctx.update(extra)
        return self.router.generate(task_type, ctx, self.inst.spec.budget_tier)

    def produce(self, task: Task, kind: str, body: dict) -> Artifact:
        self.inst.status = "idle"
        return Artifact(kind=kind, body=body, task_id=task.id, agent_id=self.inst.id,
                        evidence_refs=[f"task:{task.id}"])

    def fail(self, task: Task, reason: str) -> dict:
        """Agentic: lapor kegagalan + diagnosis, bukan diam."""
        self.inst.status = "idle"
        return {"task": task.id, "status": "failed", "diagnosis": reason, "agent": self.inst.id}
