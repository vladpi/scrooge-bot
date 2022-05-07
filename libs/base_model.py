from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def populate(self, **kwargs):
        for field_name, value in kwargs.items():
            setattr(self, field_name, value)
