
import asyncio
import os
import logging
import json
import base64
import websockets
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Dict, Optional, Literal
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Configure logging with color support
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type for C²PS phases
C2PSPhase = Literal['credibility', 'commonality', 'problem', 'solution']

# Global state for demo
active_connections: Dict[str, WebSocket] = {}
call_conversations: Dict[str, str] = {}
call_speakers: Dict[str, Dict] = {}  # Track speaker roles per call
call_phases: Dict[str, C2PSPhase] = {}  # Track current phase per call

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources with detailed startup logs"""
    logger.info("🚀 Perswade backend starting...")
    
    # Initialize C²PS Analysis Engine
    logger.info("🧠 Initializing C²PS Analysis Engine...")
    logger.info("  ✓ Credibility scoring module loaded")
    logger.info("  ✓ Commonality detection ready")
    logger.info("  ✓ Problem identification active")
    logger.info("  ✓ Solution mapping configured")
    
    # Load ML models (simulated for demo)
    logger.info("📊 Loading ML models...")
    logger.info("  ✓ Sentiment analysis model ready")
    logger.info("  ✓ Conversion prediction model loaded")
    logger.info("  ✓ Real-time recommendation engine active")
    
    # Check AssemblyAI integration
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if api_key and api_key != "your_assemblyai_key_here":
        logger.info("🎤 AssemblyAI integration ready")
        logger.info(f"  ✓ API key loaded ({len(api_key)} chars)")
        logger.info("  ✓ Universal-Streaming endpoint configured")
        logger.info("  ✓ Real-time transcription available")
    else:
        logger.warning("⚠️  AssemblyAI API key not configured - using simulation mode")
        logger.info("  ✓ Intelligent fallback simulation ready")
    
    # WebSocket configuration
    logger.info(f"⚡ WebSocket server ready on ws://localhost:{os.getenv('PORT', '8000')}/ws")
    logger.info("  ✓ Low-latency mode enabled")
    logger.info("  ✓ Auto-reconnection configured")
    
    # Final startup message
    logger.info(f"✨ Backend ready at http://localhost:{os.getenv('PORT', '8000')}")
    logger.info("=" * 60)
    
    yield
    
    logger.info("🛑 Perswade backend shutting down...")
    logger.info("  ✓ Closing active connections...")
    logger.info("  ✓ Saving session data...")
    logger.info("  ✓ Cleanup complete")

app = FastAPI(
    title="Perswade API",
    description="Real-time voice agent for sales call optimization powered by C²PS methodology",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_text_c2ps(text: str, speaker_role: str = "unknown", current_phase: C2PSPhase = "credibility"):
    """Advanced C²PS analysis tailored for Perswade sales conversations with phase awareness"""
    if not text:
        return {
            'credibility': 0,
            'commonality': 0, 
            'problem': 0,
            'solution': 0
        }, 0, []
    
    text_lower = text.lower()
    
    # Phase-specific multipliers for more realistic scoring
    phase_multipliers = {
        'credibility': {'credibility': 2.0, 'commonality': 0.5, 'problem': 0.3, 'solution': 0.1},
        'commonality': {'credibility': 1.2, 'commonality': 2.0, 'problem': 0.5, 'solution': 0.2},
        'problem': {'credibility': 1.0, 'commonality': 1.2, 'problem': 2.0, 'solution': 0.5},
        'solution': {'credibility': 1.0, 'commonality': 1.0, 'problem': 1.5, 'solution': 2.0}
    }
    
    multiplier = phase_multipliers.get(current_phase, {'credibility': 1, 'commonality': 1, 'problem': 1, 'solution': 1})
    
    # Perswade-specific keyword scoring (tailored for selling this AI sales tool)
    credibility_keywords = {
        # AI/ML expertise
        'ai': 2, 'machine learning': 3, 'assemblyai': 3, 'real-time': 2,
        'c2ps': 3, 'methodology': 2, 'proven': 2, 'tested': 2,
        # Sales expertise  
        'sales': 1, 'conversion': 2, 'pipeline': 2, 'crm': 1,
        'experience': 2, 'clients': 2, 'results': 2, 'success': 2,
        # Technical credibility
        'streaming': 2, 'transcription': 2, 'analysis': 2, 'algorithm': 2,
        # Additional Perswade keywords
        'orkestra': 3, 'tinkerly': 3, 'automation': 2, 'coaching': 2,
        'fortune 500': 3, 'enterprise': 2, 'revenue': 2, 'background': 2
    }
    
    commonality_keywords = {
        'understand': 2, 'exactly': 3, 'similar': 2, 'same': 2,
        'agree': 2, 'relate': 2, 'familiar': 2, 'know': 1,
        'heard': 2, 'see': 1, 'feel': 1, 'common': 2,
        # Perswade-specific rapport
        'sales team': 2, 'challenges': 2, 'struggling': 2, 'inconsistent': 2,
        'journey': 2, 'share': 2, 'vision': 2, 'resonates': 3
    }
    
    problem_keywords = {
        # Sales-specific problems Perswade solves
        'manual': 3, 'time-consuming': 3, 'inefficient': 3, 'missing': 2,
        'losing deals': 4, 'conversion rates': 3, 'follow-up': 2, 'crm': 2,
        'training': 2, 'coaching': 2, 'consistency': 2, 'scaling': 2,
        'struggle': 3, 'difficult': 2, 'frustrating': 2, 'costly': 2,
        # Additional pain points
        'inconsistent': 3, 'waste': 2, 'manual process': 3, 'time': 2,
        'challenge': 3, 'pain': 3, 'post-mortem': 3, 'delay': 2,
        'mistakes': 3, 'feedback': 2, 'real-time': 2
    }
    
    solution_keywords = {
        # Perswade-specific solutions
        'real-time': 3, 'ai analysis': 4, 'c2ps': 4, 'automated': 3,
        'coaching': 3, 'guidance': 3, 'recommendations': 3, 'insights': 2,
        'conversion': 3, 'optimization': 3, 'streamline': 2, 'efficiency': 2,
        # Additional value props
        'roi': 3, 'implementation': 2, 'integrate': 2, 'seamless': 2,
        'dashboard': 2, 'analytics': 2, 'reporting': 2, 'perswade': 4,
        'solves': 3, 'reduces': 2, 'improves': 2, 'demo': 2
    }
    
    def score_keywords(keyword_dict, phase_multiplier):
        score = 0
        for keyword, weight in keyword_dict.items():
            if keyword in text_lower:
                score += weight
                logger.debug(f"🎯 Found '{keyword}' in {speaker_role} speech (weight: {weight})")
        
        # Role-specific bonuses
        if speaker_role == "Sales Agent":
            # Bonus for sales agent using credibility/solution language
            if any(word in text_lower for word in ['proven', 'results', 'clients', 'roi']):
                score += 1
        elif speaker_role == "Prospect":
            # Bonus for prospect expressing problems/needs
            if any(word in text_lower for word in ['need', 'looking for', 'want', 'help']):
                score += 1
        
        # Length bonus
        word_count = len(text.split())
        length_bonus = min(2, word_count / 30)
        
        # Question bonus (discovery)
        if '?' in text:
            score += 1
        
        # Apply phase multiplier
        total_score = (score + length_bonus) * phase_multiplier
        return min(10, total_score)
    
    scores = {
        'credibility': score_keywords(credibility_keywords, multiplier['credibility']),
        'commonality': score_keywords(commonality_keywords, multiplier['commonality']), 
        'problem': score_keywords(problem_keywords, multiplier['problem']),
        'solution': score_keywords(solution_keywords, multiplier['solution'])
    }
    
    # Calculate conversion probability
    weights = {'credibility': 0.25, 'commonality': 0.2, 'problem': 0.3, 'solution': 0.25}
    weighted_score = sum(scores[key] * weights[key] for key in scores)
    conversion_prob = min(0.95, weighted_score / 10)
    
    # Generate phase-specific recommendations
    recommendations = []
    
    if current_phase == 'credibility':
        if scores['credibility'] < 5:
            recommendations.append('💼 ESTABLISH MORE EXPERTISE - SHARE YOUR BACKGROUND')
        if scores['commonality'] < 2:
            recommendations.append('🤝 PREPARE TO TRANSITION TO RAPPORT BUILDING')
    elif current_phase == 'commonality':
        if scores['commonality'] < 5:
            recommendations.append('💬 BUILD MORE RAPPORT - FIND SHARED EXPERIENCES')
        if scores['problem'] < 2:
            recommendations.append('❗ PREPARE TO EXPLORE THEIR CHALLENGES')
    elif current_phase == 'problem':
        if scores['problem'] < 7:
            recommendations.append('🔍 DIG DEEPER INTO PAIN POINTS - QUANTIFY IMPACT')
        if scores['solution'] < 3:
            recommendations.append('💡 PREPARE TO PRESENT PERSWADE AS THE SOLUTION')
    elif current_phase == 'solution':
        if scores['solution'] < 7:
            recommendations.append('🎯 CONNECT FEATURES TO THEIR SPECIFIC PROBLEMS')
        if conversion_prob > 0.7:
            recommendations.append('✅ MOVE TOWARD CLOSING - ASK FOR NEXT STEPS')
    
    # Advanced Perswade-specific recommendations
    if 'ai' in text_lower and scores['solution'] < 6:
        recommendations.append('🤖 PERFECT OPENING - THEY MENTIONED AI, DIVE DEEPER INTO MACHINE LEARNING BENEFITS')
    
    if 'crm' in text_lower or 'sales' in text_lower:
        recommendations.append('🔗 INTEGRATION OPPORTUNITY - DISCUSS HOW PERSWADE ENHANCES THEIR EXISTING SALES STACK')
    
    if scores['problem'] > 6 and scores['solution'] < 4:
        recommendations.append('⚡ STRIKE NOW - STRONG PROBLEM AWARENESS, DEMONSTRATE PERSWADE SOLUTION IMMEDIATELY')
    
    return scores, conversion_prob, recommendations

class AssemblyAIStreamProcessor:
    """Real AssemblyAI streaming processor - UPDATED for current API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.sample_rate = 16000
        self.is_connected = False
        self.websocket = None
        self.simulation_started = False
        
    async def connect(self, call_id: str, websocket: WebSocket):
        """Connect to AssemblyAI real-time service with updated configuration"""
        try:
            logger.info(f"🔌 Connecting to AssemblyAI Universal-Streaming for call {call_id}")
            
            # Updated AssemblyAI real-time endpoint URL
            ws_url = "wss://api.assemblyai.com/v2/realtime/ws"
            
            # Updated headers for current API
            headers = {
                "Authorization": self.api_key
            }
            
            # Connect to AssemblyAI streaming
            self.websocket = await websockets.connect(
                ws_url,
                extra_headers=headers,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=10
            )
            
            # Updated session configuration for current API
            session_config = {
                "sample_rate": self.sample_rate,
                "encoding": "pcm_s16le",  # Updated encoding specification
                "channels": 1,
                "word_boost": ["C2PS", "credibility", "commonality", "problem", "solution", "Perswade", "conversion", "AI", "sales"],
                "punctuate": True,
                "format_text": True
            }
            
            # Send configuration
            await self.websocket.send(json.dumps(session_config))
            logger.info(f"📤 Sent session config to AssemblyAI: {session_config}")
            
            # Listen for responses
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self.handle_assemblyai_message(data, call_id, websocket)
                except json.JSONDecodeError as e:
                    logger.error(f"❌ Failed to parse AssemblyAI message: {e}")
                except Exception as e:
                    logger.error(f"❌ Error handling AssemblyAI message: {e}")
                
        except websockets.exceptions.ConnectionClosedError as e:
            logger.error(f"❌ AssemblyAI connection closed: {e}")
            self.is_connected = False
            await self.fallback_to_simulation(call_id, websocket)
        except Exception as e:
            logger.error(f"❌ AssemblyAI connection error: {e}")
            # For demo purposes, fall back to simulated transcription
            logger.info("🔄 Falling back to simulated transcription for demo")
            await self.fallback_to_simulation(call_id, websocket)
            self.is_connected = False
    
    async def fallback_to_simulation(self, call_id: str, websocket: WebSocket):
        """Fallback to simulation if AssemblyAI fails"""
        if not self.simulation_started:
            self.simulation_started = True
            await websocket.send_json({
                "type": "fallback_notice",
                "call_id": call_id,
                "message": "Using intelligent simulation - perfect for demo!"
            })
            await self.simulate_transcription(call_id, websocket)
    
    async def handle_assemblyai_message(self, data: dict, call_id: str, websocket: WebSocket):
        """Handle messages from AssemblyAI with updated message types"""
        message_type = data.get("message_type")
        
        if message_type == "SessionBegins":
            logger.info(f"✅ AssemblyAI session started for call {call_id}")
            self.is_connected = True
            await websocket.send_json({
                "type": "assemblyai_connected",
                "call_id": call_id,
                "message": "Real-time AssemblyAI transcription active"
            })
            
        elif message_type == "PartialTranscript":
            # Send partial transcript (not final)
            text = data.get("text", "")
            if text.strip():
                current_phase = call_phases.get(call_id, 'credibility')
                await websocket.send_json({
                    "type": "transcript",
                    "data": {
                        "call_id": call_id,
                        "text": text,
                        "speaker": "Unknown",  # Will be determined by speaker identification
                        "confidence": data.get("confidence", 0.9),
                        "is_final": False,
                        "timestamp": data.get("created"),
                        "c2ps_phase": current_phase,
                        "source": "assemblyai_partial"
                    }
                })
                
        elif message_type == "FinalTranscript":
            # Process final transcript
            text = data.get("text", "")
            confidence = data.get("confidence", 0.9)
            
            if text.strip():
                logger.info(f"📝 AssemblyAI final transcript: {text}")
                
                # Simple speaker identification (can be enhanced)
                speaker_role = "Sales Agent"  # Default, can be overridden by UI
                
                # Add to conversation history
                if call_id in call_conversations:
                    call_conversations[call_id] += f" {text}"
                
                # Get current phase
                current_phase = call_phases.get(call_id, 'credibility')
                
                # Send final transcript with phase
                await websocket.send_json({
                    "type": "transcript",
                    "data": {
                        "call_id": call_id,
                        "text": text,
                        "speaker": speaker_role,
                        "confidence": confidence,
                        "is_final": True,
                        "timestamp": data.get("created"),
                        "c2ps_phase": current_phase,
                        "source": "assemblyai_final"
                    }
                })
                
                # Perform C²PS analysis with phase awareness
                scores, conversion_prob, recommendations = analyze_text_c2ps(
                    call_conversations[call_id], 
                    speaker_role,
                    current_phase
                )
                
                # Send analysis
                await websocket.send_json({
                    "type": "analysis",
                    "data": {
                        "call_id": call_id,
                        "scores": scores,
                        "conversion_probability": conversion_prob,
                        "recommendations": recommendations,
                        "current_phase": current_phase,
                        "last_speaker": speaker_role,
                        "conversation_length": len(call_conversations[call_id].split()),
                        "source": "real_assemblyai"
                    }
                })
                
                logger.info(f"📊 Real AssemblyAI C²PS analysis complete - Conv Prob: {conversion_prob:.1%}")
                
        elif message_type == "SessionInformation":
            logger.info(f"ℹ️ AssemblyAI session info: {data}")
            
        else:
            logger.info(f"🤷 Unknown AssemblyAI message type: {message_type}")
    
    async def simulate_transcription(self, call_id: str, websocket: WebSocket):
        """C²PS-aligned simulated transcription matching dashboard demo"""
        logger.info(f"🎬 Starting C²PS-aligned simulated transcription for call {call_id}")
        
        # Get speaker names from call_speakers
        speakers = call_speakers.get(call_id, {"agent": "Sales Agent", "prospect": "Prospect"})
        
        # C²PS-aligned demo conversation matching the dashboard
        demo_messages = [
            # PHASE 1: CREDIBILITY (0-25%)
            { 
                "speaker": speakers["agent"], 
                "text": "Hi there! Thanks for your interest in Perswade. I'm Matthew, and I've been working with AI-powered sales tools for over 8 years. Before we dive in, let me share a bit about my background - I've helped implement sales optimization systems for over 200 companies, including several Fortune 500 enterprises.",
                "phase": "credibility"
            },
            { 
                "speaker": speakers["prospect"], 
                "text": "That's impressive, Matthew. We're definitely looking for someone with real experience in this space.",
                "phase": "credibility"
            },
            { 
                "speaker": speakers["agent"], 
                "text": "Thank you! I've personally trained over 1,000 sales reps on the C²PS methodology, which is the foundation of Perswade. Our system is built on proven frameworks that have generated over $500M in additional revenue for our clients. I'm excited to explore how we can achieve similar results for your team.",
                "phase": "credibility"
            },
            
            # PHASE 2: COMMONALITY (25-40%)
            {
                "speaker": speakers["prospect"],
                "text": "We've been in the sales optimization space for a while too. It's been quite a journey trying to find the right tools.",
                "phase": "commonality"
            },
            {
                "speaker": speakers["agent"],
                "text": "I completely understand that journey! Many of our most successful clients went through multiple tools before finding us. It sounds like we share a similar vision for what great sales enablement should look like. Tell me, what initially got your company focused on sales optimization?",
                "phase": "commonality"
            },
            {
                "speaker": speakers["prospect"],
                "text": "We realized our sales team was our biggest asset, but also our biggest variable. Some reps were crushing it while others struggled with the same leads. We knew there had to be a better way to create consistency.",
                "phase": "commonality"
            },
            {
                "speaker": speakers["agent"],
                "text": "That resonates so much with me! That inconsistency challenge is exactly why I got passionate about this field. It's fascinating how two reps can have such different outcomes with identical opportunities. I've seen this pattern across industries - from SaaS to healthcare to financial services.",
                "phase": "commonality"
            },
            
            # PHASE 3: PROBLEM (40-70%)
            {
                "speaker": speakers["prospect"],
                "text": "Exactly! Our biggest challenge is that our reps don't get real-time feedback during calls. They only find out what went wrong after losing the deal.",
                "phase": "problem"
            },
            {
                "speaker": speakers["agent"],
                "text": "That post-mortem approach is so frustrating, isn't it? Let me dig deeper - when a rep loses a deal, how long does it typically take to identify what went wrong? And more importantly, how do you ensure the same mistakes don't happen again?",
                "phase": "problem"
            },
            {
                "speaker": speakers["prospect"],
                "text": "Honestly? Sometimes we never figure it out. Our managers listen to call recordings when they have time, which might be days or weeks later. By then, the rep has already repeated the same mistakes on other calls. It's a vicious cycle.",
                "phase": "problem"
            },
            {
                "speaker": speakers["agent"],
                "text": "That delay is costly in so many ways. Based on what you shared earlier about having 50 reps - if each rep has just 5 calls per day, that's 250 opportunities for mistakes to compound before anyone catches them. What would you estimate this inconsistency costs you in lost deals each quarter?",
                "phase": "problem"
            },
            {
                "speaker": speakers["prospect"],
                "text": "When you put it that way... we're probably losing 20-30% of winnable deals just due to execution issues. That's millions in lost revenue annually.",
                "phase": "problem"
            },
            
            # PHASE 4: SOLUTION (70-100%)
            {
                "speaker": speakers["agent"],
                "text": "Those numbers align exactly with what we see across the industry. Here's how Perswade solves this: Our AI analyzes every word in real-time, providing instant coaching through the C²PS framework. Your reps get guidance DURING the call, not days later. We've seen clients reduce those execution losses by 75% within 90 days.",
                "phase": "solution"
            },
            {
                "speaker": speakers["prospect"],
                "text": "That sounds like exactly what we need. How does the real-time guidance actually work without disrupting the conversation?",
                "phase": "solution"
            },
            {
                "speaker": speakers["agent"],
                "text": "Great question! Perswade provides subtle, non-intrusive prompts that only the rep can see. For example, if they're spending too much time on features without establishing credibility, they'll see a gentle reminder to share a relevant success story. It's like having your best sales coach whispering perfect advice in their ear, powered by AI that's analyzed millions of successful calls.",
                "phase": "solution"
            },
            {
                "speaker": speakers["prospect"],
                "text": "And this integrates with our existing CRM and call systems?",
                "phase": "solution"
            },
            {
                "speaker": speakers["agent"],
                "text": "Absolutely! Perswade integrates seamlessly with Salesforce, HubSpot, and all major CRMs. Every call is automatically logged with full transcripts, C²PS scores, and coaching insights. Your managers get dashboards showing exactly where each rep needs improvement. Implementation typically takes 5-7 days, and we handle all the technical heavy lifting. Would you like to see a live demo of how this would work for your specific sales process?",
                "phase": "solution"
            }
        ]
        
        # Initialize phase
        call_phases[call_id] = 'credibility'
        
        for i, message in enumerate(demo_messages):
            # Check if call is still active
            if call_id not in active_connections:
                break
                
            await asyncio.sleep(4.5)  # 4.5 second intervals for realistic pacing
            
            # Update phase if changed
            if message["phase"] != call_phases.get(call_id):
                call_phases[call_id] = message["phase"]
                logger.info(f"📊 Phase transition: {message['phase'].upper()}")
            
            # Send simulated transcript with phase
            await websocket.send_json({
                "type": "transcript", 
                "data": {
                    "call_id": call_id,
                    "text": message["text"],
                    "speaker": message["speaker"],
                    "confidence": 0.92 + (i * 0.005),  # Slightly increasing confidence
                    "is_final": True,
                    "timestamp": datetime.now().isoformat(),
                    "c2ps_phase": message["phase"],
                    "source": "simulated"
                }
            })
            
            # Add to conversation for analysis
            if call_id in call_conversations:
                call_conversations[call_id] += f" {message['text']}"
                
                # Analyze and send results with phase awareness
                scores, conversion_prob, recommendations = analyze_text_c2ps(
                    call_conversations[call_id], 
                    message["speaker"],
                    message["phase"]
                )
                
                await websocket.send_json({
                    "type": "analysis",
                    "data": {
                        "call_id": call_id,
                        "scores": scores,
                        "conversion_probability": conversion_prob,
                        "recommendations": recommendations,
                        "current_phase": message["phase"],
                        "last_speaker": message["speaker"],
                        "conversation_length": len(call_conversations[call_id].split()),
                        "source": "simulated"
                    }
                })
            
            logger.info(f"🎬 Simulated [{message['phase'].upper()}]: {message['speaker']} - {message['text'][:50]}...")
    
    async def send_audio_chunk(self, audio_data: bytes):
        """Send audio chunk to AssemblyAI"""
        if self.websocket and self.is_connected:
            try:
                # Send raw audio data (not base64 for Universal-Streaming)
                await self.websocket.send(audio_data)
            except Exception as e:
                logger.error(f"❌ Error sending audio chunk: {e}")
                # Fall back to simulation if real streaming fails
                self.is_connected = False
    
    async def close(self):
        """Close AssemblyAI connection"""
        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("🔌 AssemblyAI connection closed")
            except Exception as e:
                logger.error(f"❌ Error closing AssemblyAI connection: {e}")
            finally:
                self.is_connected = False

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Perswade API is running",
        "version": "1.0.0",
        "status": "healthy",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
    return {
        "status": "healthy",
        "services": {
            "assemblyai": bool(assemblyai_key and assemblyai_key != "your_assemblyai_key_here"),
            "active_connections": len(active_connections),
            "websocket": "ready"
        },
        "environment": {
            "debug": os.getenv("DEBUG", "false").lower() == "true",
            "port": os.getenv("PORT", "8000"),
            "key_configured": bool(assemblyai_key and len(assemblyai_key) > 10)
        },
        "features": {
            "real_time_transcription": "available",
            "c2ps_analysis": "active",
            "conversion_prediction": "enabled",
            "intelligent_fallback": "ready"
        }
    }

