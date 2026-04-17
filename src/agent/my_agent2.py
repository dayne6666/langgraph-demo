import os
from urllib.parse import urlparse, unquote
import pymysql
from dotenv import load_dotenv
from langgraph.checkpoint.mysql.pymysql import PyMySQLSaver
from langgraph.store.mysql.pymysql import PyMySQLStore
from langgraph.prebuilt import create_react_agent

from agent.my_agent import search_tool
from agent.my_llm import llm, mysql_url

load_dotenv()
# 强制读系统环境变量绕过 .env 展开问题
mysql_url = os.getenv("MYSQL_CONNECTION")

# 手动解析并解码URL，解决特殊字符密码问题
parsed = urlparse(mysql_url)
params = {
    "host": parsed.hostname,
    "user": parsed.username,
    "password": unquote(parsed.password) if parsed.password is not None else "",
    "database": "langgraph_db",
    "port": parsed.port or 3306,
    "charset": "utf8mb4",
}

# 手动创建连接，确保密码正确解码
with (
    pymysql.connect(**params, autocommit=True) as conn_store,
    pymysql.connect(**params, autocommit=True) as conn_ckpt,
):
    store = PyMySQLStore(conn_store)
    checkpointer = PyMySQLSaver(conn_ckpt)
    # 需要初始化表结构（第一次运行需要）
    checkpointer.setup()
    store.setup()
    agent = create_react_agent(
        llm,
        tools=[search_tool],
        prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
        checkpointer=checkpointer,
        store=store,
    )

    config = {
        "configurable": {
            "thread_id": "2"
        }
    }

    # 从短期存储中返回当前会话的上下文
    rest = list(agent.get_state(config))
    # 从长期存储中返回当前会话的上下文
    rest2 = list(agent.get_state_history(config))
    print(rest)
    print(rest2)

    resp1 = agent.invoke(
        {"messages": [{"role": "user", "content": "今天北京的天气怎么样？"}]},
        config,
    )
    print(resp1['messages'][-1].content)

    resp2 = agent.invoke(
        {"messages": [{"role": "user", "content": "那长沙呢"}]},
        config,
    )

    print(resp2['messages'][-1].content)
