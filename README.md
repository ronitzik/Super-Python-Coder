# Super Python Coder

Super Python Coder is a Python-based application designed to assist developers in generating, optimizing, and validating Python code. This tool utilizes the OpenAI API to generate Python programs based on prompts, check linting issues, run unit tests, and optimize code for performance.

## Features
- Code Generation: Generate Python code for tasks based on natural language descriptions.
- Unit Testing: Automatically validate generated code with Python's unittest framework.
- Linting: Ensure code quality by checking for lint issues with pylint and fixing them automatically.
- Performance Optimization: Optimize Python code for better runtime performance using AI assistance.
- Execution Timing: Measure and display the execution time of generated code.
- Interactive Interface: Engage in interactive conversations to provide coding tasks and refine results.
- Error Handling: Identify and handle syntax errors, linting issues, and runtime errors.

## Installation
1. Clone this repository with the following commands:
   - git clone https://github.com/yourusername/Super-Python-Coder.git
   - cd Super-Python-Coder

2. Install required dependencies:
   - pip install -r requirements.txt

3. Set up environment variables:
   - Create a .env file in the project directory.
   - Add your OpenAI API key to the file

4. (Optional) Install pylint for lint checking:
   - pip install pylint

## Usage
Run the main program:
python superpythoncoder.py

Follow the prompts to either generate code for a custom task or allow the program to choose a random task for you.

### Example Workflow
1. Code Generation:
   - Enter a task or press Enter for a random program suggestion.
   - The generated code is saved in the src/ directory.

2. Unit Testing:
   - The tool validates the code by running unit tests.

3. Lint Checking:
   - Automatically checks and resolves lint issues.

4. Execution Timing:
   - Measures the execution time of the code.

5. Optimization:
   - Optimizes code for better performance, saving the improved version in the src/ directory.

## Known Issues
- Lint fixing and performance optimization rely on OpenAI responses and may require multiple attempts for best results.
- The execution of generated code depends on its validity and the task's complexity.