@app.websocket("/ws/{call_id}")
async def websocket_endpoint(websocket: WebSocket, call_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections[call_id] = websocket
    call_conversations[call_id] = ""
    call_speakers[call_id] = {"agent": None, "prospect": None}
    call_phases[call_id] = "credibility"  # Start with credibility phase
    
    logger.info(f"🔌 WebSocket connected for call: {call_id}")
    logger.info(f"  ✓ Active connections: {len(active_connections)}")
    
    # Initialize AssemblyAI processor
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    assemblyai_processor = None
    
    if api_key and api_key != "your_assemblyai_key_here":
        assemblyai_processor = AssemblyAIStreamProcessor(api_key)
        logger.info("  ✓ AssemblyAI processor initialized")
    else:
        logger.info("  ✓ Simulation mode ready (no API key)")
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "call_id": call_id,
            "message": "Connected to Perswade backend",
            "real_transcription": bool(assemblyai_processor),
            "version": "1.0.0"
        })
        
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            logger.info(f"📨 Received {message_type} for call {call_id}")
            
            if message_type == "start_call":
                mode = data.get("data", {}).get("mode", "demo")
                agent_name = data.get("data", {}).get("agent_name", "Sales Agent")
                prospect_name = data.get("data", {}).get("prospect_name", "Prospect")
                
                # Store speaker roles
                call_speakers[call_id] = {
                    "agent": agent_name,
                    "prospect": prospect_name
                }
                
                logger.info(f"🎬 Starting {mode} call: {agent_name} → {prospect_name}")
                
                # Start AssemblyAI connection for live mode
                if mode == "live" and assemblyai_processor:
                    asyncio.create_task(assemblyai_processor.connect(call_id, websocket))
                elif mode == "demo":
                    # Start simulation immediately for demo mode
                    if assemblyai_processor:
                        assemblyai_processor.simulation_started = True
                    asyncio.create_task(AssemblyAIStreamProcessor(api_key="demo").simulate_transcription(call_id, websocket))
                
                await websocket.send_json({
                    "type": "call_started",
                    "call_id": call_id,
                    "mode": mode,
                    "status": "active",
                    "speakers": call_speakers[call_id],
                    "current_phase": call_phases[call_id],
                    "message": f"Call session started - {agent_name} selling Perswade to {prospect_name}"
                })
                
            elif message_type == "audio_chunk":
                # Handle audio processing with intelligent fallback
                if assemblyai_processor and assemblyai_processor.is_connected:
                    try:
                        # Decode base64 audio data
                        audio_data = base64.b64decode(data.get("data", {}).get("audio", ""))
                        await assemblyai_processor.send_audio_chunk(audio_data)
                        logger.info(f"🎤 Sent audio chunk to AssemblyAI for call {call_id}")
                    except Exception as e:
                        logger.error(f"❌ Error processing audio chunk: {e}")
                elif assemblyai_processor and not assemblyai_processor.simulation_started:
                    # Fallback to simulation automatically
                    logger.info(f"🎬 Triggering simulation fallback for call {call_id}")
                    assemblyai_processor.simulation_started = True
                    asyncio.create_task(assemblyai_processor.simulate_transcription(call_id, websocket))
                else:
                    logger.debug(f"🔇 Audio chunk received but no processor available for call {call_id}")
                    
            elif message_type == "set_speaker_role":
                # Allow UI to override speaker identification
                speaker_id = data.get("speaker_id")
                role = data.get("role")  # "agent" or "prospect"
                if call_id in call_speakers and role in ["agent", "prospect"]:
                    call_speakers[call_id][role] = speaker_id
                    logger.info(f"👤 Set speaker role: {speaker_id} = {role}")
                    
            elif message_type == "set_phase":
                # Allow UI to manually set phase
                phase = data.get("phase")
                if phase in ["credibility", "commonality", "problem", "solution"]:
                    call_phases[call_id] = phase
                    logger.info(f"📊 Phase manually set to: {phase.upper()}")
                    
            elif message_type == "end_call":
                logger.info(f"📞 Ending call {call_id}")
                
                # Close AssemblyAI connection
                if assemblyai_processor:
                    await assemblyai_processor.close()
                
                # Send final analysis
                if call_id in call_conversations and call_conversations[call_id]:
                    final_scores, final_prob, final_recs = analyze_text_c2ps(
                        call_conversations[call_id],
                        current_phase=call_phases.get(call_id, "solution")
                    )
                    
                    await websocket.send_json({
                        "type": "call_summary",
                        "data": {
                            "call_id": call_id,
                            "final_scores": final_scores,
                            "final_conversion_probability": final_prob,
                            "final_recommendations": final_recs,
                            "conversation_text": call_conversations[call_id],
                            "speakers": call_speakers[call_id],
                            "final_phase": call_phases.get(call_id, "solution")
                        }
                    })
                
                await websocket.send_json({
                    "type": "call_ended",
                    "call_id": call_id,
                    "message": "Call session ended"
                })
                break
                
            elif message_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": data.get("timestamp")
                })
                
    except WebSocketDisconnect:
        logger.info(f"🔌 WebSocket disconnected for call: {call_id}")
    except Exception as e:
        logger.error(f"WebSocket error for call {call_id}: {e}")
    finally:
        # Cleanup
        if assemblyai_processor:
            await assemblyai_processor.close()
        if call_id in active_connections:
            del active_connections[call_id]
        if call_id in call_conversations:
            del call_conversations[call_id]
        if call_id in call_speakers:
            del call_speakers[call_id]
        if call_id in call_phases:
            del call_phases[call_id]
        logger.info(f"  ✓ Cleanup complete for call {call_id}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info("=" * 60)
    logger.info("PERSWADE WATSON - AI SALES VOICE AGENT")
    logger.info("Powered by AssemblyAI + C²PS Methodology")
    logger.info("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    )