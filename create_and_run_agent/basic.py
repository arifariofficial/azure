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
).create_agent(instructions="You are good at telling jokes.", name="Joken")


async def main():
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)


asyncio.run(main())
