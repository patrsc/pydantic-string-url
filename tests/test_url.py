"""Unit tests."""

import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

from pydantic_string_url import HttpUrl

FAILING_HTTP_URL = [
    "",
    "not a url",
    "ftp://example.com",
]


class User(BaseModel):
    """A user."""

    name: str
    age: int
    homepage: HttpUrl


def test_validate_http_url() -> None:
    """Test validation of HttpUrl."""
    s = "http://www.example.com"
    url = TypeAdapter(HttpUrl).validate_python(s)
    url_direct = HttpUrl(s)
    assert s == url
    assert s == url_direct
    assert isinstance(url, HttpUrl)
    assert isinstance(url_direct, HttpUrl)
    assert isinstance(url, str)
    assert isinstance(url_direct, str)


@pytest.mark.parametrize("s", FAILING_HTTP_URL)
def test_validate_http_url_fail(s: str) -> None:
    """Test failing validation of HttpUrl."""
    with pytest.raises(ValidationError):
        url = TypeAdapter(HttpUrl).validate_python(s)
        print(url)
    with pytest.raises(ValidationError):
        url_direct = HttpUrl(s)
        print(url_direct)


def test_validate_httl_url_mode() -> None:
    """Test validation of HttpUrl in BaseModel."""
    user = {"name": "John Doe", "age": 33, "homepage": "https://example.com/a/bc/"}
    john = User.model_validate(user)
    assert john.homepage == user["homepage"]
    assert isinstance(john.homepage, HttpUrl)
    assert john.homepage.url.scheme == "https"


def test_validate_httl_url_mode_fail() -> None:
    """Test failing validation of HttpUrl in BaseModel."""
    user = {"name": "Alice", "age": 32, "homepage": "not a url"}
    with pytest.raises(ValidationError):
        alice = User.model_validate(user)
        print(alice)


def test_validate_url_property() -> None:
    """Test the .url property of HttpUrl."""
    s = "https://www.example.com/path/subpath"
    u = HttpUrl(s)
    assert u == s
    assert u.url.scheme == "https"
    assert u.url.host == "www.example.com"
    assert u.url.path == "/path/subpath"
