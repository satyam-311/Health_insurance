from pydantic import BaseModel


class InsuranceRequest(BaseModel):
    age: int
    gender: str
    bmi: float
    children: int
    discount_eligibility: str
    region: str
