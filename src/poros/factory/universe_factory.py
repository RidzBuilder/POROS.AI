"""Agent Factory — kemampuan 'multiverse menciptakan universe'."""
from __future__ import annotations
import copy
from ..core.models import Universe, AgentSpec, AgentInstance
from ..core.llm_router import LLMRouter
from ..agents.base import BaseAgent
from ..agents.pbc import PBCAgent
from ..agents.creators import CreatorContentAgent, CreatorAffiliateAgent, CreatorLiveAgent
from ..agents.hos import TentorHosAgent
from ..agents.distribution import DistributionCenterAgent

AGENT_CLASSES = {
    "pbc": PBCAgent,
    "creator_content": CreatorContentAgent,
    "creator_affiliate": CreatorAffiliateAgent,
    "creator_live": CreatorLiveAgent,
    "tentor_hos": TentorHosAgent,
    "ai_content": CreatorContentAgent,
    "distributor": DistributionCenterAgent,
}

class UniverseFactory:
    def __init__(self, router: LLMRouter):
        self.router = router
    def spawn_universe(self, template: dict, ecosystem_id: str = ""):
        u = Universe(kind=template["kind"], goal=template.get("goal", {}), ecosystem_id=ecosystem_id)
        agents = []
        for spec_dict in template["agents"]:
            spec = AgentSpec(**spec_dict)
            agents.append(AgentInstance(spec=spec, universe_id=u.id))
        return u, agents
    def clone_universe(self, universe, agents, overrides=None):
        tpl = {"kind": universe.kind, "goal": copy.deepcopy(universe.goal),
               "agents": [copy.deepcopy(vars(a.spec)) | (overrides or {}) for a in agents]}
        return self.spawn_universe(tpl, ecosystem_id=universe.ecosystem_id)
    def apply_evolution(self, inst, proposal):
        for k, v in (proposal.changes.get("persona") or {}).items(): inst.spec.persona[k] = v
        for k, v in (proposal.changes.get("config") or {}).items(): inst.spec.config[k] = v
        inst.spec_version += 1; inst.status = "idle"; return inst
    def build_agent(self, inst):
        return AGENT_CLASSES.get(inst.spec.role, BaseAgent)(inst, self.router)
