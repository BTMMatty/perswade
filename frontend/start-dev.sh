#!/bin/bash

echo "🚀 Starting Perswade Development Environment"

# Check if AssemblyAI key is set
if [ -z "$ASSEMBLYAI_API_KEY" ]; then
    echo "❌ Error: ASSEMBLYAI_API_KEY not set in .env file"
    echo "Please add your AssemblyAI API key to .env file"
    exit 1
fi

echo "📦 Installing dependencies..."

# Install backend dependencies
cd backend && pip install -r requirements.txt &
BACKEND_PID=$!

# Install frontend dependencies
cd frontend && npm install &
FRONTEND_PID=$!

# Wait for installations
wait $BACKEND_PID
wait $FRONTEND_PID

echo "🔧 Starting services..."

# Start backend
cd ../backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_SERVER_PID=$!

# Start frontend
cd ../frontend && npm run dev &
FRONTEND_SERVER_PID=$!

echo "✅ Perswade is running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_SERVER_PID $FRONTEND_SERVER_PID; exit" INT
wait
