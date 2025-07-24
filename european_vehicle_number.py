from logger import logger
from vehicles_details import TRACTIVE_VEHICLE_TYPE


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
    logger.debug(f"Cleaned vehicle number: {european_vehicle_number}")
    vehicle_type_code = int(european_vehicle_number[0:2])
    logger.info(f"Vehicle type code: {vehicle_type_code }")
    return vehicle_type_code


def get_tractive_vehicle_type(vehicle_type_code: int) -> str:
    """
    Returns the description of the tractive vehicle type based on the vehicle type code.

    Args:
        vehicle_type_code (int): The vehicle type code.

    Returns:
        str: The description of the tractive vehicle type.
    """
    if len(str(vehicle_type_code)) > 2:
        raise ValueError("Vehicle type code must be 2 digits long.")
    elif len(str(vehicle_type_code)) == 2:
        if vehicle_type_code // 10 != 9:
            raise ValueError(
                f"Vehicle type code should be between 90 and 99, but is not: {vehicle_type_code}."
            )
        else:
            vehicle_type_code = vehicle_type_code % 10
    return TRACTIVE_VEHICLE_TYPE.get(vehicle_type_code, "Unknown")


def get_country_code(european_vehicle_number: str) -> int:
    """
    Returns the country code based on the first two characters of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        int: The country code.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    logger.debug(f"Cleaned vehicle number: {european_vehicle_number}")
    country_code = int(european_vehicle_number[2:4])
    logger.debug(f"Country code: {country_code}")
    return country_code


def get_national_number(european_vehicle_number: str) -> str:
    """
    Returns the national number based on the characters after the first two of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        str: The national number.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    logger.info(f"Cleaned vehicle number: {european_vehicle_number}")
    national_number = european_vehicle_number[4:11]
    logger.info(f"National number: {national_number}")
    return national_number


def get_rolling_stock_group(european_vehicle_number: str) -> str:
    """
    Returns the rolling stock group based on the first character of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        str: The rolling stock group.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    logger.info(f"Cleaned vehicle number: {european_vehicle_number}")
    vehicle_type = get_vehicle_type(european_vehicle_number)
    if vehicle_type < 50 or 80 <= vehicle_type <= 89:
        rolling_stock_group = "Wagons"
    elif 50 <= vehicle_type <= 79:
        rolling_stock_group = "Hauled passenger vehicles"
    else:
        national_number = get_national_number(european_vehicle_number)
        if national_number.startswith("9"):
            rolling_stock_group = "Special vehicles"
        else:
            rolling_stock_group = "Tractive rolling stock and units in a trainset in fixed or pre-defined formation"
    logger.info(f"Rolling stock group code: {rolling_stock_group}")
    return rolling_stock_group


def get_serial_number(european_vehicle_number: str) -> str:
    """
    Returns the serial number based on the last three characters of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        str: The serial number.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    logger.info(f"Cleaned vehicle number: {european_vehicle_number}")
    serial_number = european_vehicle_number[8:11]
    logger.info(f"Serial number: {serial_number}")
    return serial_number


def get_check_digit(european_vehicle_number: str) -> int:
    """
    Returns the check digit of the European vehicle number.

    Args:
        european_vehicle_number (str): The vehicle number.

    Returns:
        int: The check digit.
    """
    european_vehicle_number = clean_number(european_vehicle_number)
    logger.info(f"Cleaned vehicle number: {european_vehicle_number}")

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
    logger.info(f"Cleaned vehicle number: {european_vehicle_number}")
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
    logger.info(f"Total before check digit: {total}")
    check_digit = (10 - total) % 10
    logger.info(f"Check digit: {check_digit}")
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
    logger.info(f"Cleaned vehicle number: {european_vehicle_number}")

    if len(european_vehicle_number) != 12:
        raise ValueError(
            "The vehicle number must be 12 characters long including the check digit. "
            f"Got: {european_vehicle_number} of size {len(european_vehicle_number)}"
        )
    check_digit = get_check_digit(european_vehicle_number)
    computed_check_digit = compute_check_digit(european_vehicle_number[:-1])
    return check_digit == computed_check_digit
