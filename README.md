# Composio App Research Intelligence

An automated research pipeline exploring the integration potential of 100 applications for AI agent toolkits.

## Live Demo

**Dashboard:** https://composio-app-research-intelligence.vercel.app/

**Source Code:** https://github.com/WildStone007/composio-app-research-intelligence

## Overview

This project investigates 100 applications across 10 categories to understand their suitability for AI agent integrations.

The research covers:

- Application categories and descriptions
- Authentication methods
- Developer access and credential requirements
- REST and GraphQL API signals
- MCP availability signals
- Integration buildability and potential blockers
- Documentation and evidence URLs

## Architecture and Workflow

1. **Application dataset:** 100 applications across 10 categories.
2. **Discovery:** DuckDuckGo searches using the DDGS Python library.
3. **Extraction:** Python-based rule-driven classification of search results.
4. **Storage:** Research records saved as JSON.
5. **Verification:** Official documentation URL reachability checks and sample-based comparison.
6. **Presentation:** Interactive HTML research dashboard.

Human review remains necessary for ambiguous or unsupported findings.

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
git clone https://github.com/WildStone007/composio-app-research-intelligence.git
cd composio-app-research-intelligence

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the Research Pipeline

```bash
python src/research.py
```

To research a limited batch:

```bash
python src/research.py --limit 10
```

The pipeline saves research records in `output/research.json` and supports resuming an existing run.

## Generate the Dashboard

```bash
python src/dashboard.py
open output/index.html
```

## Verification Results

A six-application sample was compared against expected authentication signals.

- Sample size: 6 applications
- Authentication signal overlaps: 3
- Non-overlaps: 3
- Signal overlap rate: 50%

This is a keyword-signal overlap rate, **not an overall accuracy score**.

The source-check script tested 12 documentation URLs, of which 12 responded successfully to HTTP checks. Reachability does not establish that the page content is accurate or that an integration is available.

## Findings and Limitations

The research run returned at least one search result for 93 of the 100 applications. These are discovery results, not 93 verified integrations.

- Search results can be incomplete or outdated.
- Authentication extraction is keyword-based.
- API breadth and buildability require deeper documentation review.
- MCP mentions do not prove official or functional MCP support.
- All application records remain flagged for human review.
- The pipeline does not execute API calls against all 100 applications.
- This version uses a Python rule-based research pipeline; it does not implement a Composio-powered agent or MCP execution workflow.

## Cost

The current research pipeline does not require OpenAI API credits. It uses public web search and local Python processing.

## Outputs

The primary output is the interactive dashboard at `output/index.html`, with supporting research and verification data in the `output/` directory.
