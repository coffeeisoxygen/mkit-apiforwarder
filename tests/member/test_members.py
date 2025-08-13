import ipaddress

import pytest
from pydantic import ValidationError
from src.domain.member.sch_member import MemberInDB


def valid_member_dict():
    return {
        "memberid": "M12345",
        "name": "John Doe",
        "pin": "123456",
        "password": "password123",
        "is_active": True,
        "ipaddress": "192.168.1.1",
        "report_url": "http://example.com/report",
        "allow_nosign": False,
    }


def test_valid_member_in_db():
    data = valid_member_dict()
    member = MemberInDB(**data)
    assert member.memberid == data["memberid"]
    assert member.name == data["name"]
    assert member.pin.get_secret_value() == data["pin"]
    assert member.password.get_secret_value() == data["password"]
    assert member.is_active is True
    assert member.ip_address == ipaddress.IPv4Address(data["ipaddress"])
    assert str(member.report_url) == data["report_url"]  # <-- fix: compare as string
    assert member.allow_nosign is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("memberid", ""),  # too short
        ("memberid", "123"),  # too short
        ("memberid", "M@123"),  # invalid char
        ("name", ""),  # empty name
        ("pin", ""),  # empty pin
        ("password", ""),  # empty password
        ("ipaddress", "not_an_ip"),  # invalid IP
        ("report_url", "not_a_url"),  # invalid URL
    ],
)
def test_invalid_member_fields(field, value):
    data = valid_member_dict()
    data[field] = value
    with pytest.raises(ValidationError):
        MemberInDB(**data)


def test_pin_and_password_accept_int():
    data = valid_member_dict()
    data["pin"] = 123456
    data["password"] = 987654
    member = MemberInDB(**data)
    assert member.pin.get_secret_value() == "123456"
    assert member.password.get_secret_value() == "987654"


def test_missing_required_fields():
    data = valid_member_dict()
    del data["memberid"]
    with pytest.raises(ValidationError):
        MemberInDB(**data)


def test_extra_fields_forbidden():
    data = valid_member_dict()
    data["extra_field"] = "should not be allowed"
    with pytest.raises(ValidationError):
        MemberInDB(**data)
