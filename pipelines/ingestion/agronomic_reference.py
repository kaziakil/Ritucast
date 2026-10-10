"""
BRRI / BARI Modern Crop Phenology and Kc Tables Loader (DATA-AGR-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ritucast.ingestion.agronomy")

class AgronomicReferenceLoader:
    """Loads and indexes official BRRI crop calendars, GDD requirements, and Kc coefficients."""

    def __init__(self, fixture_path: Optional[str] = None):
        self.fixture_path = fixture_path or "data/sample/brri_phenology_boro.json"
        self._data: Dict[str, Any] = {}
        self._varieties_by_name: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        """Loads and indexes agronomic tables."""
        if not os.path.exists(self.fixture_path):
            raise FileNotFoundError(f"Agronomic reference fixture not found at {self.fixture_path}")

        with open(self.fixture_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

        varieties = self._data.get("varieties", [])
        for v in varieties:
            name = v.get("variety_name")
            if name:
                self._varieties_by_name[name] = v

        logger.info(f"Loaded {len(self._varieties_by_name)} crop varieties from {self.fixture_path}")

    def get_supported_varieties(self) -> List[str]:
        """Returns list of indexed variety names."""
        return list(self._varieties_by_name.keys())

    def get_variety_info(self, variety_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves phenology duration and stage parameters for a variety."""
        return self._varieties_by_name.get(variety_name)

    def get_kc_for_stage(self, variety_name: str, day_after_transplant: int) -> float:
        """Determines stage-specific crop coefficient (Kc) based on plant age."""
        var_info = self.get_variety_info(variety_name)
        if not var_info:
            return 1.05  # Default FAO initial Kc

        stages = var_info.get("stages", [])
        for stage in stages:
            if stage["start_day"] <= day_after_transplant <= stage["end_day"]:
                return float(stage["kc"])

        # Fallback to end stage Kc if past duration
        if stages:
            return float(stages[-1]["kc"])
        return 1.05
