import pytest

import authority_boundary.authority_boundary as ab


def setup_function():
    ab.ORDERS.clear()
    ab.ORDERS.update({"A100": "packed","A101": "shipped"})

    ab.PROCESSED_REQUESTS.clear()
    ab.AUDIT_LOG.clear()


def test_authorized_cancellation_success():
    result = ab.cancel_order(order_id="A100",authorized=True,request_id="REQ-001")

    assert result == "cancelled"
    assert ab.ORDERS["A100"] == "cancelled"


def test_unauthorized_cancellation_is_rejected():
    with pytest.raises(PermissionError, match="Cancellation requires authorization"):
        ab.cancel_order(order_id="A101", authorized=False, request_id="REQ-002")

    assert ab.ORDERS["A101"] == "shipped"


def test_duplicate_request_is_idempotent():
    first_result = ab.cancel_order(order_id="A100", authorized=True, request_id="REQ-001")

    second_result = ab.cancel_order(order_id="A100", authorized=True, request_id="REQ-001")

    assert first_result == "cancelled"
    assert second_result == "already processed"


def test_actions_are_audited():
    ab.cancel_order( order_id="A100", authorized=True, request_id="REQ-001")

    assert len(ab.AUDIT_LOG) == 1
    assert ab.AUDIT_LOG[0]["event"] == "cancelled"