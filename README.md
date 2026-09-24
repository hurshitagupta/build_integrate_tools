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

---

## Task 2 — Argument Validation

### Objective

The objective of this task is to validate tool arguments before the tool is executed.

The implementation demonstrates the idea of **schema before execution** by checking that the required argument is present, has the correct type, and contains a valid value.

### Implementation

Task 2 builds on the tool structure introduced in Task 1.

The `lookup_order` tool now validates its input using:

```python
validate_order_args(args)
```

The validation checks that:

* `order_id` is present.
* `order_id` is a string.
* `order_id` is not empty.

Only after these checks pass is the actual order lookup performed.

This prevents malformed or invalid arguments from reaching the tool operation.

### Happy Path

A valid argument is passed to the tool: This confirms that valid arguments are accepted and the tool executes normally.

### Failure Paths

The implementation demonstrates three rejected inputs.

#### Missing Argument

```python
{}
```

#### Incorrect Type

```python
{"order_id": 100}
```

#### Empty Value

```python
{"order_id": ""}
```

These examples prove that argument validation happens before the actual tool operation.

### Run Command

Run the implementation from the project root:

```bash
python argument_validation.py
```

The saved output demonstrates:

* Successful validation and execution.
* Rejection of a missing required argument.
* Rejection of an incorrect argument type.
* Rejection of an empty argument value.

### Automated Tests

Run:

```bash
pytest tests/test_argument_validation.py -v
```

The automated tests verify:

1. Valid arguments are accepted.
2. A missing required argument is rejected.
3. An incorrect argument type is rejected.
4. An empty argument value is rejected.

