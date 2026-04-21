export interface AgentConfig {
  id: string;
  name: string;
  description: string;
  baseUrl: string;
  port: number;
  icon: string;
  examplePrompts: string[];
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  thinking?: string;
  timestamp: Date;
  streaming?: boolean;
  toolCalls?: string[];
}
