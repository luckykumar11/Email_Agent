from app.providers.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        return (
            "Subject: Introduction from Your Company\n\n"
            "Dear Valued Contact,\n\n"
            "I hope this email finds you well. I am writing to introduce our company "
            "and the services we offer that may be of interest to you.\n\n"
            "Based on our company profile, we specialize in providing innovative solutions "
            "tailored to meet your specific needs. Our team is dedicated to delivering "
            "high-quality results and exceptional customer service.\n\n"
            "We would love the opportunity to discuss how we can help your business. "
            "Please feel free to reach out at your convenience.\n\n"
            "Best regards,\n"
            "[Company Representative]"
        )
