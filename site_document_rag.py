from llama_index.core import VectorStoreIndex, download_loader

from llama_index.readers.web import WholeSiteReader

# Initialize the scraper with a prefix URL and maximum depth
scraper = WholeSiteReader(
            prefix="https://docs.llamaindex.ai/en/stable/",  # Example prefix
                max_depth=10,
                )

# Start scraping from a base URL
documents = scraper.load_data(
            base_url="https://docs.llamaindex.ai/en/stable/"
            )  # Example base URL
index = VectorStoreIndex.from_documents(documents)
index.query("What language is on this website?")
