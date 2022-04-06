import { spawn } from 'child_process'
import { v4 as uuidv4 } from 'uuid'
import commandExists from 'command-exists'
import os from 'os'
import path from 'path'
import { IPCMessage, IPCMessageType } from '../../../shared/ipc-message'
import WebSocket from 'ws'
import http from 'http'

export class AgentIPC {
    ws?: WebSocket
    callbackTable: {[id: string]: (response: IPCMessage) => void | boolean} = {}
    agentPath: string
    readyCallback = () => {}

    constructor(agentPath: string) {
        this.agentPath = agentPath
    }

    async spawnPython(address: string) {
        let pythonPath
        if(process.env.PYTHON_PATH && process.env.PYTHON_PATH != "") {
            pythonPath = process.env.PYTHON_PATH
        } else if(await commandExists('python3')) {
            console.log("PYTHON_PATH environment variable not provided... trying 'python3'")
            pythonPath = 'python3'
        } else if(await commandExists('python')) {
            console.log("'python3' not found in PATH... trying 'python'")
            pythonPath = 'python'
        } else {
            throw new Error('Python was not found in $PATH!  Please check that python3 is installed')
        }

        const botScript = spawn(pythonPath, [this.agentPath, address])
        botScript.stdout?.on("data", (data: Buffer) => {
            console.log("[Python3] " + data.toString('utf-8'))
        })
        botScript.stderr.on("data", (data: Buffer) => {
            console.log("[Python3] " + data.toString('utf-8'))
        })
    }

    async spawn(path_r = uuidv4(), path_w = uuidv4()) {
        path_r = path.resolve(os.tmpdir(), path_r)
        path_w = path.resolve(os.tmpdir(), path_w)

        const wss = new WebSocket.Server({noServer: true})
        const server = http.createServer()

        wss.on('connection', (ws) => {
            this.ws = ws
            this.readyCallback()
            ws.on("message", (data) => {
                this.processMessage(JSON.parse(data.toString()))
            })
        })

        server.on('upgrade', function upgrade(request, socket, head) {
            wss.handleUpgrade(request, socket, head, function done(ws) {
                wss.emit('connection', ws, request);
            });
        });

        server.listen(0, '127.0.0.1', () => {
            const addressRaw = server.address()
            const address: string = <string>((addressRaw instanceof String)
                ? addressRaw
                : `ws://${(addressRaw as any).address}:${(addressRaw as any).port}`)

            this.spawnPython(address)
        })
    }

    sendMessage<MessageBodyType = any>(type: IPCMessageType, body?: MessageBodyType, responseCallback?: (response: IPCMessage) => void | boolean, id?: string) {
        const message = new IPCMessage<MessageBodyType>(type, body, id)
        this.send(message, responseCallback)
    }

    send<MessageBodyType = any>(message: IPCMessage<MessageBodyType>, responseCallback?: (response: IPCMessage) => void | boolean) {
        if(responseCallback) this.callbackTable[message.id] = responseCallback
        this.ws?.send(JSON.stringify(message))
    }

    private processMessage(message: IPCMessage) {
        if (message.id in this.callbackTable) {
            const resp = this.callbackTable[message.id](message)
            if(!resp) delete this.callbackTable[message.id]
        } else {
            switch(message.type) {
                case IPCMessageType.AGENT_RESPONSE:
                    console.log(message.body!)
            }
        }
    }
}