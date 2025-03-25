class BusinessException(Exception):
    """Base business exception class"""
    def __init__(self, message: str, error_code: str, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)

class ValidationException(BusinessException):
    """Validation errors"""
    def __init__(self, message: str, error_code: str = "validation_error"):
        super().__init__(message, error_code, 400)

class NotFoundException(BusinessException):
    """Resource not found errors"""
    def __init__(self, message: str, error_code: str = "not_found"):
        super().__init__(message, error_code, 404)

class ConflictException(BusinessException):
    """Resource conflict errors"""
    def __init__(self, message: str, error_code: str = "conflict"):
        super().__init__(message, error_code, 409)

class ServiceException(BusinessException):
    """Service level errors"""
    def __init__(self, message: str, error_code: str = "service_error"):
        super().__init__(message, error_code, 500)