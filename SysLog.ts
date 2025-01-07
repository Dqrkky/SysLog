import * as net from "net";
import handler from './handler';


class TcpClient {
    private client: net.Socket;
    handler: handler.EventHandler;
    constructor(private host: string | undefined=undefined, private port : number | undefined = undefined) {
        this.client = new net.Socket();
        this.handler = new handler.EventHandler();
    };
    connect() : void {
        if (!this.host) {
            throw new Error("Host is required!");
        };
        if (!this.port) {
            throw new Error("Port is required!");
        }
        this.client.connect(
            {
                host: this.host,
                port: this.port
            },
            () => {
                this.handler.emit("connect", {this.host, this.port})
            }
        )
    }
}