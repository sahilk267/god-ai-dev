#!/bin/bash

echo "🚀 Setting up God-Level AI Developer System..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p workspace logs deployments backend/data

# Check for Ollama models
echo "Checking Ollama models..."
if command -v ollama &> /dev/null; then
    ollama list | grep -q "llama3" || echo "⚠️ Model 'llama3' not found. Recommended: ollama pull llama3"
    ollama list | grep -q "deepseek-coder" || echo "⚠️ Model 'deepseek-coder' not found. Recommended: ollama pull deepseek-coder"
else
    echo "⚠️ Ollama not detected. Please install Ollama to use the AI features."
fi

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️ Created .env from example. Please add your API keys!"
fi

# Final instructions
echo "✅ Setup complete!"
echo "💡 To sync state from another system, use: scripts/sync_state.sh"
echo "🚀 Run: uvicorn backend.api.routes:app --reload --port 8000"