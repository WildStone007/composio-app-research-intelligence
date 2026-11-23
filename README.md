# Composio App Research Intelligence

An automated research pipeline evaluating 100 applications for AI agent toolkit integration.

## Overview

The project researches:
- Application categories and descriptions
- Authentication methods
- Developer access and credential requirements
- REST and GraphQL API signals
- MCP availability signals
- Integration buildability and blockers
- Documentation and evidence URLs

## Architecture

1. Application dataset: 100 applications across 10 categories.
2. Discovery: DuckDuckGo search through the DDGS Python library.
3. Extraction: Python rule-based classification.
4. Storage: JSON research records.
5. Verification: Official documentation source checks and human-review flags.
6. Presentation: Interactive HTML research dashboard.

## Project Structure

```text
composio-research-agent/
├── data/
│   └── apps.json
├── src/
│   ├── research.py
│   ├── dashboard.py
│   ├── verification.py
│   └── source_check.py
├── output/
│   ├── research.json
│   ├── verification.json
│   ├── verification_report.md
│   └── index.html
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone YOUR_REPOSITORY_URL
cd composio-research-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Research

```bash
python src/research.py
```

Resume or research a limited batch:

```bash
python src/research.py --limit 10
```

## Generate Dashboard

```bash
python src/dashboard.py
open output/index.html
```

## Verification

```bash
python src/verification.py
python src/source_check.py
```

Search evidence and HTTP reachability are not equivalent to factual verification. Human review is required before treating findings as confirmed.

## Limitations

- Search results can be incomplete or outdated.
- Authentication extraction is keyword-based.
- API breadth and buildability require deeper documentation review.
- MCP mentions are not proof of official or functional MCP support.
- No overall accuracy percentage is claimed.
- The current research engine does not execute API calls against all 100 applications.

## Cost

The current research pipeline does not require OpenAI API credits. It uses public web search and local Python processing.

## Outputs

The generated dashboard is available at `output/index.html`.
