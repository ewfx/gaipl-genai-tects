import json
import os
import logging
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import List, Dict
from api_models import OperationResponse, AgentResponse,OperationRequest,Investigation, OperationStatusResponse
from exceptions import (
    BusinessException,
    NotFoundException,
    ConflictException,
    ServiceException
)
class OperationsService:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.ops_docs_dir = base_dir / "operations" / "docs"
        self.agents_file = base_dir / "agents" / "agents.json"
        self.logger = logging.getLogger('operations_service')
        self._setup_service_logger()

    def _setup_service_logger(self):
        """Configure service-specific logging"""
        logs_dir = self.base_dir / "operations" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(logs_dir / 'operations_service.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _log_operation(self, action: str, metadata: dict):
        """Helper method for consistent operation logging"""
        log_entry = {
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            **metadata
        }
        self.logger.info(json.dumps(log_entry))

    def _ensure_dir_exists(self, path: Path):
        """Ensure directory exists with logging"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            self._log_operation(
                "directory_creation",
                {"path": str(path), "status": "success"}
            )
        except Exception as e:
            self.logger.error(
                f"Failed to create directory {path}: {str(e)}",
                exc_info=True
            )
            raise ServiceException(
                f"Directory creation failed: {str(e)}",
                "directory_creation_failed"
            )

    def create_operation(self, request) -> OperationResponse:
        """Create a new operation file"""
        try:
            filename = f"{secure_filename(request.name)}.txt"
            filepath = self.ops_docs_dir / filename
            
            if filepath.exists():
                raise ConflictException(
                    f"Operation '{request.name}' already exists",
                    "operation_exists"
                )
            
            self._ensure_dir_exists(self.ops_docs_dir)
            
            with open(filepath, 'w') as f:
                f.write(request.operation_text)
            
            operation = [OperationResponse(
                name=request.name
            )]
            
            self._log_operation("create_operation", {
                "status": "success",
                "name": request.name,
            })
            
            return operation
            
        except BusinessException:
            raise
        except Exception as e:
            raise ServiceException(
                f"Error creating operation: {str(e)}",
                "operation_creation_failed"
            )


    def list_operations(self) -> List[OperationResponse]:
        """List all available operations"""
        try:
            operations = []
            self._ensure_dir_exists(self.ops_docs_dir)
            
            for filename in os.listdir(self.ops_docs_dir):
                filepath = self.ops_docs_dir / filename
                if filepath.is_file() and filename.endswith('.txt'):
                    with open(filepath, 'r') as f:
                        content = f.read()

                    name = os.path.splitext(filename)[0]
                    operations.append(OperationResponse(
                        name=name,
                        content=content
                    ))
            
            self._log_operation("list_operations", {
                "status": "success",
                "count": len(operations)
            })
            
            return operations
            
        except Exception as e:
            raise ServiceException(
                f"Error listing operations: {str(e)}",
                "operation_list_failed"
            )

    def get_agents(self) -> List[AgentResponse]:
        """Get all agents from the agents file"""
        try:
            if not self.agents_file.exists():
                raise NotFoundException(
                    "Agents file not found",
                    "agents_file_not_found"
                )
            
            with open(self.agents_file, 'r') as f:
                data = json.load(f)
            
            agents = [
                AgentResponse(
                    name=agent['name'],
                    type=agent['type'],
                ) for agent in data['agents']
            ]
            
            self._log_operation("get_agents", {
                "status": "success",
                "count": len(agents)
            })
            
            return agents
            
        except BusinessException:
            raise
        except Exception as e:
            raise ServiceException(
                f"Error getting agents: {str(e)}",
                "agents_retrieval_failed"
            )
        
    def start_operation(self, request: OperationRequest) -> OperationStatusResponse:
        """Start a new operation with full logging"""
        try:
            self.logger.info(f"Starting operation: {request.name}")
            
            # Your operation logic here
            output = f"Operation {request.name} started successfully"
            
            self.logger.info(f"Operation {request.name} started", extra={
                "operation": request.name,
                "status": "running"
            })
            
            return OperationStatusResponse(
                status="running",
                output=output
            )
            
        except Exception as e:
            self.logger.error(f"Operation start failed: {str(e)}", exc_info=True, extra={
                "operation": request.name,
                "error": str(e)
            })
            raise ServiceException(
                f"Operation start failed: {str(e)}",
                "operation_start_failed"
            )

    def list_investigations(self) -> List[Investigation]:
        """List investigations with audit logging"""
        try:
            self.logger.info("Listing investigations")
            
            # Replace with actual investigation listing logic
            investigations = [
                Investigation(
                    id="inv-123",
                    name="Security Audit",
                    status="completed",
                    created_at="2023-01-15T10:30:00Z"
                )
            ]
            
            self.logger.info(f"Found {len(investigations)} investigations")
            return investigations
            
        except Exception as e:
            self.logger.error("Failed to list investigations", exc_info=True)
            raise ServiceException(
                "Failed to list investigations",
                "investigation_list_failed"
            )

    def trigger_investigation(self, request: OperationRequest) -> OperationStatusResponse:
        """Trigger investigation with detailed logging"""
        try:
            self.logger.info(f"Triggering investigation: {request.name}")
            
            # Your investigation triggering logic here
            investigation_id = "123"
            
            return OperationStatusResponse(
                status="started",
                output=f"Investigation {investigation_id} started for {request.name}"
            )
            
        except Exception as e:
            self.logger.error(f"Investigation trigger failed: {str(e)}", exc_info=True, extra={
                "operation": request.name,
                "error": str(e)
            })
            raise ServiceException(
                f"Investigation trigger failed: {str(e)}",
                "investigation_trigger_failed"
            )