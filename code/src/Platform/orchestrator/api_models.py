from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Union, Tuple
from dataclasses import asdict
from flask import jsonify
from werkzeug.wrappers import Response

@dataclass
class BaseResponse:
    success: bool
    data: Optional[Dict] = None
    error: bool = False
    error_code: str = "none"
    error_message: str = "none"
    timestamp: str = datetime.utcnow().isoformat()

    def to_flask_response(self, status_code: int = 200): 
        """Converts the dataclass to a proper Flask response"""
        return jsonify(asdict(self)), status_code
    
@dataclass
class OperationRequest:
    name: str
    operation_text: Optional[str] = None

@dataclass
class OperationResponse:
    name: str
    content: Optional[str] = None

@dataclass
class AgentResponse:
    name: str
    type: str

@dataclass
class Investigation:
    id: str
    name: str
    status: str
    created_at: str


@dataclass
class TriggerInvestigationResponse:
    investigation_id: str
    status: str
    message: str

@dataclass
class OperationStatusResponse:
    status:str
    output:str