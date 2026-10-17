# Quick Web Lookup Tool

A small Question-Answer tool that returns a short answer to a search query
using **traditional web search** (no LLM as the primary engine), suitable for
integration into a voice interface.

## Engines

| Name | Working? | Restrictions | Notes |
|---|:---:|---|---|
| DDGS | yes | no rate limits observed | `ddgs` library. 20/20 stress test. Benchmark: 74/100. |
| DDG-HTML | yes | soft | Direct HTML scrape of `html.duckduckgo.com`. **Best coverage: 98/100, 0.77 s.** |
| DDG-InstantAnswer | yes | — | Implemented via `ddgs.text()`. Benchmark: 64/100. |
| DDG-SearchAssist | yes | — | Extended context from top-5 DDGS results. |
| DDG-Snippet (legacy) | no | — | Legacy `api.duckduckgo.com`. Covers encyclopedic entities only. Benchmark: 2/100. |
| Serper | yes | 2500 requests (one-time) | Requires `SERPER_API_KEY`. Google results. |
| GoogleAnswerBox | yes | same key as Serper | Requires `SERPER_API_KEY`. Answer box panel. |
| GoogleKnowledgeGraph | yes | same key as Serper | Requires `SERPER_API_KEY`. Knowledge graph description. |
| GoogleCalculator | yes | same key as Serper | Requires `SERPER_API_KEY`. Math queries. |
| Wolfram Alpha | yes | 2000 requests/month | Requires `WOLFRAM_TOKEN`. |
| SearchAPI | yes | 100 requests/month | Requires `SEARCHAPI_API_KEY`. |
| Google snippet | no | — | Anti-bot + dynamic selectors. |
| Google Custom Search | no | — | Requires key + engine ID; 403 in practice. |
| Brave | no | — | Anti-bot. |
| Startpage | no | — | Best-effort scrape; blocked. |
| Mojeek | no | datacenter IP block | Works only via residential proxy. Selectors verified, but network-level block. |
| Qwant | no | DataDome captcha | HTTP 403 + captcha redirect. Requires residential proxy or Staan API key. |
| Groq | yes | requires `GROQ_API_KEY` | LLM, **not** a search engine. Free tier: 30 RPM / 14 400 RPD. |
| DDG + Groq | yes | requires `GROQ_API_KEY` | Hybrid: DDGS search + Groq summarizer. LLM-generated. |
| GPT-4o (via g4f) | no | — | Provider `CopilotApp` returns HTTP 460. LLM, not search. |
| duck.ai | yes | no key | LLM + web search via `p2d-duck`. Requires `pip install p2d-duck`. |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

Engines that need an API key are skipped automatically if the corresponding
environment variable is empty. So the tool works out of the box with the
keyless engines (DDGS, DDG-HTML, DDG-InstantAnswer, DDG-SearchAssist, duck.ai).
Usage

Quick single query against all engines:
bash

python test_single.py "Столица Исландии"

Interactive mode (asks for a query, prints answers from every engine):
bash

python test.py

Full benchmark — runs all 100 queries from test_data.py against every
available engine and writes benchmark_results.csv:
bash

python benchmark.py

Structure

    base_scraper.py — shared HTTP + HTML/JSON helper (fetch_html, fetch_json,
    parse_selector, parse_multiple_selectors).

    search_duckduckgo.py — DDG HTML scrape as a function-style engine.

    engines/engine.py — abstract Engine base class.

    engines/registry.py — single source of truth for the engine list. Used by
    benchmark.py and test.py.

    engines/ — one file per engine. Each file provides:

        a class with search(self, query, language_code), and

        a module-level search(query, language_code) wrapper.

    test_data.py — 100 test queries across 10 categories, including
    «Сложные/Абстрактные (без быстрого ответа)».

    benchmark.py, test.py, test_single.py — runners.

    REPORT.md — verification report with evidence, benchmark results, and
    documented limitations.

    .env.example — template for API keys.

Test data

test_data.py contains 10 categories × 10 queries:

    География

    Личности (Биография)

    Наука и Техника

    История

    Математика и Расчеты

    Конвертация (Валюты/Меры)

    Культура и Искусство

    Бытовые вопросы

    Сложные/Абстрактные (без быстрого ответа)

    Спорт

The «Сложные/Абстрактные» category is designed to trigger the "no short
answer" case: engines should return empty, not hallucinate.
Benchmark summary

See REPORT.md for the full report and benchmark_results.csv for raw data.

Top results (100 queries):
Engine	Non-empty	Avg time
DDG-HTML	98/100	0.77 s
DDGS	74/100	2.02 s
DDG-InstantAnswer	64/100	2.07 s
DDG-SearchAssist	see REPORT.md	—
duck.ai	see REPORT.md	—
DDG-Snippet (legacy)	2/100	0.22 s
GoogleSnippet / Brave / Startpage	0/100	<0.3 s
GPT-4o (g4f)	0/100	0.40 s
Mojeek / Qwant	blocked	—

Recommended default for voice interface: search_duckduckgo.search
(DDG-HTML) — highest coverage, fastest, no API key, correctly returns empty
for questions without a short answer.
Limitations

    Mojeek and Qwant are blocked for datacenter IPs (empty response and
    DataDome captcha respectively). They require a residential proxy.

    Brave, Startpage, Google snippet use anti-bot protection and
    return empty pages.

    GPT-4o via g4f currently returns HTTP 460 from the CopilotApp
    provider.

    LLM-based engines (Groq, GPT-4o, DDG+Groq, duck.ai) do not meet the
    project requirement "search, not LLM". They are kept only for comparison.
