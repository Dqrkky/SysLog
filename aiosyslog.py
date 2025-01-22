import asyncio

class SysLogStart:
    def __init__(self, host :str=None, port :int=None):
        self.host :str=host
        self.port :int=port

class SysLogStop:
    def __init__(self):
        pass

class SysLogMessage:
    def __init__(self, message :bytes=None, addr :tuple=None):
        self.message :bytes=message
        self.addr :tuple=addr

class SysLogConnection:
    def __init__(self, transport=None):
        self.transport = transport

class SysLogConnectionLost:
    def __init__(self, exc=None):
        self.exc=exc

class SysLogError:
    def __init__(self, exc=None):
        self.exc=exc

class SysLogPauseWriting:
    def __init__(self):
        pass

class SysLogResumeWriting:
    def __init__(self):
        pass

class SysLogServer:
    def __init__(self, host :str="0.0.0.0", port=514):
        self.config = {
            "host": host if host != None and isinstance(host, str) else None,  # noqa: E711
            "port": port if port != None and isinstance(port, int) else None  # noqa: E711
        }
        self.event_handlers = {}
    def event(self, event_type=None):
        return self._register_event(event_type=event_type)
    def _register_event(self, event_type=None):
        return self.decorator(event_type) if event_type else self.decorator
    def decorator(self, event_type=None):
        if event_type.__name__ not in self.event_handlers:
            self.event_handlers[event_type.__name__] = event_type
        return event_type
    async def trigger_event(self, event_name=None, event_data=None):
        if event_name in self.event_handlers:
            await self.event_handlers[event_name](event_data)
    async def start(self):
        if hasattr(self, "config") and self.config != None and isinstance(self.config, dict) and \
        "host" in self.config and self.config["host"] != None and \
        "port" in self.config and self.config["port"] != None:  # noqa: E711
            loop = asyncio.get_running_loop()
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: SyslogServerProtocol(self),
                local_addr=(
                    self.config["host"],
                    self.config["port"]
                )
            )
            try:
                await self.trigger_event("on_start", SysLogStart(
                    host=self.config["host"],
                    port=self.config["port"]
                ))
                await asyncio.Future()
            except KeyboardInterrupt:
                await self.trigger_event("on_stop", SysLogStop())
            finally:
                transport.close()
    def run(self):
        asyncio.run(self.start())

class SyslogServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, server :SysLogServer=None):
        self.server :SysLogServer=server
        self.transport :asyncio.proactor_events._ProactorDatagramTransport= None
    def connection_made(self, transport :asyncio.proactor_events._ProactorDatagramTransport=None):
        self.transport :asyncio.proactor_events._ProactorDatagramTransport=transport
        asyncio.create_task(self.server.trigger_event("on_connection", SysLogConnection(transport=transport)))
    def datagram_received(self, data :bytes=None, addr :tuple=None):
        asyncio.create_task(self.server.trigger_event("on_message", SysLogMessage(message=data,addr=addr)))
    def error_received(self, exc):
        print(type(exc))
        asyncio.create_task(self.server.trigger_event("on_error", SysLogError(exc=exc)))
    def connection_lost(self, exc):
        asyncio.create_task(self.server.trigger_event("on_connection_lost", SysLogConnectionLost(exc=exc)))
    def pause_writing(self):
        asyncio.create_task(self.server.trigger_event("on_pause_writing", SysLogPauseWriting()))
    def resume_writing(self):
        asyncio.create_task(self.server.trigger_event("on_resume_writing", SysLogResumeWriting()))