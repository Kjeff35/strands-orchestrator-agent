import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Subscription } from 'rxjs';
import { marked } from 'marked';
import { AgentService } from '../../services/agent.service';
import { AgentConfig, ChatMessage } from '../../models/agent.model';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class ChatComponent implements OnInit, OnDestroy, AfterViewChecked {
  @ViewChild('messageList') messageList!: ElementRef<HTMLDivElement>;

  agent: AgentConfig | undefined;
  messages: ChatMessage[] = [];
  input = '';
  streaming = false;
  sessionId = crypto.randomUUID();

  private streamSub: Subscription | null = null;
  private shouldScroll = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agentService: AgentService,
    private sanitizer: DomSanitizer,
  ) {}

  renderMarkdown(content: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(marked.parse(content) as string);
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('agentId') ?? '';
    this.agent = this.agentService.getAgent(id);
    if (!this.agent) this.router.navigate(['/']);
  }

  ngOnDestroy(): void {
    this.streamSub?.unsubscribe();
  }

  ngAfterViewChecked(): void {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  send(): void {
    const text = this.input.trim();
    if (!text || this.streaming || !this.agent) return;

    this.messages.push({ role: 'user', content: text, timestamp: new Date() });
    this.input = '';
    this.streaming = true;
    this.shouldScroll = true;

    const assistantMsg: ChatMessage = { role: 'assistant', content: '', timestamp: new Date(), streaming: true };
    this.messages.push(assistantMsg);

    const thinkingParts: string[] = [];
    let currentPart = '';
    let toolStarted = false;

    this.streamSub = this.agentService.stream(this.agent, this.sessionId, text).subscribe({
      next: (event) => {
        const toolName = this.agentService.extractToolName(event);
        if (toolName) {
          assistantMsg.toolCalls = [...(assistantMsg.toolCalls ?? []), toolName];
          if (currentPart.trim()) {
            thinkingParts.push(currentPart.trim());
          }
          toolStarted = true;
          currentPart = '';
          this.shouldScroll = true;
        }
        const chunk = this.agentService.extractText(event);
        if (chunk) {
          currentPart += chunk;
          // Show all narration text in thinking immediately as it streams
          assistantMsg.thinking = [...thinkingParts, currentPart.trim()].filter(Boolean).join(' ') || undefined;
          this.shouldScroll = true;
        }
        if (event?.error) {
          assistantMsg.content = `Error: ${event.error}`;
          assistantMsg.streaming = false;
          this.streaming = false;
        }
      },
      error: (err) => {
        assistantMsg.content = `Connection error: ${err.message}`;
        assistantMsg.streaming = false;
        this.streaming = false;
      },
      complete: () => {
        if (toolStarted && currentPart.trim()) {
          // Final response after all tools → content (markdown)
          assistantMsg.content = currentPart;
          // Thinking shows only narration parts, not the final response
          assistantMsg.thinking = thinkingParts.join(' ') || undefined;
        } else if (!toolStarted) {
          // No tools used — direct response, no thinking section needed
          assistantMsg.content = currentPart;
          assistantMsg.thinking = undefined;
        }
        assistantMsg.streaming = false;
        this.streaming = false;
        this.shouldScroll = true;
      },
    });
  }

  usePrompt(prompt: string): void {
    this.input = prompt;
  }

  back(): void {
    this.streamSub?.unsubscribe();
    this.router.navigate(['/']);
  }

  private scrollToBottom(): void {
    const el = this.messageList?.nativeElement;
    if (el) el.scrollTop = el.scrollHeight;
  }
}
