import hashlib
from flask import Flask, request, render_template, flash, redirect
from contextlib import contextmanager

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from config import get_config
from rate_limit import setup_rate_limiter

config = get_config()

app = Flask(__name__)
app.config.from_object(config)
limiter = setup_rate_limiter(app)

def interpret_brainfuck(code: bytes) -> str:
    """
    Interprets and executes Brainfuck code.
    Uses instruction counter to prevent infinite loops.
    """
    memory = [0] * 30000
    pointer = 0
    output = ""
    i = 0
    instruction_count = 0
    MAX_INSTRUCTIONS = 10_000_000  # Prevent infinite loops
    
    while i < len(code):
        instruction_count += 1
        if instruction_count > MAX_INSTRUCTIONS:
            raise ValueError("Exceeded maximum instruction count - possible infinite loop")
        
        if code[i] == ord('>'):
            pointer += 1
            if pointer >= 30000:
                raise ValueError(f"Memory overflow")
        elif code[i] == ord('<'):
            pointer -= 1
            if pointer < 0:
                raise ValueError(f"Memory underflow")
        elif code[i] == ord('+'):
            memory[pointer] = (memory[pointer] + 1) % 256
        elif code[i] == ord('-'):
            memory[pointer] = (memory[pointer] - 1) % 256
        elif code[i] == ord('.'):
            output += chr(memory[pointer])
            if len(output) > 1000:
                raise ValueError("Output too long")
        elif code[i] == ord(','):
            pass
        elif code[i] == ord('['):
            if memory[pointer] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    i += 1
                    if i >= len(code):
                        raise ValueError("Unmatched '['")
                    if code[i] == ord('['):
                        open_brackets += 1
                    elif code[i] == ord(']'):
                        open_brackets -= 1
        elif code[i] == ord(']'):
            if memory[pointer] != 0:
                close_brackets = 1
                while close_brackets != 0:
                    i -= 1
                    if i < 0:
                        raise ValueError("Unmatched ']'")
                    if code[i] == ord('['):
                        close_brackets -= 1
                    elif code[i] == ord(']'):
                        close_brackets += 1
        i += 1
    
    return output

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_files():
    """
    Main route that handles file uploads and validates Brainfuck code.
    Users must submit two files that:
    - Produce different outputs ("Rock N Roll" and "Hack N Roll")
    - Have the same MD5 hash (MD5 collision)
    """
    app.logger.info(f"File upload request from {request.remote_addr}")

    try:
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Validate that both files were uploaded
        if not file1 or not file2:
            flash('Please upload both files.', 'error')
            return redirect(request.url)
        
        # Read file contents as bytes
        code1 = file1.read()
        code2 = file2.read()
        
        try:
            # Execute both Brainfuck programs
            output1 = interpret_brainfuck(code1)
            output2 = interpret_brainfuck(code2)
        except ValueError as e:
            # Handle malformed Brainfuck code
            flash(f"Error interpreting Brainfuck code: {str(e)}", "error")
            return redirect(request.url)
        
        # Validate first output
        if output1 != "Rock N Roll":
            flash(f"The value '{output1}' does not match 'Rock N Roll'", "error")

        # Validate second output
        if output2 != "Hack N Roll":
            flash(f"The value '{output2}' does not match 'Hack N Roll'", "error")

        # Check MD5 collision
        md5_1 = hashlib.md5(code1).hexdigest()
        md5_2 = hashlib.md5(code2).hexdigest()

        if md5_1 != md5_2:
            flash("The hashes do not match.", "error")
        
        # If all conditions are met, reveal the flag
        if output1 == "Rock N Roll" and output2 == "Hack N Roll" and md5_1 == md5_2:
            app.logger.info(f"Successful collision from {request.remote_addr}")
            flash(config.FLAG, "success")
    except Exception as e:
        app.logger.error(f"Error processing upload: {str(e)}", exc_info=True)
        flash("An error occurred processing your files", "error")

    return render_template('upload.html')

@app.route('/source')
def source():
    """
    Route that displays the source code with syntax highlighting.
    """
    with open(__file__) as f:
        code = f.read()
    
    # Apply syntax highlighting using Pygments
    formatter = HtmlFormatter(full=True, linenos=True, cssclass="source")
    highlighted_code = highlight(code, PythonLexer(), formatter)
    styles = "<style>" + formatter.get_style_defs() + "</style>"
    
    return styles + highlighted_code

if __name__ == '__main__':
    app.run(debug=True)