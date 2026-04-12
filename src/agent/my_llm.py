import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(override=True)
deepseek = os.getenv("DEEPSEEK_API_KEY")
deepseekBaseUrl = os.getenv("DEEPSEEK_BASE_URL")
ark_api_key = os.getenv("ARK_API_KEY")
ark_base_url = os.getenv("ARK_BASE_URL")
mysql_url = os.getenv("MYSQL_CONNECTION")


deepseek_llm = init_chat_model(
    model= "deepseek-chat",
    model_provider= "deepseek",
    base_url=deepseekBaseUrl,
    api_key=deepseek
)

#多模态的大模型，后面替换
llm  = init_chat_model(
    model= "ark-code-latest",
    model_provider= "openai",
    base_url=ark_base_url,
    api_key=ark_api_key

)


