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

---

## Task 3 — Tool Failure

### Objective

The objective of this task is to handle tool execution failures safely and predictably.

The implementation distinguishes between transient failures, which may be retried, and permanent failures, which should fail immediately.

### Implementation

Task 3 introduces two custom failure types:

```python
TransientToolError
PermanentToolError
```

The `lookup_order` tool can now demonstrate three behaviors:

* Successful execution
* Temporary failure
* Permanent failure

The execution is wrapped using:

```python
run_with_retry()
```

This function retries only transient failures and stops after a fixed retry limit.

Argument validation from Task 2 is also reused before tool execution.

### Happy Path

A valid order lookup is executed.

This proves that the tool completes normally without unnecessary retries.

### Transient Failure Path

The following input is used to simulate a temporary tool failure:

```python
{"order_id": "TEMP_FAIL"}
```

The error is classified as a `TransientToolError`. Because transient failures may recover, the operation is retried.


### Permanent Failure Path

The following input is used to simulate a permanent failure:

```python
{"order_id": "PERM_FAIL"}
```

This raises a `PermanentToolError`.

Permanent failures are not retried. This prevents unnecessary retry attempts for failures that are not expected to recover.

### Retry Strategy

The implementation follows the assessment requirement that only classified transient failures should be retried.

The retry configuration is:

```text
Maximum retries: 2
Backoff delay: 0.1 seconds
```

A small backoff is added between retries to avoid immediately repeating a failed operation.

The automated tests use a zero-second backoff so that the test suite runs quickly while checking the same retry behavior.

### Run Command

Run the implementation from the project root:

```bash
python tool_failure.py
```

### Automated Tests

Run:

```bash
pytest tests/test_tool_failure.py -v
```

The automated tests verify:

1. Successful tool execution.
2. A transient failure is retried.
3. The retry limit is enforced.
4. A permanent failure is not retried.

---

## Task 4 — Authority Boundary

### Objective

The objective of this task is to enforce an authority boundary around a tool that performs a side effect.

The implementation uses an order cancellation tool because cancellation changes system state and should not be allowed without explicit authorization.

The task demonstrates authorization, idempotency, audit logging, validation, and rejection of unauthorized actions.

### Implementation

The task introduces a `cancel_order()` function that requires:

```python
order_id
authorized
request_id
```

The tool only performs the cancellation when authorization is explicitly granted.

Before changing any state, the tool checks:

* That `order_id` is present.
* That `request_id` is present.
* That the action is authorized.
* That the same request has not already been processed.
* That the requested order exists.

This creates a clear authority boundary around the side-effecting operation.

### Happy Path

An authorized cancellation request is executed.

This proves that an authorized request is allowed to perform the side effect.

### Unauthorized Path

An unauthorized request is executed. The order remains unchanged.

### Idempotency

The implementation uses `request_id` to prevent duplicate processing.

This protects the system from repeated side effects caused by retries or duplicate requests.

### Audit Logging

Important actions are recorded in an in-memory audit log.

The audit log records:

* Successful cancellation
* Unauthorized attempts
* Duplicate requests
* Rejected requests for unknown orders

Each entry contains:

```text
timestamp
event
order_id
message
```

This provides reviewable evidence of what action occurred and why.

### Run Command

Run the implementation from the project root:

```bash
python authority_boundary.py
```

The output demonstrates:

* Authorized cancellation
* Duplicate request handling
* Unauthorized rejection
* Audit log entries

### Automated Tests

Run:

```bash
pytest tests/test_authority_boundary.py -v
```

The automated tests verify:

1. An authorized cancellation succeeds.
2. An unauthorized cancellation is rejected.
3. Duplicate requests are handled idempotently.
4. Successful actions are recorded in the audit log.

### Measurement and Traceability

The implementation provides measurable and traceable evidence through:

* Number of audit log entries
* Recorded event types
* Processed request IDs
* Order state before and after cancellation

The audit trail makes it possible to determine whether an action was:

```text
cancelled
duplicate
rejected
```

---

## Task 5 — Tool Trace

### Objective

The objective of this task is to make tool execution traceable.

The implementation records the start of each tool call, whether it succeeds or fails, the result or error, and the execution duration.

This provides observable evidence for both successful and failed tool executions.

### Implementation

Task 5 introduces a tracing wrapper:

```python
trace_tool_call()
```

The wrapper executes an existing tool while recording trace events in:

```python
TRACE_LOG
```

The `lookup_order` tool from Task 2 is reused so that validation and tool behavior are not duplicated.

Each tool call records a `tool_start` event before execution.

If the tool succeeds, a `tool_success` event is recorded.

If the tool fails, a `tool_error` event is recorded and the original exception is re-raised.

### Happy Path

A valid tool call is executed using:

```python
trace_tool_call(
    tool_name="lookup_order",
    tool_function=lookup_order,
    args={"order_id": "A100"},
)
```

The trace contains:

```text
tool_start
tool_success
```

The successful trace also includes the result and execution duration.

### Failure Path

The failure path passes an invalid argument:

```python
{}
```

The existing argument validation from Task 2 rejects the request because `order_id` is missing.


The trace records:

```text
tool_start
tool_error
```

The failure is recorded without hiding the original exception.

### Trace Information

Each trace provides information about the tool execution.

A start event records:

* Event type
* Tool name
* Arguments

A success event records:

* Event type
* Tool name
* Result
* Execution duration in milliseconds

A failure event records:

* Event type
* Tool name
* Error message
* Execution duration in milliseconds

### Measurement

The implementation records:

* Execution duration in milliseconds
* Total number of trace events
* Successful and failed execution events

For the demonstration containing one successful call and one failed call, four trace events are generated:

```text
tool_start
tool_success
tool_start
tool_error
```


### Run Command

Run the implementation from the project root:

```bash
python tool_trace.py
```

### Automated Tests

Run:

```bash
pytest tests/test_tool_trace.py -v
```

The automated tests verify:

1. A successful tool call creates `tool_start` and `tool_success` events.
2. A failed tool call creates `tool_start` and `tool_error` events.
3. Successful trace records include execution duration.





