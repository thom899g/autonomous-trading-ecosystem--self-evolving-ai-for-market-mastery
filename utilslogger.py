"""
Robust logging system with structured logging and Firebase integration.
Architectural Choice: Structlog provides structured, machine-readable logs
that can be easily ingested by monitoring systems and Firebase for real-time
performance tracking.
"""

import sys
import logging
from typing import Any, Dict, Optional
from datetime import datetime
import structlog
from pythonjsonlogger import jsonlogger

# Custom log processors
def add_timestamp(_: Any, __: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add ISO 8601 timestamp to all log entries"""
    event_dict["timestamp"] = datetime.utcnow().isoformat() +