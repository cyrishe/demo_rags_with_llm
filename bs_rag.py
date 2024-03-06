from llama_index.core import VectorStoreIndex, download_loader
from llama_index.readers.web import BeautifulSoupWebReader

loader = BeautifulSoupWebReader()
documents = loader.load_data(urls=["https://docs.llamaindex.ai/en/stable/"])
index = VectorStoreIndex.from_documents(documents)
index.query("What language is on this website?")
