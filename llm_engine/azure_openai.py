from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import logging
import sys

logging.basicConfig(
            stream=sys.stdout, level=logging.INFO
            )  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

api_key = "1b5676c691ba453bb13cc9c9f6987a3c"
azure_endpoint = "https://openai-univista.openai.azure.com/"
api_version = "2023-07-01-preview"

llm_g4 = AzureOpenAI(
            #model="gpt-35-turbo-16k",
            model="gpt-4-32k",
            deployment_name="gpt4-32K",
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            )

llm_g35 = AzureOpenAI(
            model="gpt-35-turbo-16k",
            #model="gpt-4",
            deployment_name="G35",
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            )

llm=llm_g35
# You need to deploy your own embedding model as well as your own chat completion model
embed_model = AzureOpenAIEmbedding(
            model="text-embedding-ada-002",
            deployment_name="embedding",
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            )


def get_llm_model():
    return llm

def get_emb_model():
    
    return embed_model
