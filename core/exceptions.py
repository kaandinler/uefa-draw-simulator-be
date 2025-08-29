# Custom exceptions
from typing import Any, Optional, Dict

class DomainException(Exception):
    """Base exception for domain errors"""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationException(DomainException):
    """Exception for validation errors"""
    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.errors = errors or {}

class BusinessRuleException(DomainException):
    """Exception for business rule violations"""
    def __init__(self, message: str):
        super().__init__(message, "BUSINESS_RULE_VIOLATION")

class ResourceNotFoundException(DomainException):
    """Exception for resource not found"""
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier {identifier} not found"
        super().__init__(message, "RESOURCE_NOT_FOUND")
        self.resource = resource
        self.identifier = identifier

class ConflictException(DomainException):
    """Exception for conflict errors"""
    def __init__(self, message: str):
        super().__init__(message, "CONFLICT")

class ExternalServiceException(Exception):
    """Exception for external service errors"""
    def __init__(self, service: str, message: str):
        self.service = service
        self.message = f"External service {service} error: {message}"
        super().__init__(self.message)