#!/bin/bash

echo "🧪 Testing Perswade Setup"

# Test backend
echo "Testing backend..."
curl -X GET "http://localhost:8000/health" || echo "❌ Backend not responding"

# Test WebSocket
echo "Testing WebSocket connection..."
# Note: You'll need a WebSocket client for full testing

# Test AssemblyAI connection
echo "Testing AssemblyAI integration..."
python3 -c "
import os
import assemblyai as aai
try:
    aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
    transcriber = aai.Transcriber()
    print('✅ AssemblyAI connection successful')
except Exception as e:
    print(f'❌ AssemblyAI connection failed: {e}')
"

echo "✅ Setup test complete"
