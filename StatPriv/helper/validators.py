def _validate_type(value: str, value_type):
    try: 
        value_type(value)
        return True
    except ValueError:
        return "Please enter a valid numeric value"
