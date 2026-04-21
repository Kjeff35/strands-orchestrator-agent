import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AgentService } from '../../services/agent.service';
import { AgentConfig } from '../../models/agent.model';

@Component({
  selector: 'app-agent-selector',
  standalone: true,
  templateUrl: './agent-selector.html',
  styleUrl: './agent-selector.css',
})
export class AgentSelectorComponent {
  agents: AgentConfig[];

  constructor(private agentService: AgentService, private router: Router) {
    this.agents = this.agentService.getAgents();
  }

  select(agent: AgentConfig): void {
    this.router.navigate(['/chat', agent.id]);
  }
}
