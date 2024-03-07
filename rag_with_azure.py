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

llm = AzureOpenAI(
    model="gpt-35-turbo-16k",
    deployment_name="G35",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    )

# You need to deploy your own embedding model as well as your own chat completion model
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="embedding",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    )


from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model

from llama_index.core import VectorStoreIndex, download_loader
from llama_index.readers.web import BeautifulSoupWebReader

#loader = BeautifulSoupWebReader()
#documents = loader.load_data(urls=["https://baijiahao.baidu.com/s?id=1792370154358417817&wfr=spider&for=pc",'http://auto.jrj.com.cn/2024/03/04123239718128.shtml','http://ru.mofcom.gov.cn/article/jmxw/202402/20240203475058.shtml'])


def get_query_engine(doc_file_list):
    documents = SimpleDirectoryReader( input_files=doc_file_list).load_data()

    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    return query_engine


if __name__ == '__main__':
    query_engine = get_query_engine(["./docs/1.txt"])
    question_list = []
    question_list.append("根据文中的研究机构的结论，全球哪些国家的市场适合做医美业务？")
    question_list.append("越南的医美市场有哪些优势？政策和风险呢？")
    for q in question_list:

        response = query_engine.query(q)
        print("******")
        print(q)
        print(response)
