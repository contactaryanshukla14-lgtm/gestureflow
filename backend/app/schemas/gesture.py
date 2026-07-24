from pydantic import BaseModel

class InferenceRequest(BaseModel):
    sample_label: str | None = None
    image: str | None = None

class InferenceResponse(BaseModel):
    label: str
    confidence: float
    action: str
