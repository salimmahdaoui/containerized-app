from pydantic import BaseModel, ConfigDict, field_validator


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator("title", "description")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value


class TaskResponse(BaseModel):
    # Elle permet à Pydantic de lire directement les attributs d'un objet SQLAlchemy pour construire une réponse JSON. 
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
