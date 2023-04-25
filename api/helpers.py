from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
import os
import openai
from dotenv import load_dotenv

from llama_index import GPTSimpleVectorIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory



load_dotenv()
openai.key = os.getenv("OPENAI_API_KEY")
apify_key = os.getenv("APIFY_API_TOKEN")

apify = ApifyWrapper()

# def lang_init(url_link=''):
#     loader = apify.call_actor(
#         actor_id="apify/website-content-crawler",
#         run_input={"startUrls": [{"url": "https://python.langchain.com/en/latest/"}]},
#         dataset_mapping_function=lambda item: Document(
#             page_content=item["text"] or "", metadata={"source": item["url"]}
#         ),
#     )
#     index = VectorstoreIndexCreator().from_loaders([loader])

#     query = "What is LangChain?"
#     result = index.query_with_sources(query)

#     print(result["answer"])
#     print(result["sources"])

#     return result["answer"]

def lang_init():
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")

    loader = BeautifulSoupWebReader()
    documents = loader.load_data(urls=['https://nike.com'])
    index = GPTSimpleVectorIndex(documents)

    tools = [
        Tool(
            name="Website Index",
            func=lambda q: index.query(q),
            description=f"Useful when you want answer questions about the text on websites.",
        ),
    ]
    llm = OpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(
        tools, llm, agent="zero-shot-react-description", memory=memory
    )

    output = agent_chain.run(input="What is Nike about?")
    return output
