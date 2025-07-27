import openai
import streamlit as st

def generate_technical_tasks(use_case, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Data & AI consultant. Break down the given business use case into clear, "
                        "step-by-step technical tasks that a data or AI intern would perform to build a solution."
                    )
                },
                {"role": "user", "content": use_case}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error:\n\n{str(e)}"