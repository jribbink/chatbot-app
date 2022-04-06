import { ipcMain, BrowserWindow } from "electron";
import { AgentIPC } from "../agent/agent-ipc";
import { IPCMessage } from "../../../shared/ipc-message";

export class RendererIPC {
    agent: AgentIPC
    mainWindow: BrowserWindow | null
    windowLoaded = false

    constructor(agent: AgentIPC, mainWindow: BrowserWindow | null) {
        mainWindow!.webContents.once('did-finish-load', () => {
            this.windowLoaded = true
        })

        this.agent = agent
        this.mainWindow = mainWindow
        if(this.agent.ws) {
            this.connectedToPython()
        } else {
            this.agent.readyCallback = this.connectedToPython.bind(this)
        }
    }

    connectedToPython() {
        if(this.windowLoaded) {
            this.mainWindow!.webContents.send('python-ready')
        } else {
            this.mainWindow!.webContents.once('did-finish-load', () => {
                this.mainWindow!.webContents.send('python-ready')
            })
        }
    }

    init() {
        ipcMain.on('agent-ipc', async (event, message: IPCMessage) => {
            message = new IPCMessage(message.type, message.body, message.id)
            this.relayMessage(event, message)
        });
    }

    relayMessage(event: any, message: IPCMessage) {
        // relay ipc message to python
        this.agent.send(message, (response: IPCMessage) => {
            event.reply('agent-ipc', response.body)
        })
    }
}