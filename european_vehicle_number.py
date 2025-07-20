def clean_number(european_vehicle_number: str) -> str:
    """Cleans the European vehicle number by removing any non-digit characters."""
    return "".join(filter(str.isdigit, european_vehicle_number))


def get_vehicle_type(european_vehicle_number: str) -> int:
    """
    Returns the vehicle type based on the first character of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        int: The vehicle type.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    print(f"Cleaned vehicle number: {european_vehicle_number}")
    vehicle_type_code = int(european_vehicle_number[0:2])
    print(f"Vehicle type code: {vehicle_type_code }")
    return vehicle_type_code


def get_country_code(european_vehicle_number: str) -> int:
    """
    Returns the country code based on the first two characters of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        int: The country code.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    print(f"Cleaned vehicle number: {european_vehicle_number}")
    country_code = int(european_vehicle_number[2:4])
    print(f"Country code: {country_code}")
    return country_code


def get_check_digit(european_vehicle_number: str) -> int:
    """
    Returns the check digit of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        int: The check digit.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    print(f"Cleaned vehicle number: {european_vehicle_number}")

    if len(european_vehicle_number) < 11 or len(european_vehicle_number) > 12:
        raise ValueError(
            "The vehicle number must be 12 characters long including the check digit. "
            f"Got: {european_vehicle_number} of size {len(european_vehicle_number)}"
        )
    if len(european_vehicle_number) == 11:
        raise ValueError("The vehicle number does not include the check digit.")
    return int(european_vehicle_number[-1])


def compute_check_digit(european_vehicle_number: str) -> int:
    """
    Computes the check digit for a European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number without the check digit.

    Returns:
        int: The computed check digit.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    print(f"Cleaned vehicle number: {european_vehicle_number}")
    if len(european_vehicle_number) != 11:
        raise ValueError(
            "The vehicle number must be 11 characters long without the check digit. "
            f"Got: {european_vehicle_number} of size {len(european_vehicle_number)}"
        )
    total = 0
    for i in range(11):
        multiplier = 2 if i % 2 == 0 else 1
        digit = int(european_vehicle_number[i])
        total += sum(int(d) for d in str(digit * multiplier))
    print(f"Total before check digit: {total}")
    check_digit = (10 - total) % 10
    print(f"Check digit: {check_digit}")
    return check_digit


def validate_vehicle_number(european_vehicle_number: str) -> bool:
    """
    Validates the European vehicle number by checking the check digit.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        bool: True if the vehicle number is valid, False otherwise.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    print(f"Cleaned vehicle number: {european_vehicle_number}")

    if len(european_vehicle_number) != 12:
        raise ValueError(
            "The vehicle number must be 12 characters long including the check digit. "
            f"Got: {european_vehicle_number} of size {len(european_vehicle_number)}"
        )
    check_digit = get_check_digit(european_vehicle_number)
    computed_check_digit = compute_check_digit(european_vehicle_number[:-1])
    return check_digit == computed_check_digit
