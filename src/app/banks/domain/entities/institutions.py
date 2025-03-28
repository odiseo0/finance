from typing import Any

from src.app.banks.domain.repository.models import InstitutionType
from src.core.schema import BaseModel


class Institution(BaseModel):
    name: str | None = None
    institution_type: InstitutionType | None = None
    description: str | None = None
    website: str | None = None
    phone: str | None = None
    logo_url: str | None = None
    country: str | None = None
    has_api_integration: bool | None = None
    api_details: dict[str, Any] | None = None
    notes: str | None = None


class InstitutionCreate(Institution):
    name: str
    institution_type: InstitutionType


class InstitutionUpdate(BaseModel):
    name: str | None = None
    institution_type: InstitutionType | None = None
    description: str | None = None
    website: str | None = None
    phone: str | None = None
    logo_url: str | None = None
    country: str | None = None
    has_api_integration: bool | None = None
    api_details: dict[str, Any] | None = None
    notes: str | None = None


class InstitutionResponse(Institution):
    id: int
