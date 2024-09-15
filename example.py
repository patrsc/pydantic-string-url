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
urls = ["https://test.com", "some wrong url"]

url_a = TypeAdapter(HttpUrl).validate_python(urls[0])
try:
    url_b = TypeAdapter(HttpUrl).validate_python(urls[1])
except ValidationError as e:
    print(str(e))

# You can still access the Pydantic type by using the string's .url property
assert url_a.url.scheme == "https"
assert john.homepage.url.scheme == "https"
