from app.providers.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            import importlib

            genai = importlib.import_module("google.generativeai")

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                model_name="gemini-3.8-flash",
                system_instruction=system_prompt,
            )
            response = model.generate_content(user_prompt)
            return response.text
        except ImportError:
            raise RuntimeError("google-generativeai package not installed")
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
