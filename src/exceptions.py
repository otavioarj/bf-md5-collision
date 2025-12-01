"""Custom exceptions for the application."""


class BrainfuckError(Exception):
    """Base exception for Brainfuck-related errors."""
    pass


class BrainfuckSyntaxError(BrainfuckError):
    """Raised when Brainfuck code has syntax errors."""
    pass


class BrainfuckTimeoutError(BrainfuckError):
    """Raised when Brainfuck execution times out."""
    pass


class BrainfuckMemoryError(BrainfuckError):
    """Raised when memory bounds are exceeded."""
    pass


class FileValidationError(Exception):
    """Raised when file validation fails."""
    pass