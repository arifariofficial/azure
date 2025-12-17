import os
from dotenv import load_dotenv
import asyncio

from agent_framework_azure_ai import AzureAIClient
from azure.identity.aio import AzureCliCredential

load_dotenv()


class BasicAgentClient:
    def __init__(self, instructions: str):
        self.instructions = instructions
        self.project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self.model_deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")

        if not self.project_endpoint or not self.model_deployment:
            raise ValueError(
                "Environment variables AZURE_AI_PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME must be set."
            )

        self._credential = None
        self._agent_ctx = None
        self.agent = None

    async def __aenter__(self):
        self._credential = AzureCliCredential()
        self._agent_ctx = AzureAIClient(
            credential=self._credential,
            project_endpoint=self.project_endpoint,
            agent_name="simple-agent",
            model_deployment_name=self.model_deployment,
        ).create_agent(instructions=self.instructions)

        self.agent = await self._agent_ctx.__aenter__()
        return self.agent

    async def __aexit__(self, exc_type, exc, tb):
        if self._agent_ctx is not None:
            await self._agent_ctx.__aexit__(exc_type, exc, tb)
        if self._credential is not None:
            await self._credential.close()

    async def run(self, prompt: str):
        if self.agent is None:
            raise RuntimeError(
                "Agent has not been initialized. Use 'async with' to create the agent."
            )
        return await self.agent.run(prompt)


async def main():
    async with BasicAgentClient(
        instructions="You are good at telling jokes.",
    ) as agent:
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
