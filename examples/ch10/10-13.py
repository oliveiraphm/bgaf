import datetime 

import google.generativeai as genai
from google.generativeai import caching

import os
from dotenv import load_dotenv 

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

corpus = genai.upload_file(path="corpus.txt")
cache = caching.CachedContent.create(
    model = "models/gemini-1.5-flash-001",
    display_name = "fastapi",
    system_instruction=(
        "You are an expert AI engineer, and your job is to answer "
        "the user's query based on the files you have access to."
    ),
    contents = [corpus],
    ttl = datetime.timedelta(minutes=5),
)

model = genai.GenerativeModel.from_cached_content(cached_content=cache)
response = model.generate_content(
    [
        (
            "Introduce different characters in the movie by describing "
            "their personality, looks, and names. Also list the timestamps "
            "they were introduced for the first time."
        )       
    ]
)