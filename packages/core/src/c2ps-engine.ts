/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 */

export interface C2PSScore {
  credibility: number;
  commonality: number;
  problem: number;
  solution: number;
  overall: number;
  conversionProbability: number;
}

export class C2PSEngine {
  analyzeTranscript(transcript: string): C2PSScore {
    // Implement C²PS analysis logic
    const credibility = this.analyzeCredibility(transcript);
    const commonality = this.analyzeCommonality(transcript);
    const problem = this.analyzeProblem(transcript);
    const solution = this.analyzeSolution(transcript);
    
    const overall = (credibility + commonality + problem + solution) / 4;
    const conversionProbability = this.predictConversion(overall);
    
    return {
      credibility,
      commonality,
      problem,
      solution,
      overall,
      conversionProbability
    };
  }

  private analyzeCredibility(text: string): number {
    // Authority markers detection
    const authorityMarkers = [
      'research shows', 'studies indicate', 'data suggests',
      'in my experience', 'we\'ve helped', 'our clients'
    ];
    
    let score = 5; // baseline
    authorityMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private analyzeCommonality(text: string): number {
    // Rapport and alignment detection
    const rapportMarkers = [
      'I understand', 'absolutely', 'exactly right',
      'great point', 'I agree', 'similar situation'
    ];
    
    let score = 5;
    rapportMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private analyzeProblem(text: string): number {
    // Pain point extraction
    const painMarkers = [
      'challenge', 'issue', 'problem', 'struggle',
      'difficult', 'frustrating', 'pain point', 'bottleneck'
    ];
    
    let score = 5;
    painMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private analyzeSolution(text: string): number {
    // Value proposition matching
    const valueMarkers = [
      'solution', 'benefit', 'improve', 'increase',
      'reduce', 'save', 'optimize', 'transform'
    ];
    
    let score = 5;
    valueMarkers.forEach(marker => {
      if (text.toLowerCase().includes(marker)) score += 0.5;
    });
    
    return Math.min(10, score);
  }

  private predictConversion(overallScore: number): number {
    // Simple logistic function for conversion probability
    return 1 / (1 + Math.exp(-0.5 * (overallScore - 5)));
  }
}
