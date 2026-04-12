from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CalculateArgs(BaseModel):
    a: float = Field(description="第一个需要输入的数字")
    b: float = Field(description="第一个需要输入的数字")
    operation: str = Field(description="运算类型，只能是add、subtract、multiply、divide中的任意一个")


@tool('calculate', args_schema=CalculateArgs)
def calculate2(a: float, b: float, operation: str) -> float:
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


print(calculate2.name)
print(calculate2.description)
print(calculate2.args)
print(calculate2.args_schema.model_json_schema())
print(calculate2.return_direct)
