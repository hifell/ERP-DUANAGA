"""
QC Inference Engine - Knowledge-Based Reasoning for Cosmetic Production.

Forward chaining against a specification:

    (pH within spec) AND (viscosity within spec)  ->  Approved
    exactly one outside spec                        ->  Rework
    both outside spec                               ->  Rejected

The specification is supplied per request when the caller knows the product
specification. The built-in defaults are placeholders and are not validated
for any specific product.
"""

import hmac
import logging
import os
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field, model_validator

logging.basicConfig(
    level=os.environ.get("QC_LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
_logger = logging.getLogger("qc_engine")

app = FastAPI(
    title="QC Engine",
    version="1.1.0",
    description="Cosmetic QC inference engine with per-product specification",
)

# ─── Defaults ────────────────────────────────────────────────────────────────
# Placeholder defaults. Override per product via the `spec` field of the request.
DEFAULT_PH_MIN, DEFAULT_PH_MAX = 5.5, 6.5
DEFAULT_VISC_MIN, DEFAULT_VISC_MAX = 1.05, 1.10

API_KEY_ENV = "QC_API_KEY"


# ─── Schemas ──────────────────────────────────────────────────────────────────
class QCSpec(BaseModel):
    """Product-specific acceptance limits."""

    ph_min: float = Field(DEFAULT_PH_MIN, ge=0.0, le=14.0)
    ph_max: float = Field(DEFAULT_PH_MAX, ge=0.0, le=14.0)
    visc_min: float = Field(DEFAULT_VISC_MIN, ge=0.0)
    visc_max: float = Field(DEFAULT_VISC_MAX, ge=0.0)

    @model_validator(mode="after")
    def _check_bounds(self):
        if self.ph_min >= self.ph_max:
            raise ValueError("ph_min must be lower than ph_max")
        if self.visc_min >= self.visc_max:
            raise ValueError("visc_min must be lower than visc_max")
        return self


class QCPayload(BaseModel):
    batch_id: str = Field(..., min_length=1, max_length=200)
    ph_level: float = Field(..., ge=0.0, le=14.0, description="pH level (0-14)")
    viscosity: float = Field(..., ge=0.0, description="Viscosity (Pas)")
    spec: QCSpec | None = Field(
        None, description="Product specification. Omit to use engine defaults."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "batch_id": "BATCH-2024-001",
                    "ph_level": 6.0,
                    "viscosity": 1.075,
                    "spec": {
                        "ph_min": 5.5,
                        "ph_max": 6.5,
                        "visc_min": 1.05,
                        "visc_max": 1.10,
                    },
                }
            ]
        }
    }


class QCResponse(BaseModel):
    batch_id: str
    status: Literal["Approved", "Rework", "Rejected"]
    recommendation: str
    ph_in_range: bool
    viscosity_in_range: bool
    spec_used: QCSpec
    spec_source: Literal["request", "engine_default"]


# ─── Auth ────────────────────────────────────────────────────────────────────
def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Fail closed when an API key is configured but missing or wrong."""
    configured = os.environ.get(API_KEY_ENV, "").strip()
    if not configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="QC engine API key is not configured on the server.",
        )
    provided = (x_api_key or "").strip()
    if not hmac.compare_digest(provided.encode(), configured.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Api-Key header.",
        )


# ─── Inference Engine ─────────────────────────────────────────────────────────
def infer_status(
    ph: float, visc: float, spec: QCSpec
) -> tuple[str, str, bool, bool]:
    """Forward chaining inference against the given specification."""
    ph_ok = spec.ph_min <= ph <= spec.ph_max
    visc_ok = spec.visc_min <= visc <= spec.visc_max

    if ph_ok and visc_ok:
        return (
            "Approved",
            "Batch meets all chemical specifications. Proceed to packaging.",
            True,
            True,
        )

    if not ph_ok and not visc_ok:
        return (
            "Rejected",
            "Both pH and viscosity out of range. Full reformulation required.",
            False,
            False,
        )

    if not ph_ok:
        return (
            "Rework",
            f"pH {ph:.2f} outside [{spec.ph_min}-{spec.ph_max}]. Adjust buffer system.",
            False,
            True,
        )

    return (
        "Rework",
        f"Viscosity {visc:.3f} outside "
        f"[{spec.visc_min}-{spec.visc_max}]. Adjust thickener.",
        True,
        False,
    )


# ─── Endpoints ────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "qc-engine",
        "version": app.version,
        "auth_configured": bool(os.environ.get(API_KEY_ENV, "").strip()),
    }


@app.post("/api/qc-check", response_model=QCResponse)
def qc_check(
    payload: QCPayload,
    _: None = Depends(verify_api_key),
):
    """Evaluate a batch against a QC specification."""
    spec = payload.spec or QCSpec()
    spec_source = "request" if payload.spec else "engine_default"

    status_value, recommendation, ph_ok, visc_ok = infer_status(
        payload.ph_level, payload.viscosity, spec
    )

    _logger.info(
        "qc_check batch=%s ph=%.3f visc=%.3f spec=%s status=%s",
        payload.batch_id,
        payload.ph_level,
        payload.viscosity,
        spec.model_dump(),
        status_value,
    )

    return QCResponse(
        batch_id=payload.batch_id,
        status=status_value,
        recommendation=recommendation,
        ph_in_range=ph_ok,
        viscosity_in_range=visc_ok,
        spec_used=spec,
        spec_source=spec_source,
    )
