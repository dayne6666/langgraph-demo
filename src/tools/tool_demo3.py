from typing import Annotated

from langchain_core.tools import tool


@tool('calculate')
def calculate3(
        a: Annotated[float, '第一个需要输入的数字'],
        b: Annotated[float, '第二个需要输入的数字'],
        operation: Annotated[str, '运算类型，只能是add、subtract、multiply、divide中的任意一个']) -> float:
    """工具函数：计算两个数字的运算结果"""
    print(f"调用calculate 第一个数字是{a},第二个数字是{b},运算符是{operation}")
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        raise ValueError("操作符号错误")


print(calculate3.name)
print(calculate3.description)
print(calculate3.args)
print(calculate3.args_schema.model_json_schema())
print(calculate3.return_direct)


resp = calculate3.invoke({'a': 12, 'b': 23, 'operation': 'add'})
print(resp)
