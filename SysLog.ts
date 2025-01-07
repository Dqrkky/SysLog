//import * as net from "net";
import handler from './handler';

const handle = new handler.EventHandler();

handle.on("data", (args) => {
    console.log(args);
});

handle.on("error", (error) => {
    console.log(error);
});

handle.emit("data", []);