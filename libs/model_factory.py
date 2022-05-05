from datetime import datetime

from dataclass_factory import Factory, Schema

datetime_schema = Schema(
    parser=lambda value: value,
    serializer=lambda value: value,
)

factory = Factory(
    schemas={
        datetime: datetime_schema,
    },
)
