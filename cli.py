"""
Command line:
  python cli.py --charges "Drive with mid range PCA" --state NSW --location "Penrith Local Court" \
                --facts "Breath test 40 min after driving..." --out report.md
"""
import argparse

from datetime import datetime
from pathlib import Path

from agents import Case, build_report, run_case

p = argparse.ArgumentParser()
p.add_argument("--charges", required=True)
p.add_argument("--state", default="NSW")
p.add_argument("--location", default="")
p.add_argument("--facts", default="")
p.add_argument("--age", default="")
p.add_argument("--priors", default="")
p.add_argument("--lm-studio-url", default="http://localhost:1234")
p.add_argument("--model", default=None)
p.add_argument("--out", default=None, help="report path (default: reports/defence_report_<time>.md)")
a = p.parse_args()

case = Case(a.charges, a.state, a.location, a.facts, a.age, a.priors)
result = run_case(case, a.lm_studio_url, a.model,
                  on_step=lambda n, t: print(f"\n===== {n} =====\n{t}\n", flush=True))

out = Path(a.out or f"reports/defence_report_{datetime.now():%Y%m%d_%H%M%S}.md")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(build_report(case, result), encoding="utf-8")
print(f"\nDefence strategy report saved: {out}")
