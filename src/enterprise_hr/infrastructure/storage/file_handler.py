"""
Enterprise Safe File Handler Module.
Encapsulates thread-safe, atomic file reading and writing across CSV, JSON, Excel, and Text files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd

from enterprise_hr.core.config import get_config
from enterprise_hr.core.exceptions import StorageError
from enterprise_hr.core.logging import get_logger

logger = get_logger("FileHandler")


class FileHandler:
    """Provides resilient read/write operations for the data lake zones."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or get_config().paths.project_root

    def read_csv(self, filepath: Union[str, Path], **kwargs: Any) -> pd.DataFrame:
        """Reads CSV with robust UTF-8-sig / UTF-8 fallback."""
        path = Path(filepath)
        if not path.exists():
            raise StorageError(f"CSV file not found: {path}")

        try:
            return pd.read_csv(path, encoding="utf-8-sig", **kwargs)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="utf-8", **kwargs)
        except Exception as e:
            raise StorageError(f"Failed to read CSV '{path}': {e}") from e

    def write_csv(self, df: pd.DataFrame, filepath: Union[str, Path], index: bool = False, **kwargs: Any) -> Path:
        """Writes DataFrame to CSV atomically."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".tmp")

        try:
            df.to_csv(temp_path, index=index, encoding="utf-8-sig", **kwargs)
            temp_path.replace(path)
            logger.debug("Safely written CSV to %s (%d rows)", path.name, len(df))
            return path
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise StorageError(f"Failed to write CSV '{path}': {e}") from e

    def read_json(self, filepath: Union[str, Path]) -> Union[Dict[str, Any], List[Any]]:
        """Reads JSON file safely."""
        path = Path(filepath)
        if not path.exists():
            raise StorageError(f"JSON file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise StorageError(f"Failed to read JSON '{path}': {e}") from e

    def write_json(self, data: Union[Dict[str, Any], List[Any]], filepath: Union[str, Path], indent: int = 2) -> Path:
        """Writes data to JSON atomically."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".tmp")

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, default=str)
            temp_path.replace(path)
            return path
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise StorageError(f"Failed to write JSON '{path}': {e}") from e

    def read_excel(self, filepath: Union[str, Path], sheet_name: Union[str, int] = 0, **kwargs: Any) -> pd.DataFrame:
        """Reads Excel file safely."""
        path = Path(filepath)
        if not path.exists():
            raise StorageError(f"Excel file not found: {path}")

        try:
            return pd.read_excel(path, sheet_name=sheet_name, **kwargs)
        except Exception as e:
            raise StorageError(f"Failed to read Excel '{path}': {e}") from e


def get_file_handler() -> FileHandler:
    """Convenience provider for FileHandler."""
    return FileHandler()
