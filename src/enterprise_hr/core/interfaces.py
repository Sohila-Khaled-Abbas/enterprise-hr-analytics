"""
Core Abstract Interfaces & Contracts.
Defines foundational abstractions adhering to SOLID principles:
Single Responsibility, Open/Closed, and Dependency Inversion.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pandas as pd


class BaseExtractor(ABC):
    """Abstract contract for data extractors (APIs, files, external databases)."""
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extracts source data into a pandas DataFrame."""
        pass


class BaseTransformer(ABC):
    """Abstract contract for data transformations and business rule applications."""
    
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transforms input DataFrame according to domain rules."""
        pass


class BaseLoader(ABC):
    """Abstract contract for database and lake loaders."""
    
    @abstractmethod
    def load(self, data: pd.DataFrame, target_table: str, truncate: bool = False) -> int:
        """Loads data into the destination storage or table, returning rows loaded."""
        pass


class BasePipelineStep(ABC):
    """Abstract unit of work in a multi-step data pipeline."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """Executes the pipeline step, returning execution telemetry."""
        pass

    def validate(self) -> bool:
        """Optional post-execution verification hook."""
        return True

    def rollback(self) -> None:
        """Optional recovery/rollback hook on failure."""
        pass
