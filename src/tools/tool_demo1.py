from langchain_core.tools import tool


@tool
def calculate1(a: float, b: float, operation: str) -> float:
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

print(calculate1.name)
print(calculate1.description)
print(calculate1.args)
print(calculate1.args_schema.model_json_schema())
print(calculate1.return_direct)