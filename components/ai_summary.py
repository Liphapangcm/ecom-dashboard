import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_weekly_summary(weekly_df):
    """Takes the last 8 weeks of stats and returns an AI-written summary"""

    # Format the data into a readable string for the prompt
    data_str = weekly_df.to_string(index=False)

    prompt = f"""
You are a data analyst writing a weekly performance summary for a small e-commerce business owner.
They are not technical — write in plain, friendly English with no jargon.

Here is the last 8 weeks of sales data:

{data_str}

Write a summary with exactly 3 short paragraphs:
1. Overall performance — how has revenue trended? Is it growing, flat, or declining?
2. Best and worst week — call out the standout weeks and give a possible reason why
3. One clear recommendation — what should the business owner focus on or watch next week?

Keep it under 150 words total. Be direct and specific with the numbers.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content