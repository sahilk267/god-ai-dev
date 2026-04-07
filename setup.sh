#!/bin/bash

echo "🚀 Setting up God-Level AI Developer System..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p workspace logs deployments

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️ Please edit .env file and add your API keys!"
fi

# Run the system
echo "✅ Setup complete! Run: uvicorn backend.api.routes:app --reload --port 8000"