import pytest

from european_vehicle_number import (
    compute_check_digit,
    clean_number,
    get_vehicle_type,
    get_country_code,
    get_national_number,
    get_serial_number,
    get_rolling_stock_group,
    get_tractive_vehicle_type,
    get_check_digit,
    validate_vehicle_number,
)


def test_clean_number():
    assert clean_number("33844796100") == "33844796100"
    assert clean_number("33-84-4796-100-8") == "338447961008"
    assert clean_number("3384479610A") == "3384479610"
    assert clean_number("NL 33 84 4796 100") == "33844796100"
    assert clean_number("33844796100 ") == "33844796100"


def test_compute_check_digit():
    assert compute_check_digit("33844796100") == 8
    assert compute_check_digit("31513320198") == 0


def test_compute_check_digit_invalid_length():
    with pytest.raises(ValueError):
        compute_check_digit("1234567890")  # Too short
    with pytest.raises(ValueError):
        compute_check_digit("1234567890123")  # Too long


def test_get_vehicle_type():
    assert get_vehicle_type("33844796100") == 33
    assert get_vehicle_type("31-51-3320-198-0") == 31


def test_get_country_code():
    assert get_country_code("33844796100") == 84
    assert get_country_code("31-51-3320-198-0") == 51


def test_get_check_digit():
    assert get_check_digit("338447961008") == 8
    assert get_check_digit("315133201980") == 0


def test_validate_vehicle_number_invalid_length():
    with pytest.raises(ValueError):
        validate_vehicle_number("1234567890")  # Too short
    with pytest.raises(ValueError):
        validate_vehicle_number("1234567890123")  # Too long
    with pytest.raises(ValueError):
        validate_vehicle_number("33844796100")  # Missing check digit


def tets_validate_vehicle_number():
    assert validate_vehicle_number("338447961008") is True
    assert validate_vehicle_number("315133201980") is True
    assert validate_vehicle_number("338447961002") is False  # Incorrect check digit


def test_get_national_number():
    assert get_national_number("338447961008") == "4796100"
    assert get_national_number("31-51-3320-198") == "3320198"


def test_get_serial_number():
    assert get_serial_number("338447961008") == "100"
    assert get_serial_number("31-51-3320-198") == "198"


def test_get_rolling_stock_group():
    assert (
        get_rolling_stock_group("93-84-8999999")
        == "Tractive rolling stock and units in a trainset in fixed or pre-defined formation"
    )
    assert get_rolling_stock_group("51-51-3320-198") == "Hauled passenger vehicles"


def test_get_tractive_vehicle_type():
    assert get_tractive_vehicle_type(0) == "Miscellaneous"
    assert get_tractive_vehicle_type(90) == "Miscellaneous"
    with pytest.raises(ValueError):
        get_tractive_vehicle_type(81)
    with pytest.raises(ValueError):
        get_tractive_vehicle_type(100)
