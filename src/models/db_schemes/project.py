from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id") # None means optional field
    project_id: str = Field(..., min_length=1) # ellipsis means required field

    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        
        return value

    class Config:
        arbitrary_types_allowed = True

    @classmethod # This decorator allows the method to be called on the class itself (static method), not just on instances
    # Here we will use *cls* to refer to the class itself, not *self* which refer to the object instance
    def get_indexes(cls):

        return [
            {
                # key: Represents the field name in the database to which the index is applied.
                "key": [ # Take one or more key fields to create an index on
                    ("project_id", 1) # 1 for ascending order, -1 for descending order
                ],
                "name": "project_id_index_1", # don't repeat the name of the index, it should be unique
                "unique": True, # If True, the index will enforce uniqueness for the indexed field(s).
            }
        ]