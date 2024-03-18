!pip install langchain docarray tiktoken  -i https://pypi.tuna.tsinghua.edu.cn/simple




正常新生儿和婴儿的基本护理



# 准备工作

```
apt update
git lfs install
cd root_dir
mkdir root_dir/models
cd root_dir/models

git clone https://huggingface.co/moka-ai/m3e-base
git clone https://huggingface.co/THUDM/chatglm3-6b
```

# 运行ChatGLM3工程的ChatGLM3/basic_demo/web_demo_streamlit.py的demo
```
cd root_dir
mkdir webcodes
cd root_dir/webcodes
git clone https://github.com/THUDM/ChatGLM3.git
cd root_dir/webcodes/ChatGLM3
pip install -r requirements.txt
cd root_dir/webcodes/ChatGLM3/basic_demo
修改为离线大模型：修改root_dir/webcodes/ChatGLM3/basic_demo/web_demo_streamlit.py中的18行的MODEL_PATH变量为chatglm3-6b的path
streamlit run root_dir/webcodes/ChatGLM3/basic_demo/web_demo_streamlit.py
```

# 安装 Docker 和 docker-compose
```
# 安装 Docker(参考 https://doc.fastai.site/docs/development/docker/)
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
systemctl enable --now docker
# 安装 docker-compose
curl -L https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
# 验证安装
docker -v
docker-compose -v
# 如失效，自行百度~
```

# 使用docker部署one-api项目（大模型服务-->one-api封装大模型服务）
```
# 1.运行大模型
cd root_dir/webcodes/ChatGLM3/openai_api_demo
修改为离线大模型：修改root_dir/webcodes/ChatGLM3/openai_api_demo/api_server.py中的50-55行的MODEL_PATH变量为chatglm3-6b的path,EMBEDDING_PATH变量为m3e-base的path
python api_server.py

# 2.部署one-api项目
cd root_dir
mkdir oneApi
cd root_dir/oneApi
# 使用 SQLite 的部署命令：
docker run --name one-api -d --restart always -p 3080:3000 -e TZ=Asia/Shanghai -v /home/ubuntu/data/one-api:/data justsong/one-api
docker ps
初始账号用户名为 root，密码为 123456，测试正常使用

# 3.在one-api项目中配置大模型通道
在one-api的web页面中添加新的自定义渠道：mse-base和chatglm3
分别测试通道

# 4.配置令牌
配置令牌，为部署fastgpt做准备
```

# 使用docker部署fastgpt项目（使用one-api封装大模型服务，构建应用）
```
cd root_dir

# 1.创建目录并下载 docker-compose.yml
mkdir fastgpt
cd root_dir/fastgpt
curl -O https://raw.githubusercontent.com/labring/FastGPT/main/files/deploy/fastgpt/docker-compose.yml
curl -O https://raw.githubusercontent.com/labring/FastGPT/main/projects/app/data/config.json

# 2.修改 docker-compose.yml 的环境变量
OPENAI_BASE_URL=OneAPI访问地址/v1
CHAT_API_KEY=令牌

# 3.修改 config.json 的配置
llmModels和vectorModels为chatglm3和mse-base
llmModels中datasetProcess=true


# 4.启动容器
docker-compose pull
docker-compose up -d

# 5.初始化 Mongo 副本集(4.6.8以前可忽略)
# 查看 mongo 容器是否正常运行
docker ps
# 进入容器
docker exec -it mongo bash

# 连接数据库（这里要填Mongo的用户名和密码）
mongo -u myusername -p mypassword --authenticationDatabase admin

# 初始化副本集。如果需要外网访问，mongo:27017 可以改成 ip:27017。但是需要同时修改 FastGPT 连接的参数（MONGODB_URI=mongodb://myname:mypassword@mongo:27017/fastgpt?authSource=admin => MONGODB_URI=mongodb://myname:mypassword@ip:27017/fastgpt?authSource=admin）
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo:27017" }
  ]
})
# 检查状态。如果提示 rs0 状态，则代表运行成功
rs.status()

# 6.访问 FastGPT link
目前可以通过 ip:3000 直接访问(注意防火墙)。登录用户名为 root，密码为docker-compose.yml环境变量里设置的 DEFAULT_ROOT_PSW。

如果需要域名访问，请自行安装并配置 Nginx。

# 7.试用
```


# LLaMA-Factory微调大模型
```
cd root_dir
git clone https://github.com/hiyouga/LLaMA-Factory.git
conda create -n llama_factory python=3.10
conda activate llama_factory
cd LLaMA-Factory
pip install -r requirements.txt

1.将微调数据放在 root_dir/LLaMA-Factory/data/中
2.在root_dir/LLaMA-Factory/data/dataset_info.json最后一行，添加本地微调数据的配置
3.python src/web_demo.py
4.打开web页面
5.依次填写：语言、模型名称、模型路径、数据集
6.开始训练
7.训练结束，测试模型
8.导出模型，供其他应用使用
```