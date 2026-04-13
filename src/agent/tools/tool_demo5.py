from cryptography.x509 import name
from langchain_core.tools import tool, StructuredTool


def calculate5(
        a: float,
        b: float,
        operation: str) -> float:
    """工具函数：计算两个数字的运算结果

    Args:
        a: 第一个需要输入的数字
        b: 第二个需要输入的数字
        operation: 运算类型，只能是add、subtract、multiply、divide中的任意一个

    Returns:
        返回两个输入数字的运算结果。

    """
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

async def calculate6(
        a: float,
        b: float,
        operation: str) -> float:
    """工具函数：计算两个数字的运算结果

    Args:
        a: 第一个需要输入的数字
        b: 第二个需要输入的数字
        operation: 运算类型，只能是add、subtract、multiply、divide中的任意一个

    Returns:
        返回两个输入数字的运算结果。

    """
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

calculater = StructuredTool.from_function(func=calculate5,
                                          name = "calculater",
                                          description='工具函数：计算两个数字的运算结果',
                                          coroutine=calculate6
                                        )

print(calculater.description)