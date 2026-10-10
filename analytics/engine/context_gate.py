"""Mandatory Contextual Gating Middleware (DEC-17).

Ensures that no recommendation card can ever be emitted without verified confirmation of:
1. Administrative Upazila.
2. Active Crop.
3. Active Phenological Growth Stage.
"""

from typing import List, Optional, Tuple
from analytics.contracts.advisory_schemas import ContextGatePayload


class ContextGatingError(Exception):
    """Raised when context gating invariants are violated."""
    pass


class ContextGator:
    """Validates user or system context before advisory generation."""

    # Approved initial pilot upazilas (High Barind and Haor Basin)
    VALID_PILOT_UPAZILAS = {
        "BD-50-20-30": "Godagari",
        "BD-50-20-90": "Tanore",
        "BD-60-90-86": "Sunamganj Sadar",
        "BD-60-90-89": "Tahirpur",
    }

    # Approved initial crop focus
    VALID_CROPS = {"BORO RICE", "BORO", "RICE"}

    @classmethod
    def validate_context(
        cls,
        upazila_id: Optional[str],
        crop_name: Optional[str],
        growth_stage: Optional[str],
    ) -> Tuple[bool, Optional[str], Optional[ContextGatePayload]]:
        """Validate three mandatory contextual gates (DEC-17).

        Returns:
            Tuple of (is_valid, error_message, payload).
        """
        # 1. Administrative Upazila check
        if not upazila_id or not str(upazila_id).strip():
            return False, "Gate 1 Failed: Administrative Upazila identifier is missing.", None
        clean_upazila = str(upazila_id).strip()
        if clean_upazila not in cls.VALID_PILOT_UPAZILAS:
            return False, f"Gate 1 Failed: Upazila '{clean_upazila}' is outside approved pilot testbeds.", None

        # 2. Active Crop check
        if not crop_name or not str(crop_name).strip():
            return False, "Gate 2 Failed: Active crop name is missing.", None
        clean_crop = str(crop_name).strip().upper()
        if clean_crop not in cls.VALID_CROPS:
            return False, f"Gate 2 Failed: Crop '{crop_name}' is not currently calibrated in pilot scope.", None

        # 3. Growth Stage check
        if not growth_stage or not str(growth_stage).strip():
            return False, "Gate 3 Failed: Active phenological growth stage is missing.", None
        clean_stage = str(growth_stage).strip()

        payload = ContextGatePayload(
            upazila_id=clean_upazila,
            crop_name=crop_name.strip(),
            growth_stage=clean_stage,
        )
        return True, None, payload
