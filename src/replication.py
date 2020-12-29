from pydantic import BaseModel

class Replication(BaseModel):
    steps: list = []