'use client';

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Mic, 
  MicOff, 
  TrendingUp, 
  Users, 
  Target, 
  Lightbulb,
  BarChart3,
  Activity,
  Zap,
  CheckCircle,
  Wifi,
  WifiOff,
  Volume2,
  Play,
  Square,
  User,
  Settings,
  Crown,
  Briefcase,
  Moon,
  Sun,
  Headphones,
  Radio,
  ChevronRight
} from 'lucide-react';

// Types
interface TranscriptSegment {
  id: string;
  text: string;
  speaker: string;
  timestamp: string;
  confidence: number;
  is_final: boolean;
  c2psPhase?: 'credibility' | 'commonality' | 'problem' | 'solution';
}

interface C2PSScores {
  credibility: number;
  commonality: number;
  problem: number;
  solution: number;
}

interface SpeakerRoles {
  agent: string;
  prospect: string;
}

interface AudioSourceConfig {
  agentSource: 'microphone' | 'system';
  prospectSource: 'microphone' | 'system';
}

interface WebSocketMessage {
  type: string;
  data?: {
    text?: string;
    speaker?: string;
    timestamp?: string;
    confidence?: number;
    is_final?: boolean;
    scores?: C2PSScores;
    conversion_probability?: number;
    recommendations?: string[];
    real_transcription?: boolean;
    speakers?: SpeakerRoles;
    message?: string;
    // Add these audio-related fields:
    audio?: string;
    chunk_number?: number;
    size?: number;
    mode?: string;
    agent_name?: string;
    prospect_name?: string;
    participants?: string[];
  };
}

