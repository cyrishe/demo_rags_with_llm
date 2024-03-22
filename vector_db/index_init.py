from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llm_engine.azure_openai import get_llm_model , get_emb_model

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline, IngestionCache

from llama_index.core import VectorStoreIndex, download_loader,load_index_from_storage,StorageContext ,Settings , node_parser ,Document ,ServiceContext
from llama_index.readers.file import CSVReader, DocxReader, PptxReader, FlatReader,PyMuPDFReader
from llama_index.core.node_parser import get_leaf_nodes ,HierarchicalNodeParser
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


import logging
import sys,os
#from llama_index.core import set_global_handler

#set_global_handler("langfuse")

Settings.llm = get_llm_model()
Settings.embed_model = get_emb_model()

logging.basicConfig(
            stream=sys.stdout, level=logging.INFO
            )  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

OFFLINE_HIERICHY_INDEX_FLODER='./offline_index/hierichy_index'
OFFLINE_HIERICHY_INDEX_FLODER_3_level='./offline_index/hierichy_index_2048_512_128'
OFFLINE_CHUNKED_INDEX_FLODER='./offline_index/chunked_index'

OFFLINE_INDEX = OFFLINE_HIERICHY_INDEX_FLODER_3_level

def build_chunked_index(docs , chunk_size=512,chunk_overlap=64):

    pipeline = IngestionPipeline(
        transformations=[
        SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap),
        TitleExtractor(),
        ]
     )
    nodes = pipeline.run(documents=docs)


    index = VectorStoreIndex(nodes)
    return index



def build_hierichy_index(docs,chunk_size_list = [1024,256]):
 
    node_parser = HierarchicalNodeParser.from_defaults(
             chunk_sizes=chunk_size_list
             )
    nodes = node_parser.get_nodes_from_documents(docs)
    leaf_nodes = get_leaf_nodes(nodes)
    auto_merging_context = ServiceContext.from_defaults(
        llm=Settings.llm,
        embed_model=Settings.embed_model,
        node_parser=node_parser,
        )
     
    #创建向量库索引
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)
    automerging_index = VectorStoreIndex(
        leaf_nodes, 
        storage_context=storage_context, 
        service_context=auto_merging_context
        )
    return automerging_index


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
    return document

def rebuild_document(document,file_name,suffix):
    t = ''
    for d in document:
        t = t+d.text
    metadata={"filename": file_name, "file_type": suffix , "length":len(t) , "pages": len(document)}
    new_docs = [Document(text=t,metadata=metadata)]
    return new_docs



def load_offline_documents(doc_path):
    documents = []
    for root,d,f in os.walk(doc_path):
        for name in f:
            suffix = name.split('.')[-1]
            suffix = suffix.lower()
            path = os.path.join(root,name)
            document = get_document(path,suffix)
            if document:
                document = rebuild_document(document,name,suffix)
                documents.extend(document)

    #build nodes with pipeline with custom chunk size and overlap            
    #nodes = pipeline.run(documents=documents)
    #index = build_chunked_index(documents)

    index = build_hierichy_index(documents)


    #nodes = parser.get_nodes_from_documents(documents)
    #for n in nodes:
    #    print("***")
    #    print(n)
    print("keep index persist...")
    index.storage_context.persist(persist_dir=OFFLINE_INDEX)
    print("index persist done!")
    return index




def index_init():
    print("try loading from persist indexed files...")
    try:
        storage_context = StorageContext.from_defaults(persist_dir=OFFLINE_INDEX)
        index = load_index_from_storage(storage_context)
        print("loading from persist_index done!")


    except:
        print("no persist index file, building from offline docs ")
        index = load_offline_documents("./offline_docs")
        print("loading index from documents done!")
    return index    




if __name__ == '__main__':
    index = index_init()
    q_list = []
    q_list.append('请介绍一下外固定支架的历史和发展历程？')
    q_list.append('对比一下各个国家的骨科医生的现状。')
    q_list.append('请问内固定板都有哪些国内供应商？哪些国外供应商？他们是哪个国家的？主要产品是什么？')
    q_list.append('请问外固定系统都有哪些国内供应商？哪些国外供应商？他们是哪个国家的？主要产品是什么？')
    q_list.append('请问AKED公司是那个国家的公司？主营产品有哪些？')
    for q in q_list:
        print("******",q,"******")
        #engine = index.as_query_engine(response_mode="tree_summarize",similarity_top_k=5)
        base_retriever = index.as_retriever(
            similarity_top_k=16
        )
 
        retriever = AutoMergingRetriever(
            base_retriever, 
            index.storage_context, 
            verbose=True
        )
 
        rerank = SentenceTransformerRerank(top_n=3, model="BAAI/bge-reranker-base")
 
        engine = RetrieverQueryEngine.from_args(
            retriever, node_postprocessors=[rerank]
        )


        #retrieve = index.as_retriever(similarity_top_k=5)
        ret_docs = retriever.retrieve(q)
        print("relevence docs:")
        for n in ret_docs:
            print(n.text)
            print("\n\n\n")
        r = engine.query(q)
        print("final answer:")
        print("resopnse:")
        print(r)
