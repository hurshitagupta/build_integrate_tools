import pytest

from argument_validation.argument_validation import lookup_order
from tool_trace.tool_trace import TRACE_LOG, trace_tool_call


def setup_function():
    TRACE_LOG.clear()


def test_successful_tool_call_is_traced():
    result = trace_tool_call( tool_name="lookup_order", tool_function=lookup_order, args={"order_id": "A100"})

    assert result == "packed"

    assert len(TRACE_LOG) == 2

    assert TRACE_LOG[0]["event"] == "tool_start"
    assert TRACE_LOG[1]["event"] == "tool_success"

    assert TRACE_LOG[1]["result"] == "packed"


def test_failed_tool_call_is_traced():
    with pytest.raises( ValueError, match="Missing required argument: order_id"):
        trace_tool_call(tool_name="lookup_order", tool_function=lookup_order, args={})

    assert len(TRACE_LOG) == 2

    assert TRACE_LOG[0]["event"] == "tool_start"
    assert TRACE_LOG[1]["event"] == "tool_error"

    assert TRACE_LOG[1]["error"] == "Missing required argument: order_id"
    


def test_trace_contains_execution_time():
    trace_tool_call(tool_name="lookup_order", tool_function=lookup_order, args={"order_id": "A100"})

    assert "duration_ms" in TRACE_LOG[1]
    assert TRACE_LOG[1]["duration_ms"] >= 0