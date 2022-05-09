import json
from typing import Any

from pydantic import BaseModel as PydanticBaseModel, root_validator


class BaseModel(PydanticBaseModel):
    def populate(self, **kwargs):
        for field_name, value in kwargs.items():
            setattr(self, field_name, value)

    @root_validator(pre=True)
    def convert_str_to_dict(cls, data: Any) -> Any:
        for field_name, field_value in data.items():
            field = cls.__fields__.get(field_name)
            if (
                field is not None
                and issubclass(field.type_, BaseModel)
                and isinstance(field_value, str)
            ):
                data[field_name] = json.loads(field_value)
        return data
