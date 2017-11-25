import decimal
import json


def convert_decimal_to_float(obj):
    """Helper function to serilaise Decimals to float type.
       Used inside to_json().
    """
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def to_json(gen, **kwargs):
    """Convert generator *gen* to json string.

    Returns:
        string
    """
    return json.dumps(list(gen), default=convert_decimal_to_float, **kwargs)
