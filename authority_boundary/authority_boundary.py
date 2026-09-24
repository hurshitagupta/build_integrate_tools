from datetime import datetime

ORDERS = {"A100": "packed","A101": "shipped",}

PROCESSED_REQUESTS = set()
AUDIT_LOG = []

def audit(event: str, order_id: str, message: str) -> None:
    AUDIT_LOG.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event": event,
            "order_id": order_id,
            "message": message,
        }
    )


def cancel_order( order_id: str, authorized: bool, request_id: str) -> str:
    if not order_id:
        raise ValueError("order_id is required")

    if not request_id:
        raise ValueError("request_id is required")

    if not authorized:
        audit(
            event="rejected",
            order_id=order_id,
            message="Unauthorized cancellation attempt",
        )
        raise PermissionError("Cancellation requires authorization")

    if request_id in PROCESSED_REQUESTS:
        audit(
            event="duplicate",
            order_id=order_id,
            message="Duplicate cancellation request ignored",
        )
        return "already processed"

    if order_id not in ORDERS:
        audit(event="rejected",order_id=order_id,message="Order not found")
        raise ValueError("Order not found")

    ORDERS[order_id] = "cancelled"
    PROCESSED_REQUESTS.add(request_id)

    audit(event="cancelled",order_id=order_id,message="Order cancelled successfully")

    return "cancelled"


def main():
    print("=== AUTHORITY BOUNDARY DEMO ===")

    print("\nHappy path:")

    result = cancel_order( order_id="A100", authorized=True, request_id="REQ-001")

    print(f"Result: {result}")

    print("\nDuplicate request:")

    duplicate_result = cancel_order(order_id="A100", authorized=True, request_id="REQ-001")

    print(f"Result: {duplicate_result}")

    print("\nUnauthorized path:")

    try:
        cancel_order(order_id="A101", authorized=False, request_id="REQ-002")
    except PermissionError as error:
        print(f"Rejected: {error}")

    print("\nAudit log:")

    for entry in AUDIT_LOG:
        print(entry)


if __name__ == "__main__":
    main()