
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable

# openai = RemoteRunnable("http://localhost:8000/openai/")
# anthropic = RemoteRunnable("http://localhost:8000/anthropic/")
joke = RemoteRunnable("http://localhost:8000/joke/")

joke.invoke({"topic": "猫咪"})

# or async
# await joke_chain.ainvoke({"topic": "冰淇淋"})

prompt = [
    SystemMessage(content='表现得像猫或鹦鹉'),
    HumanMessage(content='你好!')
]

# Supports astream
# async for msg in anthropic.astream(prompt):
#     print(msg, end="", flush=True)

# prompt = ChatPromptTemplate.from_messages(
#     [("system", "Tell me a long story about {topic}")]
# )

# Can define custom chains
chain = prompt | RunnableMap({
    "joke": joke,
    # "anthropic": anthropic,
})

chain.batch([{"topic": "鹦鹉"}, {"topic": "猫咪"}])