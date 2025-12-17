import asyncio
import os
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


async def main():

    async with (
        AzureCliCredential() as credential,
        AzureAIClient(
            credential=credential,
            project_endpoint=project_endpoint,
            model_deployment_name=model_deployment,
            agent_name="simple-agent",
        ).create_agent(
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
