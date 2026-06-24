import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(
    api_key=os.environ["CUSTOM_OPENAI_API_KEY"],
    base_url=os.environ["CUSTOM_OPENAI_ENDPOINT"],
)

models = client.models.list()
for m in sorted(models.data, key=lambda x: x.id):
    print(m.id)
