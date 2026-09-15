# POROS.AI — Forensic Baseline

This repository is a frozen experimental control specimen. It separates the supplied package's declared architecture from the capabilities observed in its executable MVP.

## Declared architecture
The supplied architecture describes POROS.AI as a Multiverse AI Agent Operating System with Agent Factory, Orchestrator/Workflow Engine, vendor-agnostic LLM Router, integration adapters, Evaluation & Evidence Engine, Evolution Controller, Dashboard and JALANURIYAH.

It explicitly claims AGENTIC behavior (proactive, goal-driven, memory, self-correction, agent negotiation) and AGNOSTIC integration (LLM/platform/framework/infrastructure independence through adapters/ports).

## Observed executable baseline
`src/poros/orchestrator/engine.py` runs a synchronous cycle: spawn three Universes, build agents, generate a PBC brief, create three creator artifacts, simulate early buzz, curate with TENTOR HOS, build a distribution plan, publish through simulated social adapters, aggregate metrics, evaluate, and apply evolution proposals.

## Key deltas
| Area | Declared | Observed baseline |
|---|---|---|
| Workflow | Event-driven DAG | Synchronous linear orchestrator |
| Agent autonomy | Proactive/self-correcting/negotiating | Agents invoked by orchestrator |
| LLM | Vendor-agnostic | Mock/simulated provider |
| Social | Real adapter ports | Simulated adapter |
| Evidence | Evidence Lake | In-memory runtime evidence/metrics |
| Evolution | New spec / next generation | Proposal applied to runtime objects; cross-cycle inheritance not demonstrated |
| Security | Vault/RBAC/immutable audit | Not implemented in MVP |
| Marketplace | JALANURIYAH | Architectural concept/deck |

These gaps are intentionally preserved. They are part of the experiment and should not be “fixed” before independent abstraction.

## Experimental question
> How does an independent AI system abstract the architecture that naturally emerges from this artifact before it is told what AOS/DNA-AOS says it should be?
