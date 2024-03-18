
import os

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY'] = 'ls__6bbb945fcce94b8ca12aa31e88442720' # ls__e16292c2e52b46b681fb59714f330bde
os.environ['LANGCHAIN_PROJECT'] = 'demo'


os.environ["DASHSCOPE_API_KEY"] = "sk-9f955baffcc14f098f5df1baec4cf67c"



#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
from langchain_community.llms import Tongyi
app = FastAPI(
    title="langchain",
    version="1.0",
    description="该工程用于演示langchain功能。",
)

model = Tongyi()

add_routes(
    app,
    model,
    path="/chat",
)


prompt = ChatPromptTemplate.from_template("请讲一个关于{topic}的笑话")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8888)