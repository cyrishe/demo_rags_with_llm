from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llm_engine.azure_openai import get_llm_model , get_emb_model

from llama_index.readers.file import CSVReader, DocxReader, PptxReader, FlatReader,PyMuPDFReader

import logging
import sys,os

logging.basicConfig(
            stream=sys.stdout, level=logging.INFO
            )  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, download_loader,load_index_from_storage,StorageContext ,Settings , node_parser

Settings.llm = get_llm_model()
Settings.embed_model = get_emb_model()

from llama_index.readers.web import BeautifulSoupWebReader


def get_document(path,suffix):
    document = None
    print("processing ", path)
    if suffix in ['doc','docx']:
        document = DocxReader().load_data(path)
    elif suffix in ['ppt','pptx']:
        document = PptxReader().load_data(path)
    elif suffix in ['csv']:
        document = CSVReader().load_data(path)
    elif suffix in ['txt']:
        document = SimpleDirectoryReader(input_files=[path]).load_data()
    elif suffix in ['pdf']:
        document = PyMuPDFReader().load_data(path)
    else:
        print("unsupported file format" , suffix)
    if document:
        for d in document:
            print(d)
    return document


def load_offline_documents(doc_path):
    documents = []
    for root,d,f in os.walk(doc_path):
        for name in f:
            suffix = name.split('.')[-1]
            suffix = suffix.lower()
            path = os.path.join(root,name)
            document = get_document(path,suffix)
            if document:
                documents.extend(document)
    parser = node_parser.SentenceSplitter()
    nodes = parser.get_nodes_from_documents(documents)
    for n in nodes:
        print("***")
        print(n)
    index = VectorStoreIndex(nodes)
    print("keep index persist...")
    index.storage_context.persist(persist_dir='./persist_index/')
    print("index persist done!")
    return index




def index_init():
    print("try loading from persist indexed files...")
    try:
        storage_context = StorageContext.from_defaults(persist_dir="./persist_index/")
        index = load_index_from_storage(storage_context)
        print("loading from persist_index done!")

    except:
        print("no persist index file, building from offline docs ")
        index = load_offline_documents("./offline_docs")
        print("loading index from documents done!")
    return index    




if __name__ == '__main__':
    index = index_init()
    engine = index.as_query_engine(response_mode="tree_summarize",similarity_top_k=5)
    r = engine.query('请介绍一下External Fixation的历史和发展历程？')
    #r = engine.query('Please introduce the Development History and Key Milestone of External Fixation')
    print(r)
