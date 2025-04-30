# tests/test_codee.py
import pytest
from unittest import mock
from codee.codee import (
    contains_open_house,
    extract_phone_numbers,
    normalize_phone,
    clean_name,
    escape_special_characters,
    ensure_string,
    transform_record,
    extract_refferal_or_not,
    extract_city_state,
    scrape_website,
    push_user_to_database,
    push_to_database,
    get_info_db_zil,
    send_slack_message,
    send_email,
    send_message,
    text_exists,
    close_geometry,
)

# ----------------- Basic Utility Tests -----------------

def test_contains_open_house():
    assert contains_open_house("Open House today!")
    assert not contains_open_house("Just a regular house.")
    print("[test_contains_open_house] PASSED")

def test_extract_phone_numbers():
    nums = extract_phone_numbers("Contact: (123) 456-7890 or 987-654-3210")
    assert "(123) 456-7890" in nums
    assert "987-654-3210" in nums
    print("[test_extract_phone_numbers] PASSED")

def test_normalize_phone():
    assert normalize_phone("(123) 456-7890") == "1234567890"
    assert normalize_phone("123.456.7890") == "1234567890"
    print("[test_normalize_phone] PASSED")

def test_clean_name():
    assert clean_name("John Doe (Realtor)") == "John Doe"
    print("[test_clean_name] PASSED")

def test_escape_special_characters():
    result = escape_special_characters("a+b*c?d.")
    assert "\\+" in result and "\\*" in result and "\\?" in result and "\\." in result
    print("[test_escape_special_characters] PASSED")

def test_ensure_string():
    assert ensure_string(123) == "123"
    assert ensure_string(None) == ""
    print("[test_ensure_string] PASSED")

def test_transform_record():
    record = {"Full Name": "Jane", "Email": "jane@example.com", "phones": "123", "linkedin": "url", "facebook": ""}
    out = transform_record(record, "realtor")
    assert out["Full Name"] == "Jane"
    assert "facebook" in out
    print("[test_transform_record] PASSED")

# ----------------- External API Tests (Mocked) -----------------

@mock.patch("codee.codee.requests.post")
def test_extract_refferal_or_not(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "True"}}]
    }
    assert extract_refferal_or_not("Looking for an agent in NY") is True
    print("[test_extract_refferal_or_not] PASSED")

@mock.patch("codee.codee.requests.post")
def test_extract_city_state(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "address: Buffalo, NY"}}]
    }
    result = extract_city_state("Need a realtor in Buffalo NY")
    assert "Buffalo" in result
    print("[test_extract_city_state] PASSED")

@mock.patch("codee.codee.requests.get")
def test_scrape_website(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"<html><p>email@example.com</p><p>Phone: (123)456-7890</p></html>"
    results, _ = scrape_website("http://fake.com", "http://fake.com")
    assert any("phone" in r or "email" in r for r in results)
    print("[test_scrape_website] PASSED")

# ----------------- Database Operations (Mocked) -----------------

@mock.patch("codee.codee.MongoClient")
def test_push_user_to_database(mock_mongo):
    client = mock.MagicMock()
    mock_mongo.return_value = client
    push_user_to_database("John", "Doe", True, False, True, "john@example.com", "1234567890", "fburl", ["county1"])
    db = client.__getitem__.return_value
    col = db.__getitem__.return_value
    assert col.insert_one.called
    print("[test_push_user_to_database] PASSED")

@mock.patch("codee.codee.MongoClient")
def test_push_to_database(mock_mongo):
    client = mock.MagicMock()
    mock_mongo.return_value = client
    push_to_database("profile", "post", "group", "now", ["county"], "text", "poster", "location")
    db = client.__getitem__.return_value
    col = db.__getitem__.return_value
    assert col.insert_one.called
    print("[test_push_to_database] PASSED")

@mock.patch("codee.codee.MongoClient")
def test_get_info_db_zil(mock_mongo):
    client = mock.MagicMock()
    db = client.__getitem__.return_value
    col = db.__getitem__.return_value
    col.find_one.return_value = {"Full Name": "Agent"}
    mock_mongo.return_value = client
    result = get_info_db_zil("Agent")
    assert result["Full Name"] == "Agent"
    print("[test_get_info_db_zil] PASSED")

# ----------------- Slack and Email (Mocked) -----------------

@mock.patch("codee.codee.WebClient")
def test_send_slack_message(mock_slack):
    instance = mock_slack.return_value
    instance.chat_postMessage.return_value = {"ts": "1234"}
    send_slack_message("Test message", "channel123")
    assert instance.chat_postMessage.called
    print("[test_send_slack_message] PASSED")

@mock.patch("codee.codee.smtplib.SMTP")
def test_send_email(mock_smtp):
    instance = mock_smtp.return_value.__enter__.return_value
    send_email("Subject", "Body", "to@example.com")
    assert instance.sendmail.called
    print("[test_send_email] PASSED")

@mock.patch("codee.codee.requests.post")
def test_send_message(mock_post):
    mock_post.return_value.status_code = 200
    send_message("+1234567890", "Test message")
    assert mock_post.called
    print("[test_send_message] PASSED")

# ----------------- Text and Geo Tests -----------------

@mock.patch("codee.codee.MongoClient")
def test_text_exists(mock_mongo):
    client = mock.MagicMock()
    db = client.__getitem__.return_value
    col = db.__getitem__.return_value
    col.find_one.return_value = {"text": "exists"}
    mock_mongo.return_value = client
    assert text_exists("exists") is True
    print("[test_text_exists] PASSED")

@mock.patch("codee.codee.gpd.read_file")
def test_close_geometry(mock_gpd):
    from shapely.geometry import LineString
    line = LineString([(0, 0), (1, 1)])
    closed = close_geometry(line)
    assert closed.equals(line) or closed.is_ring
    print("[test_close_geometry] PASSED")
