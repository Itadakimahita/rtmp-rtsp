import asyncio
import subprocess
from aiohttp import web

STREAMS = {}
BASE_PORT = 5004
ffmpeg_path = "C:/ffmpeg/ffmpeg.exe"  # путь к ffmpeg

async def start_stream(stream_key):
    if stream_key in STREAMS:
        return

    rtmp_url = f"rtmp://127.0.0.1/stream/{stream_key}"
    port = BASE_PORT + len(STREAMS) * 2
    
    command = [
        ffmpeg_path,
        "-i", rtmp_url,
        "-c:v", "copy",
        "-an",
        "-f", "rtp",
        f"rtp://127.0.0.1:{port}"
    ]

    print(f"🎥 Стартуем поток {stream_key} на порту {port}")
    process = await asyncio.create_subprocess_exec(*command)
    STREAMS[stream_key] = {
        "process": process,
        "port": port
    }

async def stop_stream(stream_key):
    stream = STREAMS.get(stream_key)
    if stream:
        print(f"🛑 Останавливаем поток {stream_key}")
        stream["process"].terminate()
        await stream["process"].wait()
        del STREAMS[stream_key]

async def list_streams(request):
    return web.json_response({k: v["port"] for k, v in STREAMS.items()})

async def start_handler(request):
    data = await request.json()
    stream_key = data.get("stream_key")
    if not stream_key:
        return web.HTTPBadRequest(reason="Missing stream_key")
    await start_stream(stream_key)
    return web.json_response({"status": "started", "stream_key": stream_key})

async def stop_handler(request):
    data = await request.json()
    stream_key = data.get("stream_key")
    if not stream_key:
        return web.HTTPBadRequest(reason="Missing stream_key")
    await stop_stream(stream_key)
    return web.json_response({"status": "stopped", "stream_key": stream_key})

app = web.Application()
app.router.add_post("/start", start_handler)
app.router.add_post("/stop", stop_handler)
app.router.add_get("/streams", list_streams)

if __name__ == '__main__':
    print("🚀 Сервис RTMP→RTP мультипоточный запущен на http://localhost:8080")
    web.run_app(app)
