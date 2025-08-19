import os
import exa
import google.generativeai as genai

class ExaWebsetsClient:
    def __init__(self):
        self.api_key = os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise RuntimeError("EXA_API_KEY environment variable is not set.")
        self.client = exa.Exa(api_key=self.api_key)

    def search_websets(self, query, webset_id, num_results=5):
        results = self.client.webset_search(
            webset_id=webset_id,
            query=query,
            num_results=num_results
        )
        return results

class GeminiSummarizer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def summarize(self, documents):
        content = "\n\n".join(documents)
        prompt = (
            "Summarize the following content into a concise report of actionable insights for audience research. "
            "List the most important findings and key points.\n\n"
            f"{content}"
        )
        response = self.model.generate_content(prompt)
        return response.text
