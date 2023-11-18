def valid_coordinate(value):
    try:
        # Attempt to convert the string to a float
        float_value = float(value)

        # Check if the float is within the desired range
        if -90 <= float_value <= 90:
            return True
        else:
            return False
    except ValueError:
        # The string cannot be converted to a float
        return False


def validate_elevation(string):
    try:
        value = float(string)
        return value
    except ValueError:
        return None

def validate_float(string):
    try:
        value = float(string)
        return value
    except ValueError:
        return None



def RGBA2String(list):
    return ','.join(map(str, list))



def validate_ratio_json(float_list):
    # Check if the length of the list is 4
    if len(float_list) != 4:
        return "10,10,10,50"
    # Check if each float is in the range of 0-100
    for f in float_list:
        if not 0 <= f <= 100:
            return "10,10,10,50"
    # If all validations pass, return the string representation of the list
    return ','.join([format(f, '.1f') for f in float_list])


def validate_euqla_ratio_json(float_list):
    # Check if the length of the list is 2
    if len(float_list) != 2:
        return "10,50"
    # Check if each float is in the range of 0-100
    for f in float_list:
        if not 0 <= f <= 100:
            return "10,50"
    # If all validations pass, return the string representation of the list
    return ','.join(map(str, float_list))


def check_ratio_string(input_str):
    # Split the string into a list of floats
    float_list = input_str.split(',')

    # Check if the list contains exactly 4 floats
    if len(float_list) != 4:
        return None
    # Check if each element is a valid float within the range of 0-100
    try:
        float_list = [float(num) for num in float_list]
        for num in float_list:
            if not 0 <= num <= 100:
                return None
    except ValueError:
        return None
    # If all validations pass, return the list of floats
    return float_list


def check_equal_ratio_string(input_str):
    # Split the string into a list of floats
    float_list = input_str.split(',')

    # Check if the list contains exactly 2 floats
    if len(float_list) != 2:
        return None
    # Check if each element is a valid float within the range of 0-100
    try:
        float_list = [float(num) for num in float_list]
        for num in float_list:
            if not 0 <= num <= 100:
                return None
    except ValueError:
        return None
    # If all validations pass, return the list of floats
    return float_list


def validate_float_string_5(input_string):
    # Split the input string into a list of substrings
    elements = input_string.split(',')

    # Check if there are exactly 5 elements
    if len(elements) == 5:
        # Try to convert each element to a float
        try:
            float_list = [float(item) for item in elements]
            return float_list
        except ValueError:
            # If any conversion fails, return None
            return None
    else:
        # If the number of elements is not 5, return None
        return None


def float2str_no0(value):
    value = float(value)
    str = "{:.2f}".format(value)  # Convert to string with two decimal places
    str = str.rstrip('0').rstrip('.') if '.' in str else str
    return str