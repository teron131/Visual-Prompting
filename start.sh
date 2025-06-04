#!/bin/bash

# Start the Visual Prompting backend server
echo "Starting Visual Prompting API server..."

# Check if python is available
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python to continue."
    exit 1
fi

# Check if the package is installed in development mode
if ! python -c "import visual_prompting" 2>/dev/null; then
    echo "Installing visual_prompting package in development mode..."
    pip install -e .
fi

# Check if required dependencies are installed
python -c "
try:
    import fastapi, uvicorn, pydantic, dotenv
    print('✓ All required Python dependencies are available')
except ImportError as e:
    print(f'✗ Missing dependency: {e}')
    print('Please run: pip install -r requirements.txt')
    exit(1)
"

# Start the server
echo "Starting FastAPI server on http://localhost:8001"
python -c "from visual_prompting.app import main; main()" 