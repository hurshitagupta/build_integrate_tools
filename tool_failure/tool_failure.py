from time import sleep

from argument_validation.argument_validation import validate_order_args


class TransientToolError(Exception):
    pass


class PermanentToolError(Exception):
    pass


def lookup_order(args: dict) -> str:
    validate_order_args(args)

    order_id = args["order_id"]

    if order_id == "TEMP_FAIL":
        raise TransientToolError("Temporary service failure")

    if order_id == "PERM_FAIL":
        raise PermanentToolError("Permanent tool failure")

    orders = {
        "A100": "packed",
        "A101": "shipped",
    }

    return orders.get(order_id, "not found")


def run_with_retry(args: dict,max_retries: int = 2,backoff_seconds: float = 0.1) -> str:
    attempts = 0

    while True:
        try:
            attempts += 1

            print(f"Attempt {attempts}")

            result = lookup_order(args)

            print(f"Completed after {attempts} attempt(s)")
            return result

        except TransientToolError as error:
            if attempts > max_retries:
                print("Retry limit reached")
                raise

            print(f"Transient failure: {error}")
            print("Retrying...")

            sleep(backoff_seconds)

        except PermanentToolError:
            print("Permanent failure detected - no retry")
            raise


def main():
    print("=== TOOL FAILURE DEMO ===")

    print("\nHappy path:")

    result = run_with_retry({"order_id": "A100"})

    print(f"Result: {result}")

    print("\nTransient failure path:")

    try:
        run_with_retry({"order_id": "TEMP_FAIL"},max_retries=2)
    except TransientToolError as error:
        print(f"Final failure: {error}")

    print("\nPermanent failure path:")

    try:
        run_with_retry({"order_id": "PERM_FAIL"},max_retries=2)
    except PermanentToolError as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    main()