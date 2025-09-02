/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 */

import { AssemblyAI, RealtimeTranscriber } from 'assemblyai';

export class TranscriptionService {
  private client: AssemblyAI;
  private transcriber?: RealtimeTranscriber;

  constructor(apiKey: string) {
    this.client = new AssemblyAI({ apiKey });
  }

  async startRealtimeTranscription(
    onPartialTranscript: (text: string) => void,
    onFinalTranscript: (text: string) => void
  ) {
    this.transcriber = this.client.realtime.transcriber({
      sampleRate: 16000,
      wordBoost: ['C2PS', 'credibility', 'commonality', 'problem', 'solution'],
    });

    this.transcriber.on('PartialTranscript', (transcript) => {
      onPartialTranscript(transcript.text);
    });

    this.transcriber.on('FinalTranscript', (transcript) => {
      onFinalTranscript(transcript.text);
    });

    await this.transcriber.connect();
  }

  async stopTranscription() {
    await this.transcriber?.close();
  }
}
