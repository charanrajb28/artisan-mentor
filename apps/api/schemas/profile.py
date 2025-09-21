from pydantic import BaseModel

class ArtisanProfile(BaseModel):
    name: str
    craft: str
    lineage: str
    voice_note_url: str
