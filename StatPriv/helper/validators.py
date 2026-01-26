def _validate_type(value: str, value_type):
    try: 
        value_type(value)
        return True
    except ValueError:
        return "Please enter a valid numeric value"

def _validate_probability(value: str):
    try:
        v = float(value)
    except ValueError:
        return "Please enter a valid number"

    if v < 0:
        return "Probability must be non-negative"

    return True

