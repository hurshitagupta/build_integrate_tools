# Build And Integrate Tools

# Task 1 — Tool Registry

## Objective

The objective of this task is to implement a central tool registry that can store, discover, and invoke tools by name.

The implementation demonstrates both a successful tool invocation and a rejected invocation for an unknown tool.

## Implementation

The task contains two main components:

### Tool

The `Tool` class represents an individual capability.

Each tool contains:

* A unique tool name
* A callable function that performs the actual operation

For this task, the registered tool is:

```text
lookup_order
```

The tool accepts an order ID and returns the current status of the order.

Example:

```python
{"order_id": "A100"}
```


### ToolRegistry

The `ToolRegistry` acts as the central location for managing tools.

It supports:

* Registering a tool
* Discovering registered tools
* Retrieving a tool by name
* Invoking a registered tool
* Rejecting unknown tools
* Preventing duplicate tool registration

This creates a clear capability boundary because only tools registered in the registry can be invoked.

## Happy Path

The `lookup_order` tool is registered in the registry and invoked.

This proves that a registered tool can be discovered and executed successfully.

## Failure Path

The implementation also attempts to invoke: unknown_tool

Since this tool is not registered, the registry rejects the request and raises a `ValueError`.

This prevents arbitrary or unavailable tools from being executed.


## Run Command

Run the implementation from the project root:

```bash
python tool_registry.py
```

## Automated Tests

Run the automated tests using:

```bash
pytest tests/test_tool_registry.py -v
```

The tests cover:

1. Successful invocation of a registered tool.
2. Rejection of an unknown tool.

