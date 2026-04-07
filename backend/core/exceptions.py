"""Custom exceptions for the system"""

class AIDeveloperException(Exception):
    """Base exception for AI Developer System"""
    pass

class APICallError(AIDeveloperException):
    """Raised when API call fails"""
    pass

class CodeGenerationError(AIDeveloperException):
    """Raised when code generation fails"""
    pass

class TestExecutionError(AIDeveloperException):
    """Raised when tests fail to execute"""
    pass

class DeploymentError(AIDeveloperException):
    """Raised when deployment fails"""
    pass

class ConfigurationError(AIDeveloperException):
    """Raised when configuration is invalid"""
    pass