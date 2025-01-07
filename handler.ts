type EventCallback = (...args: any[]) => void;

class EventHandler {
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
}

export default {
    EventHandler
};