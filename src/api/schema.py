from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InsuranceRequest(BaseModel):
    age: int
    bmi: float
    children: int
    region: str
    gender: Optional[str] = None
    discount_eligibility: Optional[str] = None
    sex: Optional[str] = Field(default=None, description="Backward-compatible alias for gender")
    smoker: Optional[str] = Field(default=None, description="Backward-compatible alias for discount_eligibility")
    premium: Optional[float] = None

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="after")
    def validate_categorical_inputs(self):
        if not (self.gender or self.sex):
            raise ValueError("Either 'gender' or 'sex' must be provided.")
        if not (self.discount_eligibility or self.smoker):
            raise ValueError("Either 'discount_eligibility' or 'smoker' must be provided.")
        return self

    def to_model_input(self) -> dict:
        gender_value = self.gender or self.sex
        discount_value = self.discount_eligibility or self.smoker
        return {
            "age": self.age,
            "bmi": self.bmi,
            "children": self.children,
            "region": self.region,
            "gender": gender_value,
            "discount_eligibility": discount_value,
            "sex": self.sex or gender_value,
            "smoker": self.smoker or discount_value,
            "premium": self.premium,
        }
