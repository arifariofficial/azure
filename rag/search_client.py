import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

load_dotenv()


# load environment variable
service_endpoint = os.getenv("AI_SEARCH_SERVICE_ENDPOINT")
index_name = os.getenv("AI_SEARCH_INDEX_NAME")
key = os.getenv("AZURE_SEARCH_API_KEY")

if service_endpoint is None or index_name is None or key is None:
    raise ValueError("Please setup environment key")

credential = AzureKeyCredential(key=key)

search_client = SearchClient(
    endpoint=service_endpoint, index_name=index_name, credential=credential
)

