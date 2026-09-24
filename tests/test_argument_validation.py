import pytest

from argument_validation.argument_validation import lookup_order


def test_valid_arguments_success():
    result = lookup_order({"order_id": "A100"})

    assert result == "packed"


def test_missing_argument_is_rejected():
    with pytest.raises(ValueError,match="Missing required argument: order_id"):
        lookup_order({})


def test_wrong_argument_type_is_rejected():
    with pytest.raises(TypeError,match="order_id must be a string"):
        lookup_order({"order_id": 100})


def test_empty_argument_is_rejected():
    with pytest.raises(ValueError,match="order_id cannot be empty"):
        lookup_order({"order_id": ""})