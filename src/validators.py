"""Input validation utilities."""
import hashlib
from typing import Tuple
from werkzeug.datastructures import FileStorage

from exceptions import FileValidationError


def validate_file_upload(file: FileStorage, max_size: int = 1024 * 1024) -> bytes:
    """
    Validate uploaded file.
    
    Args:
        file: Uploaded file object
        max_size: Maximum file size in bytes
        
    Returns:
        File content as bytes
        
    Raises:
        FileValidationError: If validation fails
    """
    if not file or not file.filename:
        raise FileValidationError("No file provided")
    
    # Check file extension
    allowed_extensions = {'.bf', '.b', '.txt'}
    if not any(file.filename.endswith(ext) for ext in allowed_extensions):
        raise FileValidationError(
            f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Read and check size
    content = file.read()
    if len(content) == 0:
        raise FileValidationError("File is empty")
    
    if len(content) > max_size:
        raise FileValidationError(
            f"File too large: {len(content)} bytes (max: {max_size} bytes)"
        )
    
    # Check for valid Brainfuck characters
    valid_bf_chars = set(b'><+-.,[]')
    bf_chars = set(content) & valid_bf_chars
    
    if not bf_chars:
        raise FileValidationError("File contains no valid Brainfuck commands")
    
    return content


def validate_outputs(output1: str, output2: str) -> Tuple[bool, str]:
    """
    Validate that outputs match expected strings.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    expected1 = "Rock N Roll"
    expected2 = "Hack N Roll"
    
    if output1 != expected1:
        return False, f"File 1 output '{output1}' does not match '{expected1}'"
    
    if output2 != expected2:
        return False, f"File 2 output '{output2}' does not match '{expected2}'"
    
    return True, ""


def validate_collision(code1: bytes, code2: bytes) -> Tuple[bool, str, str]:
    """
    Validate MD5 collision.
    
    Returns:
        Tuple of (is_collision, hash1, hash2)
    """
    hash1 = hashlib.md5(code1).hexdigest()
    hash2 = hashlib.md5(code2).hexdigest()
    
    return hash1 == hash2, hash1, hash2