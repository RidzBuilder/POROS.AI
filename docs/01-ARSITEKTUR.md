# POROS.AI — Dokumen Arsitektur Detail
**Versi:** 1.0 | **Status:** Draft untuk review Para JALA | **Penyusun:** Ridz + POROS.AI Design Team

## 1. Visi
POROS.AI adalah **Multiverse AI Agent Operating System**: satu wadah yang mengatur, mengorkestrasi, mengintegrasikan, mensinkronkan, dan mengawasi workflow kumpulan Universe AI Agent beserta output-nya — sampai menghasilkan **Sosial Buzz Ecosystem** yang terukur dan terus berevolusi.

Dua prinsip non-negosiable:
1. **AGENTIC** — setiap agent berinisiatif, goal-driven, ber-memori, self-correcting, dan mampu bernegosiasi antar-agent. Bukan chatbot yang menunggu prompt.
2. **AGNOSTIC** — tidak terkunci pada LLM, platform sosial, marketplace, framework, maupun infrastruktur manapun. Semua dependensi lewat adapter/ports.

## 2. Hierarki Sistem
```
POROS.AI — MULTIVERSE LAYER (The OS)
├─ Agent Factory
├─ Orchestrator & Workflow Engine
├─ LLM Router
├─ Integration Adapters
├─ Evaluation & Evidence Engine
├─ Evolution Controller
└─ Dashboard Para JALA + Layer JALANURIYAH
        │
        ├─ Universe PBC
        ├─ Universe TENTOR HOS
        ├─ Universe Distribution Center
        └─ Universe baru dari Factory
```

Universe AI Agent = bounded context dengan tujuan, persona, memori, dan toolset sendiri. AI Creator Agent = worker terspesialisasi per niche. Ekosistem = 1 akun Toko Utama + N Universe + M akun creator.

## 3. Komponen Inti
### 3.1 Agent Factory
Input Universe Template declarative; output agent instance hidup dengan spec versi + kontrak antar-agent. Kemampuan yang dideklarasikan: spawn, clone, kill, pause, migrate runtime.

### 3.2 Orchestrator & Workflow Engine
Dideklarasikan sebagai event-driven DAG dengan retry, timeout, dead-letter queue, dan human-in-the-loop gate.

### 3.3 LLM Router
Interface vendor-agnostic `generate(task, context, budget_tier) -> completion`.

### 3.4 Integration Adapters
Social, marketplace, dan affiliate adapter dengan ports yang dapat diperluas.

### 3.5 Evaluation & Evidence Engine
Menghitung Sosial Buzz Score dan menyimpan bukti/metrics dalam Evidence Lake.

### 3.6 Evolution Controller
Evaluasi + evidence → Evolution Proposal → perubahan parameter spec → generasi berikutnya.

### 3.7 Dashboard & JALANURIYAH
Monitoring multiverse, approval evolution, marketplace template, leaderboard, benchmark, playbook.

## 4. Workflow Utama
```
PBC → AI Creator → Sosial Buzz awal → TENTOR HOS → AI Content
→ Distribution Center → Value Outcome → Evaluation & Evidence
→ Evolution Creator Loop → kembali ke awal
```

Setiap tahap dideklarasikan menghasilkan event; Evidence Engine mencatat dan Evolution Controller mengubah spec generasi berikutnya.

## 5. Kontrak Antar-Agent
Envelope standar memuat msg_id, sender, receiver, type, goal_ref, payload, deadline, evidence_refs. Agent wajib memahami goal_ref, mempublikasikan artifact + evidence_refs, dan melaporkan kegagalan dengan diagnosis.

## 6. Non-Fungsional
Skala horizontal; state di DB/object storage; vault + RBAC + immutable audit; trace per goal_ref; budget tier; declarative export/import.

## 7. Roadmap
| Fase | Isi |
|---|---|
| 0 | Prototype MVP 1 ekosistem, mock adapter |
| 1 | Adapter nyata + Evidence Lake |
| 2 | Affiliate + Live + full evolution |
| 3 | Agent Factory + template marketplace |
| 4 | JALANURIYAH community/leaderboard/benchmark |
