from dataclasses import dataclass
from time import perf_counter
from typing import Callable


@dataclass
class Tool:
    name: str
    run: Callable[[dict], str]

    def invoke(self, args: dict) -> str:
        return self.run(args)


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered")

        return self._tools[name]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def invoke(self, name: str, args: dict) -> str:
        tool = self.get(name)
        return tool.invoke(args)


def lookup_order(args: dict) -> str:
    orders = {
        "A100": "packed",
        "A101": "shipped",
    }

    return orders.get(args.get("order_id"), "not found")


def main():
    registry = ToolRegistry()

    registry.register(
        Tool(name="lookup_order",run=lookup_order,)
    )

    print("=== TOOL REGISTRY DEMO ===")

    print(f"Registered tools: {registry.list_tools()}")
    print(f"Tool count: {len(registry.list_tools())}")

    start = perf_counter()

    result = registry.invoke("lookup_order",{"order_id": "A100"})

    time_used = (perf_counter() - start) * 1000

    print("\nHappy path:")
    print(f"Result: {result}")
    print(f"Execution time: {time_used:.3f} ms")

    print("\nFailure path:")

    try:
        registry.invoke("unknown_tool",{"order_id": "A100"})
    except ValueError as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    main()