"""Tests for Brainfuck interpreter."""
import pytest
from src.main import interpret_brainfuck
from src.exceptions import BrainfuckSyntaxError, BrainfuckTimeoutError


class TestBrainfuckInterpreter:
    """Test cases for Brainfuck interpreter."""
    
    def test_simple_output(self):
        """Test basic character output."""
        code = b"+++++ +++[>+++++ +++<-]>."  # Outputs '@' (64)
        result = interpret_brainfuck(code)
        assert result == "@"
    
    def test_hello_world(self):
        """Test Hello World program."""
        code = (
            b"++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]"
            b">>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
        )
        result = interpret_brainfuck(code)
        assert "Hello World" in result
    
    def test_unmatched_open_bracket(self):
        """Test that unmatched [ raises error."""
        code = b"++[++"
        with pytest.raises(BrainfuckSyntaxError, match="Unmatched '\\['"):
            interpret_brainfuck(code)
    
    def test_unmatched_close_bracket(self):
        """Test that unmatched ] raises error."""
        code = b"++]"
        with pytest.raises(BrainfuckSyntaxError, match="Unmatched '\\]'"):
            interpret_brainfuck(code)
    
    def test_memory_increment_wrap(self):
        """Test that memory wraps at 256."""
        code = b"+" * 256 + b"."  # Should wrap to 0
        result = interpret_brainfuck(code)
        assert ord(result) == 0
    
    def test_memory_decrement_wrap(self):
        """Test that memory wraps at 0."""
        code = b"-."  # Should wrap to 255
        result = interpret_brainfuck(code)
        assert ord(result) == 255
    
    
    def test_comments_ignored(self):
        """Test that non-BF characters are ignored."""
        code = b"This is a comment +++++ +++++ . and more comments"
        result = interpret_brainfuck(code)
        assert result == chr(10)  # '\n'


class TestValidation:
    """Test input validation."""
    
    def test_rock_n_roll_output(self):
        """Test validation of 'Rock N Roll' output."""
        # This would need the actual collision bytes
        pass
    
    def test_md5_collision_detection(self):
        """Test MD5 collision detection."""
        # This would need actual collision files
        pass