from pydantic import BaseModel, Field

class PoliceReportSchema(BaseModel):
    document_type: str = Field(description="E.g., Invoice, Receipt, Statement")
    vehicle_data: dict = Field(description="Sección 8.2 VEHÍCULO")
    victim_list: list[dict] = Field(description="Extracted table rows / items purchased")
