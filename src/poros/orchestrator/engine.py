"""Orchestrator — menjalankan workflow utama multiverse dalam satu siklus."""
from __future__ import annotations
from ..core.models import Message, dump
from ..core.llm_router import LLMRouter
from ..factory.universe_factory import UniverseFactory
from ..adapters.social import get_adapter
from ..eval.buzz import aggregate_buzz, evaluate, propose_evolution

class Orchestrator:
    def __init__(self):
        self.router = LLMRouter()
        self.factory = UniverseFactory(self.router)
        self.cycle_no = 0
        self.report = {}
    def run_cycle(self, template: dict) -> dict:
        self.cycle_no += 1
        niche = template.get("niche", "umum"); goal = template.get("goal", {"target_buzz": 80}); log=[]
        u_pbc, ag_pbc = self.factory.spawn_universe(template["universes"]["pbc"], "eco-demo")
        u_hos, ag_hos = self.factory.spawn_universe(template["universes"]["tentor_hos"], "eco-demo")
        u_dis, ag_dis = self.factory.spawn_universe(template["universes"]["distribution_center"], "eco-demo")
        log.append(f"[factory] 3 universe lahir ({u_pbc.id}, {u_hos.id}, {u_dis.id})")
        agents={a.spec.role:self.factory.build_agent(a) for a in ag_pbc+ag_hos+ag_dis}
        pbc=agents["pbc"]
        brief_art=pbc.run_brief(pbc.receive(Message(sender="jala/ridz",receiver=f"universe/{u_pbc.id}/pbc",type="brief",goal_ref="eco-demo/goal",payload={"niche":niche})))
        brief=brief_art.body; log.append(f"[pbc] brief: {brief['trend']}")
        creations=[]
        for role in ("creator_content","creator_affiliate","creator_live"):
            a=agents[role]
            art=a.run_produce(a.receive(Message(sender=pbc.inst.id,receiver=f"{u_pbc.id}/{role}",type="produce",goal_ref="eco-demo/goal",payload={"topic":brief["trend"],"niche":niche})))
            creations.append(dump(art)); log.append(f"[{role}] artifact {art.id}")
        early_buzz=self._simulate(creations,niche,"early")
        hos=agents["tentor_hos"]
        curated=hos.run_curate(hos.receive(Message(sender=u_pbc.id,receiver=f"universe/{u_hos.id}/hos",type="curate",goal_ref="eco-demo/goal",payload={"artifacts":creations,"topic":brief["trend"],"niche":niche,"avg_buzz":early_buzz})))
        log.append(f"[hos] lolos kurasi: {curated.body['passed']}")
        dist=agents["distributor"]
        plan_art=dist.run_distribute(dist.receive(Message(sender=u_hos.id,receiver=f"universe/{u_dis.id}/dist",type="repurpose",goal_ref="eco-demo/goal",payload={"artifacts":[c for c in creations if c["id"] in curated.body["passed"]],"niche":niche,"account_handle":template.get("account_handle","@toko_utama")})))
        plan=plan_art.body["distribution_plan"]; log.append(f"[dist] {len(plan)} titik distribusi: {sorted(set(p['platform'] for p in plan))}")
        metrics=[]; per_platform={}
        for p in plan:
            d=get_adapter(p["platform"]).publish(p); m=get_adapter(p["platform"]).fetch_metrics(d); metrics.append(m); per_platform.setdefault(p["platform"],[]).append(m)
        value_buzz=aggregate_buzz(metrics); log.append(f"[buzz] Sosial Buzz terukur: {value_buzz}/100 (target {goal.get('target_buzz',80)})")
        ev=evaluate(self.cycle_no,goal,metrics,per_platform); log.append(f"[eval] verdict={ev.verdict} | bukti={len(ev.evidence_pack)} metrik")
        proposals=propose_evolution(ev,ag_pbc+ag_hos+ag_dis); applied=[]; all_agents=ag_pbc+ag_hos+ag_dis
        for prop in proposals:
            if prop.target_agent_id=="factory":
                u_clone,_=self.factory.clone_universe(u_pbc,all_agents); applied.append(f"clone_universe -> {u_clone.id}"); continue
            target=next((a for a in all_agents if a.id==prop.target_agent_id),None)
            if target:
                self.factory.apply_evolution(target,prop); prop.status="applied"; applied.append(f"{target.spec.role} v{target.spec_version} (+{prop.predicted_delta})")
        log.append(f"[evolution] applied: {applied}")
        self.report={"cycle":self.cycle_no,"niche":niche,"brief_trend":brief["trend"],"creations":len(creations),"distributions":len(plan),"platforms":sorted(per_platform),"early_buzz":early_buzz,"value_buzz":value_buzz,"target":goal.get("target_buzz",80),"verdict":ev.verdict,"evolution_applied":applied,"log":log}
        return self.report
    def _simulate(self,artifacts,niche,stage):
        from ..adapters.social import SimulatedSocialAdapter
        tmp=SimulatedSocialAdapter("early-signal")
        ms=[tmp.fetch_metrics(tmp.publish({"artifact_id":a["id"],"account_handle":"@creator","platform":stage})) for a in artifacts]
        return aggregate_buzz(ms)
