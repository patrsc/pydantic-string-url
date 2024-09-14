"""HTTP URL.

The class HttpUrl here fixes a problem with the pydantic v2 HttpUrl class.
It is based on str, so it is compatible with the URLs expected from other packages.

See Also
--------
- https://github.com/pydantic/pydantic/issues/7186
- https://github.com/pydantic/pydantic/discussions/8211
- https://github.com/pydantic/pydantic/discussions/6395

"""

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic import HttpUrl as PyHttpUrl
from pydantic import TypeAdapter
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema


class HttpUrl(str):
    """Represents a HTTP URL."""

    def __init__(self, url: str) -> None:
        """Initialize HttpUrl."""
        validate_url(url)
        str.__init__(url)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # pylint: disable=unused-argument
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Get pydantic core schema."""
        return core_schema.no_info_after_validator_function(cls._validate, handler(str))

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """Get pydantic JSON schema."""
        json_schema = handler(schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema["format"] = "uri"
        json_schema["minLength"] = 1
        json_schema["maxLength"] = 65536
        json_schema["examples"] = ["http://www.example.com/"]
        return json_schema

    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return validate_url(__input_value)


def validate_url(s: str) -> str:
    """Validate if string has the format of a proper HTTP URL."""
    # use pydantic's HttpUrl class just for validation
    a = TypeAdapter(PyHttpUrl)
    a.validate_python(s, strict=True)
    return s
