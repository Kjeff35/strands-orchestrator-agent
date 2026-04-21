import { Routes } from '@angular/router';
import { AgentSelectorComponent } from './components/agent-selector/agent-selector';
import { ChatComponent } from './components/chat/chat';

export const routes: Routes = [
  { path: '', component: AgentSelectorComponent },
  { path: 'chat/:agentId', component: ChatComponent },
  { path: '**', redirectTo: '' },
];
