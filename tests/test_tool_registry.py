import pytest

from tool_registry.tool_registry import Tool, ToolRegistry, lookup_order


def create_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        Tool( name="lookup_order", run=lookup_order)
    )

    return registry


def test_registered_tool_invocation_success():
    registry = create_registry()

    result = registry.invoke("lookup_order",{"order_id": "A100"})

    assert result == "packed"


def test_unknown_tool_is_rejected():
    registry = create_registry()

    with pytest.raises(ValueError,match="Tool 'unknown_tool' is not registered"):
        registry.invoke("unknown_tool",{"order_id": "A100"})