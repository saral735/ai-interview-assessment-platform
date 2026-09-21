from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.groq_api_key
)


def generate_text(
    prompt: str,
    system_prompt: str = "You are a helpful AI assistant."
) -> str:
    """
    Generate text using Groq LLM.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content