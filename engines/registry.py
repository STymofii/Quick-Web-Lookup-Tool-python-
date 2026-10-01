"""Single source of truth for the list of available engines.

Engines that require an API key are skipped when the corresponding
environment variable is not set.

Mojeek and Qwant are excluded from the active list because they block
requests from datacenter IPs (Mojeek) or use DataDome captcha (Qwant).
Their implementations remain in the repo as documented best-effort attempts.
"""
import os

import search_duckduckgo

from engines.ddgs_engine import DDGS_Engine
from engines.ddg_snippet import DDG_Snippet
from engines.ddg_instant_answer import DDG_Instant_Answer
from engines.ddg_search_assist import DDG_Search_Assist
from engines.gpt_engine import GPT_Engine
from engines.google_snippet import GoogleSnippet
from engines.brave_snippet import BraveEngine
from engines.qwant_snippet import QwantSnippet
from engines.startpage_snippet import StartpageSnippet
from engines.mojeek_snippet import MojeekSnippet
from engines.duck_ai import DuckAI

from engines.serper_engine import Serper_Engine
from engines.google_answer_box import GoogleAnswerBox
from engines.google_knowledge_graph import GoogleKnowledgeGraph
from engines.google_calculator import GoogleCalculator
from engines.wolfram_engine import Wolfram_Engine
from engines.searchapi_engine import SearchAPI_Engine
from engines.groq_engine import GroqEngine
from engines.ddg_groq_engine import DDG_Groq_Engine


def get_engines() -> list[tuple[str, callable]]:
    engines: list[tuple[str, callable]] = []

    # ---- No API key required ----
    engines.append(("DDGS", DDGS_Engine().search))
    engines.append(("DDG-HTML", search_duckduckgo.search))
    engines.append(("DDG-InstantAnswer", DDG_Instant_Answer().search))
    engines.append(("DDG-SearchAssist", DDG_Search_Assist().search))
    engines.append(("DDG-Snippet-deprecated", DDG_Snippet().search))
    engines.append(("GoogleSnippet", GoogleSnippet().search))
    engines.append(("Brave", BraveEngine().search))
    engines.append(("Startpage", StartpageSnippet().search))
    engines.append(("duck.ai", DuckAI().search))
    engines.append(("GPT-4o", GPT_Engine().search))

    # Mojeek and Qwant are intentionally excluded from the active list.
    # See REPORT.md for the blocking evidence.

    # ---- Require API keys ----
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key:
        engines.append(("Serper", Serper_Engine(serper_key).search))
        engines.append(("GoogleAnswerBox", GoogleAnswerBox(serper_key).search))
        engines.append(("GoogleKnowledgeGraph", GoogleKnowledgeGraph(serper_key).search))
        engines.append(("GoogleCalculator", GoogleCalculator(serper_key).search))

    wolfram_key = os.getenv("WOLFRAM_TOKEN")
    if wolfram_key:
        engines.append(("Wolfram", Wolfram_Engine(wolfram_key).search))

    searchapi_key = os.getenv("SEARCHAPI_API_KEY")
    if searchapi_key:
        engines.append(("SearchAPI", SearchAPI_Engine(searchapi_key).search))

    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        engines.append(("Groq", GroqEngine(groq_key).search))
        engines.append(("DDG+Groq", DDG_Groq_Engine(groq_key).search))

    return engines
