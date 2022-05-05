class BaseModel:
    def populate(self, **kwargs):
        for field_name, value in kwargs.items():
            setattr(self, field_name, value)
