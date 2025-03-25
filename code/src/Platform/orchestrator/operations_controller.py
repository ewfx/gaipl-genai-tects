from flask import request
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from api_models import BaseResponse,OperationRequest
from operations_service import OperationsService
from exceptions import BusinessException, ValidationException
from dataclasses import asdict

class OperationsController:
    def __init__(self, service: OperationsService):
        self.service = service
        self.logger = logging.getLogger('operations_controller')
        self._setup_controller_logger()

    def _setup_controller_logger(self):
        """Configure controller-specific logging"""
        logs_dir = self.service.base_dir / "operations" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(logs_dir / 'operations_controller.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _log_request(self, endpoint: str, method: str, status: str, metadata: dict = None):
        """Log API requests"""
        log_entry = {
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            **(metadata or {})
        }
        self.logger.info(json.dumps(log_entry))

    def create_operation(self):
        """Handle operation creation requests"""
        try:
            data = request.get_json()
            self._log_request(
                '/api/operations/create',
                'POST',
                'started'
            )

            if not data or 'name' not in data or 'operationText' not in data:
                raise ValidationException(
                    "Missing name or operationText in request",
                    "invalid_request"
                )
            
            req = OperationRequest(
                name=data['name'],
                operation_text=data['operationText']
            )
            
            operation = self.service.create_operation(req)

            response = BaseResponse(
                success=True,
                data=[op.__dict__ for op in operation]
            ).to_flask_response(201)
            
            self._log_request(
                '/api/operations/create',
                'POST',
                'completed',
                {
                    "status_code": 201,
                    "operation_name": req.name
                }
            )
            
            return response            
                    
        except BusinessException as e:
            self._log_request(
                '/api/operations/create',
                'POST',
                'failed',
                {
                    "status_code": e.status_code,
                    "error_code": e.error_code,
                    "error": e.message
                }
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code=e.error_code,
                error_message=e.message
            ).to_flask_response(e.status_code)
        except Exception as e:
            self.logger.error(
                f"Unexpected error in create_operation: {str(e)}",
                exc_info=True
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code="internal_error",
                error_message="Internal server error"
            ).to_flask_response(500)


    def list_operations(self):
        """Handle operations listing requests"""
        try:
            self._log_request(
                '/api/operations',
                'GET',
                'started'
            )
            
            operations = self.service.list_operations()
            response = BaseResponse(
                success=True,
                data=[op.__dict__ for op in operations]
            ).to_flask_response(201)
            
            self._log_request(
                '/api/operations',
                'GET',
                'completed',
                {
                    "status_code": 200,
                    "count": len(operations)
                }
            )
            
            return response
            
        except BusinessException as e:
            self._log_request(
                '/api/operations',
                'GET',
                'failed',
                {
                    "status_code": e.status_code,
                    "error_code": e.error_code,
                    "error": e.message
                }
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code=e.error_code,
                error_message=e.message
            ).to_flask_response(e.status_code)
        except Exception as e:
            self.logger.error(
                f"Unexpected error in list_operations: {str(e)}",
                exc_info=True
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code="internal_error",
                error_message="Internal server error"
            ).to_flask_response(500)

    def get_agents(self):
        """Handle agents retrieval requests"""
        try:
            self._log_request(
                '/api/agents',
                'GET',
                'started'
            )
            
            agents = self.service.get_agents()
            response = BaseResponse(
                success=True,
                data=[agent.__dict__ for agent in agents]
            ).to_flask_response(201)
            
            self._log_request(
                '/api/agents',
                'GET',
                'completed',
                {
                    "status_code": 200,
                    "count": len(agents)
                }
            )
            
            return response
            
        except BusinessException as e:
            self._log_request(
                '/api/agents',
                'GET',
                'failed',
                {
                    "status_code": e.status_code,
                    "error_code": e.error_code,
                    "error": e.message
                }
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code=e.error_code,
                error_message=e.message
            ).to_flask_response(e.status_code)
        except Exception as e:
            self.logger.error(
                f"Unexpected error in get_agents: {str(e)}",
                exc_info=True
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code="internal_error",
                error_message="Internal server error"
            ).to_flask_response(500)
        

    def start_operation(self, operation_name: str):
        """API endpoint to start an operation"""
        try:
            self._log_request('/api/operations/start', 'POST', 'started')
            
            if not operation_name:
                raise ValidationException("Missing operation name", "invalid_request")
                
            result = self.service.start_operation(
                OperationRequest(name=operation_name)
            )
            
            self._log_request('/api/operations/start', 'POST', 'completed', {
                "status_code": 202,
                "operation":operation_name
            })
            
            return BaseResponse(
                success=True,
                data=asdict(result)
            ).to_flask_response(202)
            
        except BusinessException as e:
            self._log_request('/api/operations/start', 'POST', 'failed', {
                "status_code": e.status_code,
                "error": e.message
            })
            return BaseResponse(
                success=False,
                error=True,
                error_code=e.error_code,
                error_message=e.message
            ).to_flask_response(e.status_code)
        except Exception as e:
            self.logger.error(
                f"Unexpected error in start operation: {str(e)}",
                exc_info=True
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code="internal_error",
                error_message="Internal server error"
            ).to_flask_response(500)

    def list_investigations(self):
        """API endpoint to list investigations"""
        try:
            self._log_request('/api/investigations', 'GET', 'started')
            
            investigations = self.service.list_investigations()
            
            self._log_request('/api/investigations', 'GET', 'completed', {
                "status_code": 200,
                "count": len(investigations)
            })
            
            return BaseResponse(
                success=True,
                data=[asdict(inv) for inv in investigations]
            ).to_flask_response()
            
        except BusinessException as e:
            self._log_request('/api/investigations', 'GET', 'failed', {
                "status_code": e.status_code,
                "error": e.message
            })
            return BaseResponse(
                success=False,
                error=True,
                error_code=e.error_code,
                error_message=e.message
            ).to_flask_response(e.status_code)
        except Exception as e:
            self.logger.error(
                f"Unexpected error in list investigations: {str(e)}",
                exc_info=True
            )
            return BaseResponse(
                success=False,
                error=True,
                error_code="internal_error",
                error_message="Internal server error"
            ).to_flask_response(500)

    def trigger_investigation(self,investigation_name: str):
        """API endpoint to trigger investigation"""
        try:
            self._log_request('/api/investigations/trigger', 'POST', 'started')
            
            
            if not investigation_name:
                raise ValidationException("Missing investigation name", "invalid_request")
                
            result = self.service.trigger_investigation(
                OperationRequest(name=investigation_name)
            )
            
            self._log_request('/api/investigations/trigger', 'POST', 'completed', {
                "status_code": 202,
                "investigation": investigation_name
            })
            
            return BaseResponse(
                success=True,
                data=asdict(result)
            ).to_flask_response(202)
            
        except BusinessException as e:
            self._log_request('/api/investigations/trigger', 'POST', 'failed', {
                "status_code": e.status_code,
                "error": e.message
            })
            return BaseResponse(
                    success=False,
                    error=True,
                    error_code=e.error_code,
                    error_message=e.message
                ).to_flask_response(e.status_code)
        except Exception as e:
                self.logger.error(
                    f"Unexpected error in list investigations: {str(e)}",
                    exc_info=True
                )
                return BaseResponse(
                    success=False,
                    error=True,
                    error_code="internal_error",
                    error_message="Internal server error"
                ).to_flask_response(500)


