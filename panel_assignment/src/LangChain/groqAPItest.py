import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env
api_key = os.getenv("GROQ_API_KEY")

# Your API Key
api_key = api_key

# List of publication titles (example)
titles = [
    "A Survey on Vehicle Platooning Concepts and Protocols",
    "Autonomous Navigation in Urban Environments",
    "Machine Learning for Smart Transportation",
    "A Review on VANET Communication Security",
    "Deep Learning Approaches for Self-Driving Cars"
]

# Build the prompt
prompt = "Based on the following publication titles, give the top 5 research interests or keywords:\n\n"
prompt += "\n".join(titles)

# API endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

# Payload
payload = {
    "model": "llama3-70b-8192",  # You can also use "llama3-70b-8192"
    "messages": [
        {"role": "system", "content": "You are an expert assistant that summarizes research interests."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3,
}

# Headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Send request
response = requests.post(url, json=payload, headers=headers)

# Parse and print result
if response.status_code == 200:
    result = response.json()
    reply = result['choices'][0]['message']['content']
    print("Top 5 Research Interests:")
    print(reply)
else:
    print("Error:", response.status_code, response.text)
