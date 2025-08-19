from .external_integrations import ExaWebsetsClient, GeminiSummarizer

# Replace the following IDs with your actual Exa Webset IDs
WEBSET_IDS = {
    "research_papers": "replace_with_your_research_papers_webset_id",
    "surveys": "replace_with_your_surveys_webset_id",
    "statistica": "replace_with_your_statistica_webset_id"
}

def perform_audience_research(mode, user_query, num_results=5):
    """
    mode: one of 'research_papers', 'surveys', 'statistica'
    user_query: string, the user's research question
    num_results: int, number of search results to retrieve
    """
    if mode not in WEBSET_IDS:
        raise ValueError("Invalid research mode.")
    webset_id = WEBSET_IDS[mode]
    exa_client = ExaWebsetsClient()
    gemini = GeminiSummarizer()

    # 1. Search Exa Websets
    results = exa_client.search_websets(user_query, webset_id=webset_id, num_results=num_results)
    docs = [r.text for r in results.results]
    links = [r.url for r in results.results]

    # 2. Summarize with Gemini
    summary = gemini.summarize(docs)

    return summary, links
