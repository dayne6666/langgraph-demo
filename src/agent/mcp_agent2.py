import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from agent.my_llm import llm


test_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXZfdXNlciIsImlzcyI6Imh0dHBzOi8vd3d3Lmxhb3hpYW8uY29tIiwiaWF0IjoxNzc2NDgwNzAyLCJleHAiOjE3NzY0ODQzMDIsImF1ZCI6Im15LWRldi1zZXJ2ZXIiLCJzY29wZSI6Imxhb3hpYW8gaW52b2tlX3Rvb2xzIn0.HYtudeu75xlpzWtPuovAz1vc-16D51Nwaez0KEYkDNOxOaATCVXaEaJfLjnTo8Pw70H2FEkbY4VGWbb9ez2giwynybsXtMNgaMdFRGSmfKvbH5dy93YVXddSbWg9Ft0i1yHmwdq4NsUOKTe3kHoNoiBlOVTsgfrauqEURDzUGEDmuh7jTjX3WgwjAXUzYdagrTNPK-UwzeQgAV1uwa7qp2lxWpRp3Aes-pG_b5vIqRcN3YqOOEFDpflL0Mjs4ca8HdzKcxcr52dxqJb53Xa-k24R-kcZkwe6Qe5mD2rYFY9DDp7wIINHF_nGcfzjTS9oDfoc8rNv4RclvX4pZ4bqOQ"

# Python MCP 服务端的连接配置
python_mcp_server_config = {
    'url': 'http://127.0.0.1:8080/streamable',
    'transport': 'streamable_http',
    'headers': {
        'Authorization': f'Bearer {test_token}',
    }
    # 'url': 'http://127.0.0.1:8080/sse',
    # 'transport': 'sse',
}



# MCP的客户端
mcp_client = MultiServerMCPClient(
    {
        'python_mcp': python_mcp_server_config,
    }
)


async def create_agent():
    """必须是异步函数中"""
    mcp_tools = await mcp_client.get_tools()
    print(mcp_tools)
    # p = await mcp_client.get_prompt(server_name='python_mcp', prompt_name='ask_about_topic', arguments={'topic': '深度学习'})
    # print(p)
    # data = await mcp_client.get_resources(server_name='python_mcp', uris='resource://config')
    # print(data[0])
    # print(data[0].data)  # json数据


    # return create_react_agent(
    #     llm,
    #     tools=mcp_tools,
    #     prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
    # )

    agent = create_react_agent(
        llm,
        tools=mcp_tools,
        prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
    )


    rest = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "今天，北京的天气怎么样？"}]}
    )
    print(rest['messages'])
    print(rest['messages'][-1].content)


#
# agent = asyncio.run(create_agent())


if __name__ == '__main__':
    asyncio.run(create_agent())



