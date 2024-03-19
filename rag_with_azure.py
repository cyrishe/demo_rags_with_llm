from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llm_engine.azure_openai import get_llm_model , get_emb_model
from task_analyzer.task_analyzer import task_analyzer , final_answer
import logging
import sys

logging.basicConfig(
            stream=sys.stdout, level=logging.INFO
            )  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import Settings

Settings.llm = get_llm_model()
Settings.embed_model = get_emb_model()

from llama_index.core import VectorStoreIndex, download_loader
from llama_index.readers.web import BeautifulSoupWebReader


def get_query_engine(file_dir):
    documents = SimpleDirectoryReader( input_dir=file_dir).load_data()

    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    return query_engine


if __name__ == '__main__':
    
    query_engine = get_query_engine("./offline_docs/tmp")
    question_list = []
    #question_list.append("根据文中的研究机构的结论，全球哪些国家的市场适合做医美业务？")
    #question_list.append("越南的医美市场有哪些优势？政策和风险呢？")
    question_list.append("印尼的医疗器械市场怎么样？是否适合进入？为什么？")
    for q in question_list:
        break_down_list = task_analyzer(q)
        action_list = break_down_list.split("*")[1:]
        context = ''
        for action in action_list:
            q = '请你检索出和"%s"相关的段落文字' % action 
            response = query_engine.query(q)
            context += str(response)+"\n\n"
        response = final_answer(context,q)        
        print(response)
