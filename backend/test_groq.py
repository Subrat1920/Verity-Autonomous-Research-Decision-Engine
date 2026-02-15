import httpx, os, json
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
key = os.environ.get("GROQ_API_KEY")
resp = httpx.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {key}"},
    timeout=30.0
)
data = resp.json()
for m in data.get("data", []):
    print(f"{m['id']:45s}  owned_by={m.get('owned_by','')}")
