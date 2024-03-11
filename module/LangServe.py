 
#!/usr/bin/env python
# from fastapi import FastAPI
# from langchain.prompts import ChatPromptTemplate
# from langchain.chat_models import ChatAnthropic, ChatOpenAI
# from langserve import add_routes
# import uvicorn

# import os
# os.environ["DASHSCOPE_API_KEY"] = "sk-5e56b4e6ddba4a6a8110e168d8dd8377"



import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY'] = 'ls__eaf357058c534c5da51bd8574575c046'

os.environ['LANGCHAIN_PROJECT'] = 'demo'

os.environ["DASHSCOPE_API_KEY"] = "sk-5e56b4e6ddba4a6a8110e168d8dd8377"



#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
# from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langserve import add_routes

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# add_routes(
#     app,
#     Tongyi(),
#     path="/openai",
# )

# add_routes(
#     app,
#     ChatAnthropic(),
#     path="/anthropic",
# )

from langchain_community.llms import Tongyi
model = Tongyi()
prompt = ChatPromptTemplate.from_template("请讲一个关于{topic}的笑话")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)