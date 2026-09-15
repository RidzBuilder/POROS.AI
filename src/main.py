"""Demo POROS.AI MVP — jalankan: python src/main.py

Menjalankan 3 siklus workflow multiverse pada 1 ekosistem niche skincare,
lalu menampilkan laporan Evolution Creator Loop.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from poros.orchestrator.engine import Orchestrator


def main():
    template = json.loads((Path(__file__).parent / "config" / "universe_template.example.json").read_text())
    orch = Orchestrator()

    print("=" * 64)
    print("POROS.AI — Multiverse AI Agent OS | Demo MVP")
    print("Para JALA: Ridz | Komunitas: JALANURIYAH")
    print("=" * 64)

    for cycle in range(1, 4):
        r = orch.run_cycle(template)
        print(f"\n--- CYCLE {r['cycle']} | niche: {r['niche']} ---")
        for line in r["log"]:
            print("  " + line)
        print(f"  => Buzz: {r['early_buzz']} (awal) -> {r['value_buzz']}/100 "
              f"(outcome) | verdict: {r['verdict'].upper()}")

    print("\n" + "=" * 64)
    print("RINGKASAN EVOLUTION CREATOR LOOP")
    print("=" * 64)
    print(json.dumps({k: v for k, v in r.items() if k != "log"}, indent=2, ensure_ascii=False))
    print("\nSelesai. Sistem berevolusi otomatis — multiverse menciptakan universe.")


if __name__ == "__main__":
    main()
