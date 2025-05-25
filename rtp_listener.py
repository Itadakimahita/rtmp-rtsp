import asyncio
from aiortc.rtp import RtpPacket
import socket

RTP_IP = "127.0.0.1"
RTP_PORT = 5004

async def rtp_listener():
    print(f"🎧 Слушаем RTP поток на {RTP_IP}:{RTP_PORT}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((RTP_IP, RTP_PORT))

    while True:
        data, addr = sock.recvfrom(2048)
        packet = RtpPacket.parse(data)
        print(f"🎞️ Получен пакет: seq={packet.sequence_number}, timestamp={packet.timestamp}")


asyncio.run(rtp_listener())
