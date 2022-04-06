import Message from 'renderer/models/message';
import { User } from 'renderer/models/user';
import { Module } from 'vuex';
import doctorPhoto from 'assets/doctor.jpg';

export interface ChatState {
  messages: Message[];
  recipient?: User;
  self?: User;
  connected: boolean
}

export const ChatModule: Module<ChatState, any> = {
  state: {
    messages: [],
    recipient: new User('Doctor Phil (MD)', doctorPhoto),
    self: new User('You'),
    connected: false
  },
  getters: {
    isConnected(state) {
      return state.connected
    }
  }
};
