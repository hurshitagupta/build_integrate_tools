import pytest

from tool_failure.tool_failure import PermanentToolError,TransientToolError,run_with_retry

def test_tool_success():
    result = run_with_retry({"order_id": "A100"},max_retries=2,backoff_seconds=0)

    assert result == "packed"


def test_transient_failure_retries_then_fails(capsys):
    with pytest.raises(TransientToolError):
        run_with_retry({"order_id": "TEMP_FAIL"},max_retries=2,backoff_seconds=0)

    output = capsys.readouterr().out

    assert "Attempt 1" in output
    assert "Attempt 2" in output
    assert "Attempt 3" in output
    assert "Retry limit reached" in output


def test_permanent_failure_is_not_retried(capsys):
    with pytest.raises(PermanentToolError):
        run_with_retry({"order_id": "PERM_FAIL"},max_retries=2,backoff_seconds=0)

    output = capsys.readouterr().out

    assert "Attempt 1" in output
    assert "Attempt 2" not in output
    assert "Permanent failure detected - no retry" in output