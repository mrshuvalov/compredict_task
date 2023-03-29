from pydantic import BaseModel
from typing import List, Optional


class StandardizedData(BaseModel):
    success: bool
    result: Optional[dict]


class SensorData(BaseModel):
    __root__: List[List[float]]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, dict):
            raise ValueError("must be a dict")
        length = None
        for k, v_ in v.items():
            if not isinstance(v_, list):
                raise ValueError(f"value for key {k} is not a list")
            elif length is None:
                length = len(v_)
            elif len(v_) != length:
                raise ValueError(
                    f"value for key {k} does not have same length "
                    f"({len(v_)} vs {length})"
                )
        return v
