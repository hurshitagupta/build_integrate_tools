from tool_registry.tool_registry import Tool, ToolRegistry


def validate_order_args(args: dict) -> None:
    if "order_id" not in args:
        raise ValueError("Missing required argument: order_id")

    if not isinstance(args["order_id"], str):
        raise TypeError("order_id must be a string")

    if not args["order_id"].strip():
        raise ValueError("order_id cannot be empty")


def lookup_order(args: dict) -> str:
    validate_order_args(args)

    orders = {
        "A100": "packed",
        "A101": "shipped",
    }

    return orders.get(args["order_id"], "not found")


def main():
    registry = ToolRegistry()

    registry.register(Tool(name="lookup_order",run=lookup_order))

    print("=== ARGUMENT VALIDATION DEMO ===")

    print("\nHappy path:")

    valid_args = {"order_id": "A100"}

    result = registry.invoke("lookup_order",valid_args)

    print(f"Arguments: {valid_args}")
    print(f"Result: {result}")

    print("\nFailure path - missing argument:")

    try:
        registry.invoke("lookup_order",{})
    except (ValueError, TypeError) as error:
        print(f"Rejected: {error}")

    print("\nFailure path - wrong type:")

    try:
        registry.invoke("lookup_order",{"order_id": 100},)
    except (ValueError, TypeError) as error:
        print(f"Rejected: {error}")

    print("\nFailure path - empty value:")

    try:
        registry.invoke("lookup_order",{"order_id": ""})
    except (ValueError, TypeError) as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    main()