# Australian Defence Agents

Type in the criminal charges you've been given, plus your state and court. A team of AI agents running **locally in LM Studio** builds a defence plan under Australian law. Nothing leaves your computer.

> **Not legal advice.** The output is AI-generated general information and may be wrong. Always speak to a lawyer, Legal Aid, or an Aboriginal Legal Service before court.

## The agents

| # | Agent | What it does |
|---|-------|--------------|
| 1 | Charge Analyst | Finds the legislation, maximum penalty, and every element the prosecution has to prove |
| 2 | Defence Strategist | Goes through each element and the available defences, then ranks the strongest arguments |
| 3 | Procedure Reviewer | Looks at the stop, search, arrest, caution, testing procedure and evidence admissibility (e.g. s138), and what to request in the brief |
| 4 | Diversion Advisor | Covers ways to avoid a conviction: withdrawal, diversion, s10 / s12 / s19B dismissals, plea deals |
| 5 | Critic | Checks the team's work for mistakes and gaps |
| 6 | Case Lead | Writes the Defence Strategy Report |

## The Defence Strategy Report

Every run produces a markdown report aimed at getting the charges withdrawn, dismissed or beaten, and failing that, at avoiding a conviction:

1. Charges and elements (legislation, maximum penalty, what must be proved)
2. Primary defence strategy (the single best way out)
3. Ranked defence arguments (legal basis, evidence needed, strength)
4. Getting the charges withdrawn or downgraded (what to put in representations)
5. Evidence to challenge or exclude
6. Fallback options for avoiding a conviction
7. Action plan and timeline
8. Documents and evidence checklist
9. Questions for your lawyer
10. Realistic assessment of each outcome

An appendix includes each agent's full working notes. Reports are saved to `reports/`, and the web UI also has a **Download** button. A full run takes about 10–20 minutes on a 9B model.

It supports NSW, VIC, QLD, WA, SA, TAS, ACT, NT and Commonwealth offences.

## Setup

1. Install [LM Studio](https://lmstudio.ai), load a model, and start the **Local Server** (port 1234).
   It works best with a legal fine-tune, such as an Australian-law fine-tuned model.
2. Install the dependency with `pip install -r requirements.txt`.

## Run

Web UI (http://localhost:8000):

```
python app.py
```

Command line:

```
python cli.py --charges "Drive with middle range PCA" --state NSW --location "Penrith Local Court" --facts "Breath tested 2.5 hours after driving"
```

Options: `--lm-studio-url http://localhost:1234`, `--model <id>` (it auto-detects the loaded model if you leave this out).
