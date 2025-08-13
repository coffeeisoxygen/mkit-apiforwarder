import contextlib
import os
from pathlib import Path

import pytest
import yaml
from src.domain.member.dta_member import (
    check_duplicate_memberids,
    load_and_validate_yaml,
)
from src.domain.member.rep_member import MemberRepository
from src.domain.member.sch_member import MemberInDB

# Sample member data for tests
SAMPLE_MEMBERS = [
    {
        "memberid": "user1",
        "name": "User One",
        "pin": "123456",
        "password": "TestPassword90",
        "ipaddress": "192.168.1.10",
        "report_url": "http://report1.local",
        "is_active": True,
        "allow_nosign": False,
    },
    {
        "memberid": "user2",
        "name": "User Two",
        "pin": "567814",
        "password": "TestPassword90",
        "ipaddress": "192.168.1.20",
        "report_url": "http://report2.local",
        "is_active": False,
        "allow_nosign": True,
    },
]


def write_yaml_file(path: Path, members: list[dict]):
    data = {"members": members}
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)


def test_check_duplicate_memberids():
    members = [{"memberid": "a"}, {"memberid": "b"}, {"memberid": "a"}]
    assert check_duplicate_memberids(members) == ["a"]


def get_data_path():
    return Path(os.environ.get("DATA_PATH", "tests/data/"))


def test_load_and_validate_yaml_success():
    data_dir = get_data_path()
    yaml_file = data_dir / "members.yaml"
    write_yaml_file(yaml_file, SAMPLE_MEMBERS)
    members = load_and_validate_yaml(yaml_file)
    assert isinstance(members, list)
    assert all(isinstance(m, MemberInDB) for m in members)
    assert members[0].memberid == "user1"
    assert members[1].memberid == "user2"


def test_load_and_validate_yaml_file_not_found(tmp_path):
    yaml_file = tmp_path / "notfound.yaml"
    with pytest.raises(FileNotFoundError):
        load_and_validate_yaml(yaml_file)


def test_load_and_validate_yaml_invalid_structure(tmp_path):
    yaml_file = tmp_path / "members.yaml"
    with yaml_file.open("w", encoding="utf-8") as f:
        yaml.safe_dump({"not_members": []}, f)
    with pytest.raises(ValueError):
        load_and_validate_yaml(yaml_file)


def test_load_and_validate_yaml_duplicate_memberids(tmp_path):
    yaml_file = tmp_path / "members.yaml"
    members = [{"memberid": "x"}, {"memberid": "x"}]
    write_yaml_file(yaml_file, members)
    with pytest.raises(ValueError):
        load_and_validate_yaml(yaml_file)


def test_load_and_validate_yaml_invalid_member(tmp_path):
    yaml_file = tmp_path / "members.yaml"
    # Missing required fields for MemberInDB
    members = [{"memberid": "x"}]
    write_yaml_file(yaml_file, members)
    with pytest.raises(ValueError):
        load_and_validate_yaml(yaml_file)


def test_member_repository_basic():
    data_dir = get_data_path()
    yaml_file = data_dir / "members.yaml"
    write_yaml_file(yaml_file, SAMPLE_MEMBERS)
    repo = MemberRepository(file_path=yaml_file)
    assert repo.get_member_count() == 2
    assert repo.has_member("user1")
    member = repo.get_member_by_id("user1")
    assert member is not None
    assert member.memberid == "user1"
    assert repo.is_member_active("user1") is True
    assert repo.is_member_active("user2") is False
    assert repo.check_allow_nosign("user2") is True
    assert repo.check_allow_nosign("user1") is False
    assert set(repo.get_member_ids()) == {"user1", "user2"}
    all_members = repo.get_all_members()
    assert len(all_members) == 2


def test_member_repository_reload_fallback():
    data_dir = get_data_path()
    yaml_file = data_dir / "members.yaml"
    write_yaml_file(yaml_file, SAMPLE_MEMBERS)
    repo = MemberRepository(file_path=yaml_file)
    # Remove file to trigger fallback
    yaml_file.unlink()
    with contextlib.suppress(FileNotFoundError):
        repo.reload()
    # Data should remain unchanged (if fallback implemented)
    assert repo.get_member_count() == 2


def test_member_repository_clear_data():
    data_dir = get_data_path()
    yaml_file = data_dir / "members.yaml"
    write_yaml_file(yaml_file, SAMPLE_MEMBERS)
    repo = MemberRepository(file_path=yaml_file)
    repo.clear_data()
    assert repo.get_member_count() == 0
    assert repo.get_member_by_id("user1") is None
