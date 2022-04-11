import Message from 'renderer/models/message';
import { Service } from '../models/service';
import * as Vue from 'vue';
import { ChatState } from 'renderer/store/modules/chat';
import { IPCMessage, IPCMessageType } from 'shared/ipc-message';

export class ChatService extends Service {
  messagesWaiting: { message: string; delay: number }[] = [];

  constructor(app: Vue.App) {
    super(app);
    this.receiveMessageDelay(
      'Hi, I am your virtual care consultant.  How can I help you today?'
    );

    window.electron.ipcRenderer.pythonLoadedCallback(() => {
      this.state.connected = true
    })
  }

  sendMessage(message: string) {
    this.addMessage(new Message(new Date(), this.state.self!!, message));
    window.electron.ipcRenderer.agentIPC(
      new IPCMessage(IPCMessageType.AGENT_QUERY, message),
      (event: any, message: any) => {
        this.receiveMessageDelay(message);
      }
    );
  }

  receiveMessageDelay(message: string, delay: number = 1000) {
    if (!this.state.recipient) return;

    this.messagesWaiting.push(...message.split("\n").map(message => ({message, delay})));

    const sendNextMessage = () => {
      if (this.messagesWaiting.length > 0) {
        this.state.recipient!!.typing = true;
        setTimeout(() => {
          this.addMessage(
            new Message(
              new Date(),
              this.state.recipient!!,
              this.messagesWaiting.shift()!!.message
            )
          );
          this.state.recipient!!.typing = false;
          sendNextMessage();
        }, delay);
      }
    };
    if (this.messagesWaiting.length > 0) sendNextMessage();
  }

  private addMessage(message: Message) {
    this.state.messages.push(message);
  }

  get messages() {
    return this.state.messages;
  }

  get state(): ChatState {
    return this.store.state['chat'];
  }
}
