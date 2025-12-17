import asyncio
import os
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

from dotenv import load_dotenv

load_dotenv()

project_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
if project_endpoint is None and model_deployment is None:
    raise ValueError("Please set env")

credential = AzureCliCredential()

agent = AzureOpenAIChatClient(
    credential=credential,
    deployment_name=model_deployment,
    endpoint=project_endpoint,
).create_agent(instructions="You are a helpful assistant", name="helpful-assistant")


async def main():
    async for update in agent.run_stream(
        "Write me a essay for 200 words about Finland.",
    ):
        if update.text:
            print(update.text, end="", flush=True)
    print()


asyncio.run(main())
