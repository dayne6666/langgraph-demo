from langchain_core.tools import tool


@tool('calculate', parse_docstring=True)
def calculate4(
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


print(calculate4.name)
print(calculate4.description)
print(calculate4.args)
print(calculate4.args_schema.model_json_schema())
print(calculate4.return_direct)
resp = calculate4.invoke({'a': 12, 'b': 23, 'operation': 'add'})
print(resp)
