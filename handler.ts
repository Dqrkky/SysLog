type EventCallback = (...args: any[]) => void;

interface EventHandlerInterface  {
    on(event_name :string, callback: EventCallback) : void;
    emit(event_name :string, ...args: any[]) : void;
    removeListener(event_name :string, callback: EventCallback) : void;
    removeAllListener(event_name :string) : void;
}

class EventHandler implements EventHandlerInterface {
    private events: Record<string, EventCallback[]> = {};
    on(event_name :string | undefined=undefined, callback: EventCallback) : void {
        if (!event_name) {
            throw new Error("Event name is required!");
        };
        if (!this.events[event_name]) {
            this.events[event_name] = [];
        };
        this.events[event_name].push(callback);
    };
    emit(event_name :string | undefined=undefined, ...args: any[]) :void {
        if (!event_name) {
            throw new Error("Event name is required!");
        };
        const listeners = this.events[event_name];
        if (!listeners || listeners.length === 0) {
            console.warn(`No listeners for event : ${event_name}`);
            return;
        };
        listeners.forEach((callback) => callback(...args));
    };
    removeListener(event_name :string | undefined=undefined, callback: EventCallback) : void {
        if (!event_name) {
            throw new Error("Event name is required!");
        };
        const listeners = this.events[event_name];
        if (!listeners) return;
        this.events[event_name] = listeners.filter((callback1) => callback1 !== callback);
    };
    removeAllListener(event_name :string | undefined=undefined) : void {
        if (!event_name) {
            throw new Error("Event name is required!");
        };
        const listeners = this.events[event_name];
        if (!listeners) return;
        this.events[event_name] = [];
    };
}

export default {
    EventHandler
};