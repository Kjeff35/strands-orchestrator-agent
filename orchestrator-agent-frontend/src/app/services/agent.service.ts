import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AgentConfig } from '../models/agent.model';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AgentService {
  private readonly agents: AgentConfig[] = [
    {
      id: 'content_production',
      name: 'Content Production',
      description: 'Researches a topic, extracts insights, then writes polished content.',
      baseUrl: environment.agents.content_production,
      port: 8000,
      icon: '✍️',
      examplePrompts: [
        'Write an article about how multi-agent AI systems are changing software development',
        'Explain the key differences between RAG and fine-tuning for LLM applications',
        'Summarise the current state of quantum computing for a non-technical audience',
      ],
    },
    {
      id: 'travel_planner',
      name: 'Travel Planner',
      description: 'Researches your destination, builds an itinerary, and suggests gear.',
      baseUrl: environment.agents.travel_planner,
      port: 8010,
      icon: '✈️',
      examplePrompts: [
        'Plan a 10-day hiking trip to Patagonia in November for an intermediate hiker',
        'Weekend city break to Tokyo in March, first time in Japan, food and photography',
        'Two-week family holiday in Costa Rica with kids aged 8 and 11',
      ],
    },
    {
      id: 'customer_support',
      name: 'Customer Support',
      description: 'Triages your issue, resolves it, and drafts a clear response or escalation.',
      baseUrl: environment.agents.customer_support,
      port: 8020,
      icon: '🎧',
      examplePrompts: [
        'I was charged twice for my subscription this month and need a refund',
        "I can't log into my account — password reset isn't working",
        'What is your cancellation policy?',
      ],
    },
  ];

  private userId: string;

  constructor() {
    this.userId = sessionStorage.getItem('user_id') ?? crypto.randomUUID();
    sessionStorage.setItem('user_id', this.userId);
  }

  getAgents(): AgentConfig[] {
    return this.agents;
  }

  getAgent(id: string): AgentConfig | undefined {
    return this.agents.find((a) => a.id === id);
  }

  getUserId(): string {
    return this.userId;
  }

  stream(agent: AgentConfig, sessionId: string, message: string): Observable<any> {
    const payload = {
      user_id: this.userId,
      session_id: sessionId,
      prompt: message,
    };

    return new Observable((observer) => {
      const controller = new AbortController();

      fetch(`${agent.baseUrl}/invocations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal,
      })
        .then((response) => {
          if (!response.ok) {
            observer.error(new Error(`HTTP ${response.status}`));
            return;
          }
          const reader = response.body!.getReader();
          const decoder = new TextDecoder();

          const pump = (): void => {
            reader.read().then(({ done, value }) => {
              if (done) {
                observer.complete();
                return;
              }
              const text = decoder.decode(value, { stream: true });
              for (const line of text.split('\n')) {
                const trimmed = line.trim();
                if (!trimmed) continue;
                const jsonStr = trimmed.startsWith('data: ')
                  ? trimmed.slice(6)
                  : trimmed;
                try {
                  observer.next(JSON.parse(jsonStr));
                } catch {}
              }
              pump();
            });
          };
          pump();
        })
        .catch((err) => {
          if (err.name !== 'AbortError') observer.error(err);
        });

      return () => controller.abort();
    });
  }

  extractToolName(event: any): string | null {
    return event?.tool_use?.name ?? null;
  }

  extractText(event: any): string | null {
    return event?.event?.contentBlockDelta?.delta?.text ?? null;
  }
}