// Enhanced WebSocket hook with improved error handling and debugging
const useWebSocket = (url: string) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [connectionError, setConnectionError] = useState<string>('');
  const retryTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    // Clear any previous retry timeout
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
    }

    // Don't attempt connection if URL is empty or invalid
    if (!url || url === '' || url.includes('undefined')) {
      console.log('⏳ Waiting for valid WebSocket URL...', { url, isEmpty: !url });
      return;
    }

    console.log('🔌 Creating WebSocket connection to:', url);
    setConnectionError('');
    
    let ws: WebSocket;
    let connectionTimeout: ReturnType<typeof setTimeout>;
    
    try {
      ws = new WebSocket(url);
      
      // Set connection timeout
      connectionTimeout = setTimeout(() => {
        if (ws.readyState === WebSocket.CONNECTING) {
          console.error('⏰ WebSocket connection timeout after 5 seconds');
          setConnectionError('Connection timeout');
          ws.close();
        }
      }, 5000);
      
      ws.onopen = () => {
        clearTimeout(connectionTimeout);
        console.log('✅ WebSocket connection opened successfully!', {
          url,
          readyState: ws.readyState,
          protocol: ws.protocol,
          extensions: ws.extensions
        });
        setIsConnected(true);
        setSocket(ws);
        setConnectionError('');
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message received:', {
            type: data.type,
            hasData: !!data.data,
            timestamp: new Date().toISOString()
          });
          setLastMessage(data);
        } catch (error) {
          console.error('❌ Failed to parse WebSocket message:', {
            error,
            rawData: event.data,
            dataType: typeof event.data
          });
        }
      };
      
      ws.onclose = (event) => {
        clearTimeout(connectionTimeout);
        console.log('🔌 WebSocket connection closed:', {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
          url
        });
        
        setIsConnected(false);
        setSocket(null);
        
        // Set error message based on close code
        if (event.code === 1006) {
          setConnectionError('Connection lost unexpectedly');
        } else if (event.code !== 1000 && event.code !== 1001) {
          setConnectionError(`Connection closed with code ${event.code}: ${event.reason}`);
        }
      };
      
      ws.onerror = (error) => {
        clearTimeout(connectionTimeout);
        console.error('🚨 WebSocket error occurred:', {
          error,
          url,
          readyState: ws.readyState,
          timestamp: new Date().toISOString()
        });
        
        setConnectionError('WebSocket connection failed');
        setIsConnected(false);
        
        // Additional debugging
        console.error('🔍 WebSocket error details:', {
          wsConstructor: typeof WebSocket,
          urlValid: url.startsWith('ws://') || url.startsWith('wss://'),
          browserSupport: 'WebSocket' in window,
          networkOnline: navigator.onLine
        });
      };

      // Store reference for cleanup
      setSocket(ws);
      
    } catch (error) {
      clearTimeout(connectionTimeout!);
      console.error('❌ Failed to create WebSocket:', {
        error,
        url,
        errorMessage: error instanceof Error ? error.message : 'Unknown error'
      });
      setConnectionError(`Failed to create WebSocket: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    // Cleanup function
    return () => {
      if (connectionTimeout) {
        clearTimeout(connectionTimeout);
      }
      if (ws && ws.readyState === WebSocket.OPEN) {
        console.log('🧹 Cleaning up WebSocket connection');
        ws.close(1000, 'Component cleanup');
      }
    };
  }, [url]);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (!socket) {
      console.warn('⚠️ Cannot send message - no socket object');
      return false;
    }
    
    if (socket.readyState !== WebSocket.OPEN) {
      console.warn('⚠️ Cannot send message - WebSocket not open:', {
        readyState: socket.readyState,
        states: {
          [WebSocket.CONNECTING]: 'CONNECTING',
          [WebSocket.OPEN]: 'OPEN',
          [WebSocket.CLOSING]: 'CLOSING',
          [WebSocket.CLOSED]: 'CLOSED'
        }[socket.readyState]
      });
      return false;
    }

    try {
      const messageStr = JSON.stringify(message);
      console.log('📤 Sending WebSocket message:', {
        type: message.type,
        messageSize: messageStr.length,
        dataSize: message.data ? JSON.stringify(message.data).length : 0,
        timestamp: new Date().toISOString()
      });
      socket.send(messageStr);
      return true;
    } catch (error) {
      console.error('❌ Failed to send WebSocket message:', {
        error,
        message: message.type,
        socketState: socket.readyState
      });
      return false;
    }
  }, [socket]);

  return { 
    isConnected, 
    lastMessage, 
    sendMessage,
    connectionError,
    // Debug info
    debug: {
      url,
      socketState: socket?.readyState,
      hasSocket: !!socket
    }
  };
};

const PerswadeDashboard: React.FC = () => {
  // Dark mode state
  const [isDarkMode, setIsDarkMode] = useState(false);
  
  // Mode state - Demo vs Live + Real demo mode
  const [isLiveMode, setIsLiveMode] = useState(false);
  const [showLiveConfig, setShowLiveConfig] = useState(false);
  
  // Speaker role configuration
  const [speakerRoles, setSpeakerRoles] = useState<SpeakerRoles>({
    agent: "Sales Agent",
    prospect: "Prospect"
  });
  
  // Audio source configuration for live mode
  const [audioSources, setAudioSources] = useState<AudioSourceConfig>({
    agentSource: 'microphone',
    prospectSource: 'system'
  });
  
  // Call state - Prevent hydration mismatch
  const [callId, setCallId] = useState('');
  const [isCallActive, setIsCallActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  
  // Live audio state - Real microphone functionality
  const [audioStream, setAudioStream] = useState<MediaStream | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioLevel, setAudioLevel] = useState(0);
  const [micPermission, setMicPermission] = useState<'granted' | 'denied' | 'prompt'>('prompt');
  const [realTranscription, setRealTranscription] = useState(false);
  
  // Audio processing refs
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationRef = useRef<number | undefined>(undefined);
  const demoStartedRef = useRef(false);
  
  // Real-time data
  const [transcript, setTranscript] = useState<TranscriptSegment[]>([]);
  const [currentText, setCurrentText] = useState('');
  const [c2psScores, setC2psScores] = useState<C2PSScores>({
    credibility: 0,
    commonality: 0,
    problem: 0,
    solution: 0
  });
  const [conversionProbability, setConversionProbability] = useState(0);
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [currentPhase, setCurrentPhase] = useState<'credibility' | 'commonality' | 'problem' | 'solution'>('credibility');

  // Toggle dark mode - Prevent infinite loops
  useEffect(() => {
    // Only update if we're in the browser
    if (typeof window !== 'undefined') {
      if (isDarkMode) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }
  }, [isDarkMode]);

  // Set callId on client side only to prevent hydration mismatch
  useEffect(() => {
    const newCallId = `call_${Date.now()}`;
    console.log('🆔 Generated call ID:', newCallId);
    setCallId(newCallId);
  }, []);

  // Enhanced WebSocket URL construction with debugging
  const wsUrl = useMemo(() => {
    if (!callId) {
      console.log('🔍 No callId yet, WebSocket URL will be empty');
      return '';
    }
    
    // Construct WebSocket URL
    const baseUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    const fullUrl = `${baseUrl}/ws/${callId}`;
    
    console.log('🔗 WebSocket URL constructed:', {
      callId,
      baseUrl,
      fullUrl,
      env: process.env.NEXT_PUBLIC_WS_URL
    });
    
    return fullUrl;
  }, [callId]);
  
  const { isConnected, lastMessage, sendMessage, connectionError } = useWebSocket(wsUrl);

  // Audio level monitoring for live mode
  const updateAudioLevel = useCallback(() => {
    if (!analyserRef.current) return;
    
    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    analyserRef.current.getByteFrequencyData(dataArray);
    
    const average = dataArray.reduce((acc, val) => acc + val, 0) / dataArray.length;
    setAudioLevel(average / 255 * 100);
    
    animationRef.current = requestAnimationFrame(updateAudioLevel);
  }, []);

  // Enhanced audio capture with better processing
  const initializeAudioCapture = useCallback(async () => {
    try {
      console.log('🎤 Requesting microphone access for REAL demo...');
      
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 16000,
          channelCount: 1
        }
      });
      
      setAudioStream(stream);
      setMicPermission('granted');
      console.log('✅ Microphone access granted');
      
      // Set up audio context for level monitoring
      audioContextRef.current = new AudioContext({ sampleRate: 16000 });
      const source = audioContextRef.current.createMediaStreamSource(stream);
      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 256;
      source.connect(analyserRef.current);
      
      // Start level monitoring
      updateAudioLevel();
      
      // Enhanced MediaRecorder setup with proper format for AssemblyAI
      const mimeType = 'audio/webm;codecs=opus';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        console.warn('⚠️ Preferred MIME type not supported, using default');
      }
      
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported(mimeType) ? mimeType : undefined,
        audioBitsPerSecond: 16000
      });
      
      let audioChunkCount = 0;
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0 && isConnected && isLiveMode) {
          audioChunkCount++;
          console.log(`🎤 Processing audio chunk #${audioChunkCount}, size: ${event.data.size} bytes`);
          
          // Convert to the format expected by backend
          const reader = new FileReader();
          reader.onloadend = () => {
            try {
              const arrayBuffer = reader.result as ArrayBuffer;
              const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
              
              console.log(`📤 Sending audio chunk #${audioChunkCount} to backend`);
              const success = sendMessage({
                type: 'audio_chunk',
                data: {
                  audio: base64Audio,
                  timestamp: new Date().toISOString(),
                  chunk_number: audioChunkCount,
                  size: event.data.size
                }
              });
              
              if (!success) {
                console.error('❌ Failed to send audio chunk - WebSocket not ready');
              }
            } catch (error) {
              console.error('❌ Error processing audio chunk:', error);
            }
          };
          reader.readAsArrayBuffer(event.data);
        } else {
          console.log('🔇 Audio chunk received but conditions not met:', {
            dataSize: event.data.size,
            isConnected,
            isLiveMode
          });
        }
      };
      
      recorder.onerror = (event: Event) => {
        console.error('❌ MediaRecorder error:', event);
      };
      
      recorder.onstart = () => {
        console.log('✅ Audio recording started successfully');
      };
      
      recorder.onstop = () => {
        console.log('🛑 Audio recording stopped');
      };
      
      setMediaRecorder(recorder);
      console.log('✅ Real audio capture initialized for Perswade demo');
      
    } catch (error) {
      console.error('❌ Failed to access microphone:', error);
      setMicPermission('denied');
      
      // Show user-friendly error message
      if (error instanceof Error) {
        if (error.name === 'NotAllowedError') {
          console.error('🚫 Microphone permission denied by user');
        } else if (error.name === 'NotFoundError') {
          console.error('🔍 No microphone device found');
        } else {
          console.error('❓ Unknown microphone error:', error.message);
        }
      }
    }
  }, [isConnected, sendMessage, updateAudioLevel, isLiveMode]);

  // Cleanup audio resources
  const cleanupAudio = useCallback(() => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
    
    if (audioStream) {
      audioStream.getTracks().forEach(track => track.stop());
      setAudioStream(null);
    }
    
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    
    setAudioLevel(0);
    setMediaRecorder(null);
  }, [audioStream, mediaRecorder]);

  // Simulate C2PS analysis for demo mode only
  const simulateAnalysis = useCallback((text: string, phase: string) => {
    if (isLiveMode) return; // Real analysis happens on backend
    
    const textLower = text.toLowerCase();
    
    // Phase-specific scoring - FIX: Change let to const
    const phaseMultiplier = {
      credibility: { credibility: 2, commonality: 0.5, problem: 0.3, solution: 0.1 },
      commonality: { credibility: 1.2, commonality: 2, problem: 0.5, solution: 0.2 },
      problem: { credibility: 1, commonality: 1.2, problem: 2, solution: 0.5 },
      solution: { credibility: 1, commonality: 1, problem: 1.5, solution: 2 }
    }[phase] || { credibility: 1, commonality: 1, problem: 1, solution: 1 };
    
    // Enhanced keyword scoring for more realistic demo
    const credibilityKeywords = ['experience', 'expert', 'proven', 'clients', 'years', 'successful', 'enterprise', 'roi', 'results', 'ai-powered', 'methodology'];
    const commonalityKeywords = ['understand', 'similar', 'agree', 'exactly', 'absolutely', 'right', 'same', 'also', 'too', 'relate', 'familiar'];
    const problemKeywords = ['problem', 'challenge', 'issue', 'pain', 'struggle', 'difficult', 'frustrating', 'inconsistent', 'missing', 'losing', 'inefficient'];
    const solutionKeywords = ['solution', 'benefit', 'improve', 'save', 'reduce', 'increase', 'optimize', 'transform', 'real-time', 'perswade', 'implementation'];
    
    const scoreKeywords = (keywords: string[], multiplier: number) => {
      const baseScore = keywords.reduce((score, keyword) => {
        return textLower.includes(keyword) ? score + 1.5 : score;
      }, 0);
      // Add some randomness for realism but keep it progressive
      return Math.min(10, (baseScore + Math.random() * 1) * multiplier);
    };
    
    const newScores = {
      credibility: Math.max(c2psScores.credibility, scoreKeywords(credibilityKeywords, phaseMultiplier.credibility)),
      commonality: Math.max(c2psScores.commonality, scoreKeywords(commonalityKeywords, phaseMultiplier.commonality)),
      problem: Math.max(c2psScores.problem, scoreKeywords(problemKeywords, phaseMultiplier.problem)),
      solution: Math.max(c2psScores.solution, scoreKeywords(solutionKeywords, phaseMultiplier.solution))
    };
    
    setC2psScores(newScores);
    
    const avgScore = Object.values(newScores).reduce((a, b) => a + b, 0) / 4;
    setConversionProbability(Math.round(Math.min(95, avgScore * 12)));
    
    // Phase-specific recommendations
    const newRecommendations = [];
    
    if (phase === 'credibility') {
      if (newScores.credibility < 5) newRecommendations.push('💼 ESTABLISH MORE EXPERTISE - SHARE YOUR BACKGROUND');
      if (newScores.commonality < 2) newRecommendations.push('🤝 PREPARE TO TRANSITION TO RAPPORT BUILDING');
    } else if (phase === 'commonality') {
      if (newScores.commonality < 5) newRecommendations.push('💬 BUILD MORE RAPPORT - FIND SHARED EXPERIENCES');
      if (newScores.problem < 2) newRecommendations.push('❗ PREPARE TO EXPLORE THEIR CHALLENGES');
    } else if (phase === 'problem') {
      if (newScores.problem < 7) newRecommendations.push('🔍 DIG DEEPER INTO PAIN POINTS - QUANTIFY IMPACT');
      if (newScores.solution < 3) newRecommendations.push('💡 PREPARE TO PRESENT PERSWADE AS THE SOLUTION');
    } else if (phase === 'solution') {
      if (newScores.solution < 7) newRecommendations.push('🎯 CONNECT FEATURES TO THEIR SPECIFIC PROBLEMS');
      if (avgScore > 7) newRecommendations.push('✅ MOVE TOWARD CLOSING - ASK FOR NEXT STEPS');
    }
    
    setRecommendations(newRecommendations);
  }, [isLiveMode, c2psScores]);

  // Handle WebSocket messages - Enhanced for real demo
  useEffect(() => {
    if (!lastMessage) return;

    const { type, data } = lastMessage;

    switch (type) {
      case 'connected':
        console.log('✅ Backend connection established');
        if (data?.real_transcription) {
          setRealTranscription(true);
          console.log('🎯 Real AssemblyAI transcription available!');
        }
        break;
        
      case 'call_started':
        console.log('📞 Call session started:', data?.speakers);
        if (data?.speakers) {
          setSpeakerRoles(data.speakers);
        }
        break;
        
      case 'transcript':
        if (data?.is_final) {
          const newSegment: TranscriptSegment = {
            id: `${Date.now()}_${Math.random()}`,
            text: data.text || '',
            speaker: data.speaker || 'Unknown',
            timestamp: data.timestamp || new Date().toISOString(),
            confidence: data.confidence || 0.9,
            is_final: true,
            c2psPhase: currentPhase
          };
          setTranscript(prev => [...prev, newSegment]);
          setCurrentText('');
          
          // Real analysis happens on backend for live mode
          if (!isLiveMode && data.text) {
            // Use setTimeout to avoid state update during render
            setTimeout(() => {
              simulateAnalysis(data.text!, currentPhase);
            }, 0);
          }
        } else if (data?.text) {
          setCurrentText(data.text);
        }
        break;
        
      case 'analysis':
        // Real C²PS analysis from backend
        if (data?.scores) {
          setC2psScores(data.scores);
        }
        if (typeof data?.conversion_probability === 'number') {
          setConversionProbability(Math.round(data.conversion_probability * 100));
        }
        if (data?.recommendations) {
          setRecommendations(data.recommendations);
        }
        console.log('📊 Real C²PS analysis received:', {
          scores: data?.scores,
          conversionProb: data?.conversion_probability,
          recommendations: data?.recommendations?.length || 0
        });
        break;
        
      case 'call_summary':
        console.log('📋 Final call summary:', data);
        break;
        
      case 'call_ended':
        console.log('📞 Call session ended');
        setIsCallActive(false);
        setIsRecording(false);
        break;
        
      case 'fallback_notice':
        console.log('🔄 Fallback to simulation activated:', data?.message);
        break;
        
      default:
        console.log('🤷 Unknown message type:', type);
    }
  }, [lastMessage, isLiveMode, currentPhase, simulateAnalysis]);

  // C²PS-aligned demo conversation
  useEffect(() => {
    if (!isCallActive || isLiveMode || transcript.length > 0 || demoStartedRef.current) {
      return; // Exit early if conditions not met or demo already started
    }

    // Mark demo as started
    demoStartedRef.current = true;

    const demoMessages = [
      // PHASE 1: CREDIBILITY (0-25%)
      { 
        speaker: speakerRoles.agent, 
        text: "Hi there! Thanks for your interest in Perswade. I'm Matthew, and I've been working with AI-powered sales tools for over 8 years. Before we dive in, let me share a bit about my background - I've helped implement sales optimization systems for over 200 companies, including several Fortune 500 enterprises.",
        phase: 'credibility'
      },
      { 
        speaker: speakerRoles.prospect, 
        text: "That's impressive, Matthew. We're definitely looking for someone with real experience in this space.",
        phase: 'credibility'
      },
      { 
        speaker: speakerRoles.agent, 
        text: "Thank you! I've personally trained over 1,000 sales reps on the C²PS methodology, which is the foundation of Perswade. Our system is built on proven frameworks that have generated over $500M in additional revenue for our clients. I'm excited to explore how we can achieve similar results for your team.",
        phase: 'credibility'
      },
      
      // PHASE 2: COMMONALITY (25-40%)
      {
        speaker: speakerRoles.prospect,
        text: "We've been in the sales optimization space for a while too. It's been quite a journey trying to find the right tools.",
        phase: 'commonality'
      },
      {
        speaker: speakerRoles.agent,
        text: "I completely understand that journey! Many of our most successful clients went through multiple tools before finding us. It sounds like we share a similar vision for what great sales enablement should look like. Tell me, what initially got your company focused on sales optimization?",
        phase: 'commonality'
      },
      {
        speaker: speakerRoles.prospect,
        text: "We realized our sales team was our biggest asset, but also our biggest variable. Some reps were crushing it while others struggled with the same leads. We knew there had to be a better way to create consistency.",
        phase: 'commonality'
      },
      {
        speaker: speakerRoles.agent,
        text: "That resonates so much with me! That inconsistency challenge is exactly why I got passionate about this field. It's fascinating how two reps can have such different outcomes with identical opportunities. I've seen this pattern across industries - from SaaS to healthcare to financial services.",
        phase: 'commonality'
      },
      
      // PHASE 3: PROBLEM (40-70%)
      {
        speaker: speakerRoles.prospect,
        text: "Exactly! Our biggest challenge is that our reps don't get real-time feedback during calls. They only find out what went wrong after losing the deal.",
        phase: 'problem'
      },
      {
        speaker: speakerRoles.agent,
        text: "That post-mortem approach is so frustrating, isn't it? Let me dig deeper - when a rep loses a deal, how long does it typically take to identify what went wrong? And more importantly, how do you ensure the same mistakes don't happen again?",
        phase: 'problem'
      },
      {
        speaker: speakerRoles.prospect,
        text: "Honestly? Sometimes we never figure it out. Our managers listen to call recordings when they have time, which might be days or weeks later. By then, the rep has already repeated the same mistakes on other calls. It's a vicious cycle.",
        phase: 'problem'
      },
      {
        speaker: speakerRoles.agent,
        text: "That delay is costly in so many ways. Based on what you shared earlier about having 50 reps - if each rep has just 5 calls per day, that's 250 opportunities for mistakes to compound before anyone catches them. What would you estimate this inconsistency costs you in lost deals each quarter?",
        phase: 'problem'
      },
      {
        speaker: speakerRoles.prospect,
        text: "When you put it that way... we're probably losing 20-30% of winnable deals just due to execution issues. That's millions in lost revenue annually.",
        phase: 'problem'
      },
      
      // PHASE 4: SOLUTION (70-100%)
      {
        speaker: speakerRoles.agent,
        text: "Those numbers align exactly with what we see across the industry. Here's how Perswade solves this: Our AI analyzes every word in real-time, providing instant coaching through the C²PS framework. Your reps get guidance DURING the call, not days later. We've seen clients reduce those execution losses by 75% within 90 days.",
        phase: 'solution'
      },
      {
        speaker: speakerRoles.prospect,
        text: "That sounds like exactly what we need. How does the real-time guidance actually work without disrupting the conversation?",
        phase: 'solution'
      },
      {
        speaker: speakerRoles.agent,
        text: "Great question! Perswade provides subtle, non-intrusive prompts that only the rep can see. For example, if they're spending too much time on features without establishing credibility, they'll see a gentle reminder to share a relevant success story. It's like having your best sales coach whispering perfect advice in their ear, powered by AI that's analyzed millions of successful calls.",
        phase: 'solution'
      },
      {
        speaker: speakerRoles.prospect,
        text: "And this integrates with our existing CRM and call systems?",
        phase: 'solution'
      },
      {
        speaker: speakerRoles.agent,
        text: "Absolutely! Perswade integrates seamlessly with Salesforce, HubSpot, and all major CRMs. Every call is automatically logged with full transcripts, C²PS scores, and coaching insights. Your managers get dashboards showing exactly where each rep needs improvement. Implementation typically takes 5-7 days, and we handle all the technical heavy lifting. Would you like to see a live demo of how this would work for your specific sales process?",
        phase: 'solution'
      }
    ];

    let index = 0;
    
    const interval = setInterval(() => {
      if (index < demoMessages.length && isCallActive && !isLiveMode) {
        const message = demoMessages[index];
        
        // Update current phase
        if (message.phase && message.phase !== currentPhase) {
          setCurrentPhase(message.phase as 'credibility' | 'commonality' | 'problem' | 'solution');
        }
        
        const newSegment: TranscriptSegment = {
          id: `demo_${index}`,
          text: message.text,
          speaker: message.speaker,
          timestamp: new Date().toISOString(),
          confidence: 0.9 + Math.random() * 0.1,
          is_final: true,
          c2psPhase: message.phase as 'credibility' | 'commonality' | 'problem' | 'solution'
        };
        
        setTranscript(prev => [...prev, newSegment]);
        
        // Update phase and simulate analysis with delay to prevent loops
        setTimeout(() => {
          simulateAnalysis(message.text, message.phase);
        }, 10);
        
        index++;
      } else if (index >= demoMessages.length) {
        clearInterval(interval);
      }
    }, 4500); // 4.5 seconds between messages for readability

    return () => {
      clearInterval(interval);
      demoStartedRef.current = false; // Reset on cleanup
    };
  }, [isCallActive, isLiveMode, speakerRoles.agent, speakerRoles.prospect, currentPhase, simulateAnalysis, transcript.length]);

  // Enhanced startCall function with proper recording setup
  const startCall = useCallback(async () => {
    const mode = isLiveMode ? 'live' : 'demo';
    console.log(`📞 Starting ${mode} call - ${isLiveMode && realTranscription ? 'REAL AssemblyAI' : 'simulated'}...`);
    
    // Reset demo flag for new call
    demoStartedRef.current = false;
    
    setIsCallActive(true);
    setIsRecording(true);
    setTranscript([]);
    setCurrentText('');
    setC2psScores({ credibility: 0, commonality: 0, problem: 0, solution: 0 });
    setConversionProbability(0);
    setRecommendations([]);
    setCurrentPhase('credibility'); // Start with credibility phase
    setShowLiveConfig(false); // Hide config when starting
    
    if (isLiveMode) {
      console.log('🎤 Setting up real audio processing...');
      
      // Initialize REAL audio capture
      await initializeAudioCapture();
      
      // Start recording with a small delay to ensure everything is ready
      setTimeout(() => {
        if (mediaRecorder && mediaRecorder.state === 'inactive') {
          try {
            mediaRecorder.start(250); // Send chunks every 250ms for real-time processing
            console.log('🎤 Real audio recording started - sending chunks every 250ms');
          } catch (error) {
            console.error('❌ Failed to start recording:', error);
          }
        } else {
          console.warn('⚠️ MediaRecorder not ready or already active');
        }
      }, 1000); // 1 second delay to ensure everything is initialized
    }
    
    if (isConnected) {
      const success = sendMessage({
        type: 'start_call',
        data: {
          mode,
          agent_name: speakerRoles.agent,
          prospect_name: speakerRoles.prospect,
          participants: [speakerRoles.agent, speakerRoles.prospect]
        }
      });
      
      if (success) {
        console.log(`✅ Start call message sent successfully for ${mode} mode`);
      } else {
        console.error('❌ Failed to send start call message');
      }
    } else if (!isLiveMode) {
      console.warn('⚠️ Starting call in demo mode - not connected to backend');
    }
  }, [sendMessage, isConnected, isLiveMode, realTranscription, initializeAudioCapture, mediaRecorder, speakerRoles]);

  const endCall = useCallback(() => {
    console.log('📞 Ending call...');
    setIsCallActive(false);
    setIsRecording(false);
    setCurrentText('');
    
    // Reset demo started flag
    demoStartedRef.current = false;
    
    // Cleanup audio if in live mode
    if (isLiveMode) {
      cleanupAudio();
    }
    
    if (isConnected) {
      sendMessage({
        type: 'end_call'
      });
    }
  }, [sendMessage, isConnected, isLiveMode, cleanupAudio]);

  // Mode switch handler - FIXED: Replaced Switch with Button
  const handleModeSwitch = useCallback((toMode: 'demo' | 'live') => {
    if (isCallActive) {
      return; // Can't switch modes during active call
    }
    
    const isLive = toMode === 'live';
    setIsLiveMode(isLive);
    setShowLiveConfig(isLive); // Show config when switching to live mode
    
    // Reset state when switching modes
    setTranscript([]);
    setCurrentText('');
    setC2psScores({ credibility: 0, commonality: 0, problem: 0, solution: 0 });
    setConversionProbability(0);
    setRecommendations([]);
    setCurrentPhase('credibility');
    demoStartedRef.current = false; // Reset demo flag
    
    // Cleanup audio if switching away from live mode
    if (!isLive && audioStream) {
      cleanupAudio();
    }
    
    console.log(`🔄 Switched to ${toMode} mode`);
  }, [isCallActive, audioStream, cleanupAudio]);

  // Orkestra helper functions - Black & White only
  const getScoreColor = (score: number) => {
    if (score >= 7) return 'font-bold';
    if (score >= 4) return 'text-muted';
    return 'opacity-50';
  };

  const getScoreBackground = (score: number) => {
    if (score >= 7) return 'border-2 border-foreground';
    if (score >= 4) return 'border border-foreground';
    return 'border border-foreground/30';
  };

  const getSpeakerIcon = (speaker: string) => {
    if (speaker === speakerRoles.agent || speaker.includes('Agent')) {
      return <Briefcase className="h-4 w-4" />;
    }
    return <User className="h-4 w-4" />;
  };

  const getSpeakerBadge = (speaker: string) => {
    if (speaker === speakerRoles.agent || speaker.includes('Agent')) {
      return <Badge className="text-xs bg-foreground text-background border-0 px-2 py-0 font-bold uppercase">AGENT</Badge>;
    }
    return <Badge className="text-xs bg-background text-foreground border border-foreground px-2 py-0 uppercase">PROSPECT</Badge>;
  };

  const getPhaseIcon = (phase: string) => {
    switch (phase) {
      case 'credibility': return <Crown className="h-4 w-4" />;
      case 'commonality': return <Users className="h-4 w-4" />;
      case 'problem': return <Target className="h-4 w-4" />;
      case 'solution': return <Lightbulb className="h-4 w-4" />;
      default: return <ChevronRight className="h-4 w-4" />;
    }
  };

  // Don't render anything if callId is not set yet
  if (!callId) {
    return <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center">
        <Zap className="h-8 w-8 animate-pulse mx-auto mb-2" />
        <p className="text-foreground font-mono uppercase tracking-wider">INITIALIZING PERSWADE...</p>
      </div>
    </div>;
  }

  return (
    <div className="min-h-screen bg-background p-6 font-mono" suppressHydrationWarning>
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header with Mode Switcher & Real Demo Banner */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-foreground shadow-orkestra-sm">
              <Zap className="h-6 w-6 text-background" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-3xl font-bold uppercase tracking-tight">PERSWADE WATSON</h1>
                {isLiveMode && realTranscription && (
                  <Badge className="bg-foreground text-background border-0 px-2 py-0">
                    <Crown className="h-3 w-3 mr-1" />
                    PODCAST READY
                  </Badge>
                )}
              </div>
              <p className="text-muted uppercase text-sm tracking-wider">
                {isLiveMode && realTranscription 
                  ? 'LIVE AI ANALYSIS - STUDIO MODE' 
                  : 'AI-POWERED SALES VOICE AGENT - C²PS METHODOLOGY'
                }
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Dark Mode Toggle - FIXED: Replaced Switch with Button */}
            <div className="flex items-center gap-2 p-2 border-2 border-foreground shadow-orkestra-sm">
              <Sun className="h-4 w-4" />
              <Button
                variant={isDarkMode ? "default" : "outline"}
                size="sm"
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="h-6 px-2"
              >
                {isDarkMode ? 'DARK' : 'LIGHT'}
              </Button>
              <Moon className="h-4 w-4" />
            </div>
            
            {/* Mode Switcher - FIXED: Replaced Switch with Buttons */}
            <div className="flex items-center gap-3 p-3 bg-background border-2 border-foreground shadow-orkestra-sm">
              <Button
                variant={!isLiveMode ? "default" : "outline"}
                size="sm"
                onClick={() => handleModeSwitch('demo')}
                disabled={isCallActive}
                className="text-xs font-bold uppercase"
              >
                DEMO
              </Button>
              <Button
                variant={isLiveMode ? "default" : "outline"}
                size="sm"
                onClick={() => handleModeSwitch('live')}
                disabled={isCallActive}
                className="text-xs font-bold uppercase"
              >
                LIVE
              </Button>
              {isLiveMode && (
                <div className="flex items-center gap-1">
                  <Badge className="ml-2 bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                    <Radio className="h-3 w-3 mr-1" />
                    PODCAST MODE
                  </Badge>
                </div>
              )}
            </div>
            
            <div className="flex items-center gap-3">
              <Badge className={`${isConnected ? 'bg-foreground text-background' : 'bg-background text-foreground border border-foreground'} px-2 py-0 uppercase`}>
                {isConnected ? (
                  <>
                    <Wifi className="h-3 w-3 mr-1" />
                    CONNECTED
                  </>
                ) : (
                  <>
                    <WifiOff className="h-3 w-3 mr-1" />
                    {callId ? 'DISCONNECTED' : 'CONNECTING...'}
                  </>
                )}
              </Badge>
              <Badge className={`${isCallActive ? 'bg-foreground text-background' : 'bg-background text-foreground border border-foreground'} px-2 py-0 uppercase`}>
                CALL: {callId.slice(-8)}
              </Badge>
            </div>
          </div>
        </div>

        {/* C²PS Phase Indicator */}
        {isCallActive && (
          <Card className="border-2 !border-foreground shadow-orkestra bg-background">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <h3 className="font-bold uppercase mb-2">C²PS METHODOLOGY PHASE</h3>
                <div className="flex items-center gap-4">
                  {['credibility', 'commonality', 'problem', 'solution'].map((phase) => (
                    <div 
                      key={phase}
                      className={`flex items-center gap-2 px-3 py-1 border ${
                        currentPhase === phase 
                          ? 'bg-foreground text-background border-foreground' 
                          : 'border-foreground/30'
                      }`}
                    >
                      {getPhaseIcon(phase)}
                      <span className="text-xs font-bold uppercase">{phase}</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Live Configuration Panel */}
        {isLiveMode && showLiveConfig && !isCallActive && (
          <Card className="border-2 !border-foreground shadow-orkestra bg-background">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 uppercase">
                <Settings className="h-5 w-5" />
                LIVE PODCAST CONFIGURATION
                <Badge className="ml-auto bg-foreground text-background px-2 py-0 uppercase">
                  STUDIO MODE
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {/* Speaker Names */}
                <div className="space-y-2">
                  <Label className="text-xs font-bold uppercase">SALES AGENT NAME</Label>
                  <Input
                    value={speakerRoles.agent}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSpeakerRoles(prev => ({ ...prev, agent: e.target.value }))}
                    placeholder="Enter agent name"
                    className="border-foreground"
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-xs font-bold uppercase">PROSPECT NAME</Label>
                  <Input
                    value={speakerRoles.prospect}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSpeakerRoles(prev => ({ ...prev, prospect: e.target.value }))}
                    placeholder="Enter prospect name"
                    className="border-foreground"
                  />
                </div>
                
                {/* Audio Source Selection */}
                <div className="space-y-2">
                  <Label className="text-xs font-bold uppercase">AGENT AUDIO SOURCE</Label>
                  <Select 
                    value={audioSources.agentSource}
                    onValueChange={(value: string) => setAudioSources(prev => ({ ...prev, agentSource: value as 'microphone' | 'system' }))}
                  >
                    <SelectTrigger className="border-foreground">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="microphone">
                        <div className="flex items-center gap-2">
                          <Mic className="h-4 w-4" />
                          MICROPHONE
                        </div>
                      </SelectItem>
                      <SelectItem value="system">
                        <div className="flex items-center gap-2">
                          <Headphones className="h-4 w-4" />
                          SYSTEM AUDIO
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label className="text-xs font-bold uppercase">PROSPECT AUDIO SOURCE</Label>
                  <Select
                    value={audioSources.prospectSource}
                    onValueChange={(value: string) => setAudioSources(prev => ({ ...prev, prospectSource: value as 'microphone' | 'system' }))}
                  >
                    <SelectTrigger className="border-foreground">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="microphone">
                        <div className="flex items-center gap-2">
                          <Mic className="h-4 w-4" />
                          MICROPHONE
                        </div>
                      </SelectItem>
                      <SelectItem value="system">
                        <div className="flex items-center gap-2">
                          <Headphones className="h-4 w-4" />
                          SYSTEM AUDIO
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="pt-4 border-t border-foreground">
                <p className="text-sm mb-2">
                  <strong>STUDIO SETUP:</strong> Configure speaker names and audio sources for your Studio recording. 
                  Agent audio (you) typically uses microphone, while prospect audio (your friend) uses system audio from the call.
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Real Demo Instructions */}
        {isLiveMode && realTranscription && !isCallActive && (
          <Card className="border-2 !border-foreground shadow-orkestra bg-background">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <Radio className="h-5 w-5 mt-0.5" />
                <div>
                  <h3 className="font-bold uppercase mb-2">🎙️ STUDIO MODE SETUP</h3>
                  <p className="text-sm mb-3">
                    READY FOR YOUR LIVE STUDIO DEMO! FOLLOW THE C²PS METHODOLOGY:
                  </p>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <Crown className="h-4 w-4 mt-0.5" />
                      <div>
                        <strong>1. CREDIBILITY (0-25%):</strong> ESTABLISH YOUR EXPERTISE FIRST. SHARE YOUR BACKGROUND, EXPERIENCE, AND SUCCESS STORIES.
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Users className="h-4 w-4 mt-0.5" />
                      <div>
                        <strong>2. COMMONALITY (25-40%):</strong> BUILD RAPPORT. FIND SHARED EXPERIENCES AND COMMON GROUND.
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Target className="h-4 w-4 mt-0.5" />
                      <div>
                        <strong>3. PROBLEM (40-70%):</strong> DISCOVER THEIR PAIN. USE INSIGHTS FROM EARLIER PHASES TO DIG DEEP.
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <Lightbulb className="h-4 w-4 mt-0.5" />
                      <div>
                        <strong>4. SOLUTION (70-100%):</strong> PRESENT PERSWADE WATSON AS THE PERFECT FIT FOR THEIR SPECIFIC NEEDS.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Extended Demo Notice */}
        {!isLiveMode && (
          <Card className="border-2 !border-foreground shadow-orkestra bg-background">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <Play className="h-5 w-5 mt-0.5" />
                <div>
                  <h3 className="font-bold uppercase mb-2">🎬 C²PS-ALIGNED DEMO MODE</h3>
                  <p className="text-sm mb-3">
                    EXPERIENCE A PERFECTLY STRUCTURED SALES CONVERSATION FOLLOWING THE C²PS METHODOLOGY. 
                    WATCH HOW EACH PHASE BUILDS UPON THE PREVIOUS TO CREATE MAXIMUM CONVERSION IMPACT.
                  </p>
                  <div className="flex items-center gap-4 text-xs uppercase font-bold">
                    <span>✅ CREDIBILITY → COMMONALITY → PROBLEM → SOLUTION</span>
                    <span>✅ PHASE-SPECIFIC SCORING</span>
                    <span>✅ PROGRESSIVE RECOMMENDATIONS</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Call Controls - Enhanced for Real Demo */}
        <Card className="border-2 !border-foreground shadow-orkestra">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 uppercase">
              <Activity className="h-5 w-5" />
              CALL CONTROLS
              <Badge className="ml-auto bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                {isLiveMode ? '🎙️ STUDIO MODE' : '🎬 C²PS DEMO MODE'}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              {!isCallActive ? (
                <Button 
                  onClick={startCall}
                  className={`btn-orkestra flex items-center gap-2 ${isLiveMode && realTranscription ? 'glitch-hover' : ''}`}
                  size="lg"
                  disabled={isLiveMode && micPermission === 'denied'}
                >
                  {isLiveMode ? <Radio className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                  {isLiveMode 
                    ? 'START STUDIO RECORDING'
                    : 'START C²PS DEMO'
                  }
                </Button>
              ) : (
                <div className="flex gap-3">
                  <Button
                    onClick={endCall}
                    variant="destructive"
                    size="lg"
                    className="btn-orkestra flex items-center gap-2"
                  >
                    <Square className="h-4 w-4" />
                    END CALL
                  </Button>
                </div>
              )}
              
              {/* Real Audio Status */}
              {isLiveMode && isRecording && (
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-2 text-sm font-bold uppercase">
                    <div className="w-2 h-2 bg-foreground animate-pulse" />
                    🎙️ STUDIO RECORDING ACTIVE
                  </div>
                  
                  {audioLevel > 0 && (
                    <div className="flex items-center gap-2">
                      <Volume2 className="h-4 w-4" />
                      <div className="w-20 h-2 border border-foreground">
                        <div 
                          className="h-full bg-foreground transition-all duration-100"
                          style={{ width: `${Math.min(100, audioLevel)}%` }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}
              
              {/* Demo Status */}
              {!isLiveMode && isRecording && (
                <div className="flex items-center gap-2 text-sm font-bold uppercase">
                  <div className="w-2 h-2 bg-foreground animate-pulse" />
                  🎬 C²PS DEMO SESSION ACTIVE - PHASE: {currentPhase.toUpperCase()}
                </div>
              )}
              
              {/* Microphone Permission Warning */}
              {isLiveMode && micPermission === 'denied' && (
                <div className="flex items-center gap-2 text-sm font-bold uppercase bg-background border border-foreground px-3 py-2">
                  <MicOff className="h-4 w-4" />
                  MICROPHONE ACCESS DENIED. PLEASE ENABLE IN BROWSER SETTINGS.
                </div>
              )}

              {/* Connection Error Display */}
              {connectionError && (
                <div className="flex items-center gap-2 text-sm font-bold uppercase bg-background border border-foreground px-3 py-2">
                  <WifiOff className="h-4 w-4" />
                  {connectionError.toUpperCase()}
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column - Transcript */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Live Transcript */}
            <Card className="h-96 border-2 !border-foreground shadow-orkestra">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 uppercase">
                  <Users className="h-5 w-5" />
                  LIVE TRANSCRIPT
                  {isCallActive && (
                    <Badge className="ml-auto bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                      <div className="w-2 h-2 bg-foreground animate-pulse mr-1" />
                      {isLiveMode ? '🎙️ STUDIO' : '🎬 C²PS DEMO'}
                    </Badge>
                  )}
                </CardTitle>
              </CardHeader>
              
              <CardContent className="h-80 p-0">
                <ScrollArea className="h-full px-4">
                  <div className="space-y-3 pb-4">
                    {transcript.map((segment) => {
                      const isAgent = segment.speaker === speakerRoles.agent || segment.speaker.includes('Agent');
                      
                      return (
                        <div
                          key={segment.id}
                          className={`flex gap-3 p-3 ${
                            isAgent
                              ? 'border-l-4 border-foreground shadow-orkestra-sm' 
                              : 'border-l-2 border-foreground/50'
                          }`}
                        >
                          <div className="flex-shrink-0">
                            <div className={`w-8 h-8 flex items-center justify-center text-background text-sm font-bold ${
                              isAgent ? 'bg-foreground' : 'bg-foreground/70'
                            }`}>
                              {getSpeakerIcon(segment.speaker)}
                            </div>
                          </div>
                          
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="text-sm font-bold uppercase">
                                {segment.speaker}
                              </span>
                              {getSpeakerBadge(segment.speaker)}
                              {segment.c2psPhase && (
                                <Badge className="text-xs bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                                  {getPhaseIcon(segment.c2psPhase)}
                                  {segment.c2psPhase}
                                </Badge>
                              )}
                              <Badge 
                                className={`text-xs bg-background text-foreground border border-foreground px-2 py-0 ${getScoreColor(segment.confidence * 10)}`}
                              >
                                {Math.round(segment.confidence * 100)}%
                              </Badge>
                            </div>
                            
                            <p className="text-sm leading-relaxed">
                              {segment.text}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                    
                    {currentText && (
                      <div className="flex gap-3 p-3 border-l-2 border-foreground/30 opacity-75">
                        <div className="w-8 h-8 bg-foreground/50 flex items-center justify-center text-background text-sm font-bold">
                          ...
                        </div>
                        <div className="flex-1">
                          <p className="text-sm italic">{currentText}</p>
                        </div>
                      </div>
                    )}
                    
                    {transcript.length === 0 && !currentText && (
                      <div className="text-center py-12">
                        <Users className="h-12 w-12 mx-auto mb-3 opacity-50" />
                        <p className="text-lg font-bold uppercase">READY FOR CONVERSATION...</p>
                        <p className="text-sm mt-1 uppercase">
                          {isLiveMode 
                            ? 'START YOUR STUDIO RECORDING - FOLLOW THE C²PS METHODOLOGY FOR MAXIMUM IMPACT!'
                            : 'START THE DEMO TO SEE THE C²PS METHODOLOGY IN ACTION'
                          }
                        </p>
                      </div>
                    )}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* Live Guidance */}
            <Card className="border-2 !border-foreground shadow-orkestra">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 uppercase">
                  <Lightbulb className="h-5 w-5" />
                  LIVE GUIDANCE
                  {currentPhase && (
                    <Badge className="ml-auto bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                      PHASE: {currentPhase}
                    </Badge>
                  )}
                </CardTitle>
              </CardHeader>
              
              <CardContent>
                {recommendations.length > 0 ? (
                  <div className="space-y-3">
                    {recommendations.map((rec, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 border-2 border-foreground shadow-orkestra-sm">
                        <Lightbulb className="h-5 w-5 mt-0.5 flex-shrink-0" />
                        <p className="text-sm font-bold uppercase">{rec}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-6">
                    <Lightbulb className="h-8 w-8 mx-auto mb-2 opacity-50" />
                    <p className="uppercase font-bold">NO GUIDANCE RECOMMENDATIONS YET</p>
                    <p className="text-xs mt-1 uppercase">
                      {isLiveMode && realTranscription 
                        ? 'REAL-TIME C²PS SUGGESTIONS WILL APPEAR AS YOU PROGRESS THROUGH EACH PHASE'
                        : 'PHASE-SPECIFIC GUIDANCE WILL APPEAR AS THE CONVERSATION DEVELOPS'
                      }
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Analytics */}
          <div className="space-y-6">
            
            {/* Conversion Probability */}
            <Card className="border-2 !border-foreground shadow-orkestra">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 uppercase">
                  <Target className="h-5 w-5" />
                  CONVERSION PROBABILITY
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-4xl font-bold mb-2">
                    {conversionProbability}%
                  </div>
                  <div className="w-full h-3 border-2 border-foreground">
                    <div 
                      className="h-full bg-foreground transition-all duration-300"
                      style={{ width: `${conversionProbability}%` }}
                    />
                  </div>
                </div>
                
                <div className="text-center text-sm font-bold uppercase">
                  {conversionProbability >= 70 ? '🎯 HIGH PROBABILITY' : 
                   conversionProbability >= 40 ? '⚡ MODERATE PROBABILITY' : 
                   '📈 BUILDING MOMENTUM'}
                </div>
                
                {isLiveMode && realTranscription && (
                  <div className="text-center">
                    <Badge className="bg-foreground text-background px-2 py-0 uppercase">
                      LIVE ANALYSIS
                    </Badge>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* C²PS Scores */}
            <Card className="border-2 !border-foreground shadow-orkestra">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 uppercase">
                  <BarChart3 className="h-5 w-5" />
                  C²PS ANALYSIS
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {Object.entries(c2psScores).map(([pillar, score]) => (
                  <div key={pillar} className={`p-3 ${getScoreBackground(score)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold uppercase">{pillar}</span>
                        {score >= 7 && <CheckCircle className="h-4 w-4" />}
                      </div>
                      <span className={`text-sm font-bold ${getScoreColor(score)}`}>
                        {score.toFixed(1)}/10
                      </span>
                    </div>
                    <div className="h-2 border border-foreground">
                      <div 
                        className="h-full bg-foreground transition-all duration-300"
                        style={{ width: `${score * 10}%` }}
                      />
                    </div>
                  </div>
                ))}
                
                <Separator className="bg-foreground" />
                
                <div className="text-xs space-y-1 uppercase">
                  <p><strong>CREDIBILITY:</strong> AUTHORITY & EXPERTISE SIGNALS</p>
                  <p><strong>COMMONALITY:</strong> RAPPORT & AGREEMENT BUILDING</p>
                  <p><strong>PROBLEM:</strong> PAIN POINT IDENTIFICATION</p>
                  <p><strong>SOLUTION:</strong> VALUE PROPOSITION DELIVERY</p>
                </div>
                
                {isLiveMode && realTranscription && (
                  <div className="pt-2 border-t border-foreground">
                    <Badge className="bg-foreground text-background text-xs px-2 py-0 uppercase">
                      REAL-TIME C²PS METHODOLOGY
                    </Badge>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Call Metrics */}
            <Card className="border-2 !border-foreground shadow-orkestra">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 uppercase">
                  <TrendingUp className="h-5 w-5" />
                  CALL METRICS
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="uppercase font-bold">DURATION</span>
                  <span className="font-bold">
                    {isCallActive ? `${Math.floor((transcript.length * 4.5) / 60)}:${String(Math.round((transcript.length * 4.5) % 60)).padStart(2, '0')}` : '0:00'}
                  </span>
                </div>
                
                <div className="flex justify-between text-sm">
                  <span className="uppercase font-bold">EXCHANGES</span>
                  <span className="font-bold">{transcript.length}</span>
                </div>
                
                <div className="flex justify-between text-sm">
                  <span className="uppercase font-bold">CURRENT PHASE</span>
                  <Badge className="bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                    {currentPhase}
                  </Badge>
                </div>
                
                <div className="flex justify-between text-sm">
                  <span className="uppercase font-bold">MODE</span>
                  <Badge className={`${isLiveMode ? 'bg-foreground text-background' : 'bg-background text-foreground border border-foreground'} px-2 py-0 uppercase`}>
                    {isLiveMode ? '🎙️ STUDIO' : '🎬 C²PS DEMO'}
                  </Badge>
                </div>
                
                <div className="flex justify-between text-sm">
                  <span className="uppercase font-bold">CONNECTION</span>
                  <Badge className={`${isConnected ? 'bg-foreground text-background' : 'bg-background text-foreground border border-foreground'} px-2 py-0 uppercase`}>
                    {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
                  </Badge>
                </div>
                
                {isLiveMode && audioLevel > 0 && (
                  <div className="flex justify-between text-sm">
                    <span className="uppercase font-bold">AUDIO LEVEL</span>
                    <span className="font-bold">{Math.round(audioLevel)}%</span>
                  </div>
                )}
                
                {isLiveMode && (
                  <>
                    <Separator className="bg-foreground" />
                    <div className="space-y-2 text-xs">
                      <div className="flex justify-between">
                        <span className="uppercase font-bold">{speakerRoles.agent} SOURCE</span>
                        <Badge className="bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                          {audioSources.agentSource === 'microphone' ? (
                            <><Mic className="h-3 w-3 mr-1 inline" />MIC</>
                          ) : (
                            <><Headphones className="h-3 w-3 mr-1 inline" />SYSTEM</>
                          )}
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="uppercase font-bold">{speakerRoles.prospect} SOURCE</span>
                        <Badge className="bg-background text-foreground border border-foreground px-2 py-0 uppercase">
                          {audioSources.prospectSource === 'microphone' ? (
                            <><Mic className="h-3 w-3 mr-1 inline" />MIC</>
                          ) : (
                            <><Headphones className="h-3 w-3 mr-1 inline" />SYSTEM</>
                          )}
                        </Badge>
                      </div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm uppercase">
          <p className="font-bold">PERSWADE WATSON V1.0.0 • C²PS METHODOLOGY FOR SALES EXCELLENCE</p>
          <p className="mt-1 text-muted">
            {isLiveMode && realTranscription 
              ? 'STUDIO MODE • POWERED BY ASSEMBLYAI & C²PS'
              : 'POWERED BY ASSEMBLYAI UNIVERSAL-STREAMING & C²PS METHODOLOGY'
            }
          </p>
          <p className="mt-2 font-bold">ORCHESTRATED BY ORKESTRA 🔥</p>
        </div>
      </div>
    </div>
  );
};

export default PerswadeDashboard;