"""
QC Inference Engine - Knowledge-Based Reasoning for Cosmetic Production
Forward Chaining: pH + Viscosity → Approval Status
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="QC Engine", version="1.0.0", description="Cosmetic QC inference engine")

# ─── Constants ────────────────────────────────────────────────────────────────
PH_MIN, PH_MAX = 5.5, 6.5
VISC_MIN, VISC_MAX = 1.05, 1.10

# ─── Schemas ──────────────────────────────────────────────────────────────────
class QCPayload(BaseModel):
    batch_id: str = Field(..., min_length=1, description="Production batch identifier")
    ph_level: float = Field(..., description="pH level (0-14)")
    viscosity: float = Field(..., description="Viscosity (Pas)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "batch_id": "BATCH-2024-001",
                    "ph_level": 6.0,
                    "viscosity": 1.075
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


# ─── Inference Engine ─────────────────────────────────────────────────────────
def infer_status(ph: float, visc: float) -> tuple[str, str, bool, bool]:
    """
    Forward chaining inference.
    Returns: (status, recommendation, ph_in_range, visc_in_range)
    """
    ph_ok = PH_MIN <= ph <= PH_MAX
    visc_ok = VISC_MIN <= visc <= VISC_MAX

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

    # One is out of range → Rework
    if not ph_ok:
        return (
            "Rework",
            f"pH {ph:.2f} outside [{PH_MIN}-{PH_MAX}]. Adjust buffer system.",
            False,
            True,
        )

    return (
        "Rework",
        f"Viscosity {visc:.3f} outside [{VISC_MIN}-{VISC_MAX}]. Adjust thickener.",
        True,
        False,
    )


# ─── Endpoints ───────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "healthy", "service": "qc-engine"}


@app.post("/api/qc-check", response_model=QCResponse)
def qc_check(payload: QCPayload):
    """
    Evaluate batch against QC rules.
    Forward chains: (pH range) ∧ (viscosity range) → status
    """
    status, recommendation, ph_ok, visc_ok = infer_status(
        payload.ph_level, payload.viscosity
    )

    return QCResponse(
        batch_id=payload.batch_id,
        status=status,
        recommendation=recommendation,
        ph_in_range=ph_ok,
        viscosity_in_range=visc_ok,
    )
