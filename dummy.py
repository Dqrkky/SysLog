import aiosyslog
import json
import os

client = aiosyslog.SysLogServer()

def printJson(js0n :dict=None):
    if js0n != None and isinstance(js0n, dict):  # noqa: E711
        os.system("cls")
        print(json.dumps(
            obj=js0n,
            indent=4
        ))

@client.event
async def on_start(ctx :aiosyslog.SysLogStart):
    printJson({"SysLogStart": ctx.__dict__})

@client.event
async def on_stop(ctx :aiosyslog.SysLogStop):
    printJson({"SysLogStop": ctx.__dict__})

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
    printJson({"SysLogMessage": data})

@client.event
async def on_connection(ctx :aiosyslog.SysLogConnection):
    printJson({"SysLogConnection": ctx.__dict__})

@client.event
async def on_connection_lost(ctx :aiosyslog.SysLogConnectionLost):
    printJson({"SysLogConnectionLost": ctx.__dict__})

@client.event
async def on_error(ctx :aiosyslog.SysLogError):
    printJson({"SysLogError": ctx.__dict__})

@client.event
async def on_pause_writing(ctx :aiosyslog.SysLogPauseWriting):
    printJson({"SysLogPauseWriting": ctx.__dict__})

@client.event
async def on_resume_writing(ctx :aiosyslog.SysLogResumeWriting):
    printJson({"SysLogResumeWriting": ctx.__dict__})

client.run()