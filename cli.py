"""
Command line:
  python cli.py --charges "Drive with mid range PCA" --state NSW --location "Penrith Local Court" \
                --facts "Breath test 40 min after driving..." --out report.md
"""
import argparse

from agents import DISCLAIMER, Case, run_case

p = argparse.ArgumentParser()
p.add_argument("--charges", required=True)
p.add_argument("--state", default="NSW")
p.add_argument("--location", default="")
p.add_argument("--facts", default="")
p.add_argument("--age", default="")
p.add_argument("--priors", default="")
p.add_argument("--lm-studio-url", default="http://localhost:1234")
p.add_argument("--model", default=None)
p.add_argument("--out", default=None, help="write markdown report here")
a = p.parse_args()

case = Case(a.charges, a.state, a.location, a.facts, a.age, a.priors)
result = run_case(case, a.lm_studio_url, a.model,
                  on_step=lambda n, t: print(f"\n===== {n} =====\n{t}\n", flush=True))

if a.out:
    md = [f"# Defence analysis\n\n> {DISCLAIMER}\n\n```\n{case.describe()}\n```\n"]
    md += [f"## {s['agent']}\n\n{s['output']}\n" for s in result["steps"]]
    open(a.out, "w", encoding="utf-8").write("\n".join(md))
    print(f"Saved {a.out}")
