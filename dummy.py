import aiosyslog
import json

client = aiosyslog.SysLogServer()

@client.event
async def on_start(ctx :aiosyslog.SysLogStart):
    print(f"Server Started: {ctx.__dict__}")

@client.event
async def on_stop(ctx :aiosyslog.SysLogStop):
    print(f"Server Stoped: {ctx.__dict__}")

@client.event
async def on_message(ctx :aiosyslog.SysLogMessage):
    # Decode message
    message = ctx.message.decode("Latin1")
    # Find when the header ends
    # or when the json starts
    jsi = message.find('{')
    # Create dictionary 'data'
    # and decode nginx data/json
    data = {
        "headers": message[:jsi],
        "data": json.loads(s=message[jsi:])
    }
    print(data)

@client.event
async def on_connection(ctx :aiosyslog.SysLogConnection):
    print(f"Connection: {ctx.__dict__}")

@client.event
async def on_connection_lost(ctx :aiosyslog.SysLogConnectionLost):
    print(f"Connection Error: {ctx.__dict__}")

@client.event
async def on_error(ctx :aiosyslog.SysLogError):
    print(f"Error: {ctx.__dict__}")

@client.event
async def on_pause_writing(ctx :aiosyslog.SysLogPauseWriting):
    print(f"Pause Writing: {ctx.__dict__}")

@client.event
async def on_resume_writing(ctx :aiosyslog.SysLogResumeWriting):
    print(f"Pause Writing: {ctx.__dict__}")

client.run()