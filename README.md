# pydantic-string-url

Pydantic URL types that are based on the `str` class.

## Introduction

Since [Pydantic](https://docs.pydantic.dev/) v2 the URL-realated types are not based on the
standard [Python](https://www.python.org/) `str` class any more.

This decision comes with some issues:
* URLs cannot be directly passed to library packages that expect `str`, you must use `str(url)`
  instead
* some internal normalization is done, so the input strings are not always preserved when a
  URL object is created (trailing slashes could be added), which might be problematic for some
  applications

This package provides direct replacements for the Pydantic types:
* `AnyUrl`
* `AnyHttpUrl`
* `HttpUrl`
* `AnyWebsocketUrl`
* `WebsocketUrl`
* `FileUrl`
* `FtpUrl`

Those replacement types are based on strings, so they are also a `str`, preserve the original input
string and use the same validation functions as their Pydantic counterparts.

See also the discussions here:
- https://github.com/pydantic/pydantic/issues/7186
- https://github.com/pydantic/pydantic/discussions/8211
- https://github.com/pydantic/pydantic/discussions/6395

## Usage

The package [pydantic-string-url](#) is available on [PyPi](https://pypi.org/), so it can be
installed with Python package managers such as `pip` or [poetry](https://python-poetry.org/).

Usage example:

```py
"""Example."""

from pydantic import BaseModel, TypeAdapter, ValidationError

from pydantic_string_url import HttpUrl


# Use inside BaseModel
class User(BaseModel):
    """A user."""

    name: str
    age: int
    homepage: HttpUrl


user = {"name": "John Doe", "age": 33, "homepage": "https://example.com"}

invalid_user = {"name": "Alice", "age": 32, "homepage": "not a url"}

john = User.model_validate(user)
assert john.homepage == "https://example.com"  # no trailing slash was added
try:
    alice = User.model_validate(invalid_user)
except ValidationError as e:
    print(str(e))

# Use standalone
urls = ["https://google.com", "some wrong url"]

url_a = TypeAdapter(HttpUrl).validate_python(urls[0])
try:
    url_b = TypeAdapter(HttpUrl).validate_python(urls[1])
except ValidationError as e:
    print(str(e))

```

## Licence

MIT
