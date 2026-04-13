import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jose import jwt
from routes.auth import (
    create_access_token, hash_password, verify_password, SECRET_KEY, ALGORITHM
)


class TestCreateAccessToken:
    def test_returns_string(self):
        token = create_access_token("test@example.com")
        assert isinstance(token, str)

    def test_contains_email_in_sub(self):
        email = "user@test.com"
        token = create_access_token(email)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == email

    def test_has_expiry(self):
        token = create_access_token("test@example.com")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_expiry_is_7_days(self):
        token = create_access_token("test@example.com")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = datetime.utcfromtimestamp(payload["exp"])
        now = datetime.utcnow()
        diff = exp - now
        assert 6 <= diff.days <= 7

    def test_round_trip(self):
        email = "roundtrip@test.com"
        token = create_access_token(email)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == email


class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert hashed != password

    def test_verify_correct_password(self):
        password = "correctpassword123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("correctpassword123")
        assert verify_password("wrongpassword", hashed) is False

    def test_hash_is_bcrypt_format(self):
        hashed = hash_password("testpassword")
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
