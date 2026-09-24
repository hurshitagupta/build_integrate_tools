from time import perf_counter

from argument_validation.argument_validation import lookup_order


TRACE_LOG = []


def trace_tool_call(tool_name: str, tool_function, args: dict):
    start_time = perf_counter()

    TRACE_LOG.append(
        {
            "event": "tool_start",
            "tool": tool_name,
            "args": args,
        }
    )

    try:
        result = tool_function(args)

        duration_ms = (perf_counter() - start_time) * 1000

        TRACE_LOG.append(
            {
                "event": "tool_success",
                "tool": tool_name,
                "result": result,
                "duration_ms": round(duration_ms, 3),
            }
        )

        return result

    except Exception as error:
        duration_ms = (perf_counter() - start_time) * 1000

        TRACE_LOG.append(
            {
                "event": "tool_error",
                "tool": tool_name,
                "error": str(error),
                "duration_ms": round(duration_ms, 3),
            }
        )

        raise


def main():
    TRACE_LOG.clear()

    print("=== TOOL TRACE DEMO ===")

    print("\nHappy path:")

    result = trace_tool_call(tool_name="lookup_order", tool_function=lookup_order, args={"order_id": "A100"})

    print(f"Result: {result}")

    print("\nFailure path:")

    try:
        trace_tool_call(tool_name="lookup_order", tool_function=lookup_order, args={})
    except ValueError as error:
        print(f"Rejected: {error}")

    print("\nTrace log:")

    for entry in TRACE_LOG:
        print(entry)

    print(f"\nTotal trace events: {len(TRACE_LOG)}")


if __name__ == "__main__":
    main()