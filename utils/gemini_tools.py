import os

from google import genai
from google.genai import types


def generate_ai_description(brand, model, version, year):
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    prompt = f'Faça uma descrição de venda para o carro {brand} {model} {version} {year} em apenas 512 caracteres. Fale coisas específicas desse modelo de carro sem mencionar a lista de equipamentos. Não coloque caracteres especiais que não sejam acentuação.'
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0)),
    )
    return response.text
