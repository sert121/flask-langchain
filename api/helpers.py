from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
import os
import openai
from dotenv import load_dotenv


load_dotenv()
openai.key = os.getenv("OPENAI_API_KEY")
apify_key = os.getenv("APIFY_API_TOKEN")

apify = ApifyWrapper()

def lang_init(url_link=''):
    
    loader = apify.call_actor(
        actor_id="apify/website-content-crawler",
        run_input={"startUrls": [{"url": "https://python.langchain.com/en/latest/"}]},
        dataset_mapping_function=lambda item: Document(
            page_content=item["text"] or "", metadata={"source": item["url"]}
        ),
    )
    index = VectorstoreIndexCreator().from_loaders([loader])

    query = "What is LangChain?"
    result = index.query_with_sources(query)

    print(result["answer"])
    print(result["sources"])

    return result["answer"]