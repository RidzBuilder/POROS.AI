# POROS.AI — Desain Database & Skema Agent
**Versi:** 1.0 | **Target DB:** PostgreSQL 15+ (JSONB untuk agnostic config)

## 1. Prinsip
- Declarative + vendor-neutral JSONB.
- Evidence-first.
- Soft-delete + audit log.

## 2. ER Ringkas
```
jala → ecosystem → universe → agent_instance → task → artifact
                         ├→ agent_memory / agent_state
artifact → distribution → buzz_metric
evaluation → evolution_proposal
audit_log
```

## 3. DDL
The supplied design defines PostgreSQL tables for jala, ecosystem, account, universe_template, universe, agent_instance, agent_memory, agent_state, task, artifact, distribution, buzz_metric, evaluation, evolution_proposal, and immutable audit_log. Configuration and evidence are modeled with JSONB.

## 4. Agent schema
```json
{
  "llm": { "provider": "any-openai-compatible", "model_tier": "frugal" },
  "platforms": ["tiktok", "instagram"],
  "schedule": { "posts_per_day": 3, "best_hours": [11, 19, 21] },
  "tools": ["search_trends", "publish", "fetch_metrics"]
}
```

Persona includes expertise, tone, forbidden claims, and memory policy.

## 5. Key indexes
Indexes are declared for agent_instance(universe_id, role), task(universe_id, status), buzz_metric(distribution_id, captured_at DESC), and evaluation(ecosystem_id, cycle_no DESC).
