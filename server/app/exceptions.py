class BaseAPIException(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserCreationError(BaseAPIException):
    """Raised when there's an error creating a user"""
    def __init__(self, message="Error creating user"):
        super().__init__(message, status_code=400)

class AuthenticationError(BaseAPIException):
    """Raised when there's an authentication error"""
    def __init__(self, message="Authentication failed"):
        super().__init__(message, status_code=401)

class PermissionDeniedError(BaseAPIException):
    """Raised when a user doesn't have permission to perform an action"""
    def __init__(self, message="Permission denied"):
        super().__init__(message, status_code=403)

class ResourceNotFoundError(BaseAPIException):
    """Raised when a requested resource is not found"""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class QueryProcessingError(BaseAPIException):
    """Raised when there's an error processing a query"""
    def __init__(self, message="Error processing query"):
        super().__init__(message, status_code=400)

class DatabaseError(BaseAPIException):
    """Raised when there's a database-related error"""
    def __init__(self, message="Database error occurred"):
        super().__init__(message, status_code=500)