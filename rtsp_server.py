import asyncio
import socket
import struct
import time

SDP_RESPONSE = """v=0
o=- 0 0 IN IP4 127.0.0.1
s=RTSP Stream
c=IN IP4 127.0.0.1
t=0 0
a=control:*
m=video 5004 RTP/AVP 96
a=rtpmap:96 H264/90000
a=control:track1
"""

class RTSPServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.session_id = "123456"
        self.client_addr = None
        self.client_rtp_port = 5004  # пока жёстко задан
        self.rtp_task = None

    def connection_made(self, transport):
        self.transport = transport
        self.client_addr = transport.get_extra_info('peername')
        print(f"🔗 RTSP клиент подключился: {self.client_addr}")

    def data_received(self, data):
        request = data.decode(errors="ignore")
        print("📥 Запрос от клиента:\n", request.strip())
        lines = request.split('\r\n')
        method, path, protocol = lines[0].split()
        cseq = next((line.split(": ")[1] for line in lines if line.startswith("CSeq")), "1")

        if method == "OPTIONS":
            response = (
                f"RTSP/1.0 200 OK\r\n"
                f"CSeq: {cseq}\r\n"
                f"Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY\r\n\r\n"
            )
        elif method == "DESCRIBE":
            response = (
                f"RTSP/1.0 200 OK\r\n"
                f"CSeq: {cseq}\r\n"
                f"Content-Base: rtsp://127.0.0.1:8554/stream/\r\n"
                f"Content-Type: application/sdp\r\n"
                f"Content-Length: {len(SDP_RESPONSE)}\r\n\r\n"
                f"{SDP_RESPONSE}"
            )
        elif method == "SETUP":
            # пока жёстко используем client_port=5004
            response = (
                f"RTSP/1.0 200 OK\r\n"
                f"CSeq: {cseq}\r\n"
                f"Transport: RTP/AVP;unicast;client_port=5004-5005;server_port=5004-5005\r\n"
                f"Session: {self.session_id}\r\n\r\n"
            )
        elif method == "PLAY":
            response = (
                f"RTSP/1.0 200 OK\r\n"
                f"CSeq: {cseq}\r\n"
                f"Session: {self.session_id}\r\n\r\n"
            )
            print("▶️ PLAY запрос принят — начинаем RTP передачу")
            self.rtp_task = asyncio.create_task(self.start_rtp_stream())

        else:
            response = (
                f"RTSP/1.0 501 Not Implemented\r\n"
                f"CSeq: {cseq}\r\n\r\n"
            )

        self.transport.write(response.encode())

    def connection_lost(self, exc):
        print(f"❌ RTSP клиент отключился: {self.client_addr}")
        if self.rtp_task:
            self.rtp_task.cancel()

    async def start_rtp_stream(self):
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock.bind(("0.0.0.0", 5004))
        recv_sock.setblocking(False)

        ip = self.client_addr[0]
        port = self.client_rtp_port
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print(f"📥 RTP: прослушиваем вход на 0.0.0.0:5004 → ⏩ отправка на {ip}:{port}")

        loop = asyncio.get_event_loop()

        try:
            while True:
                try:
                    data, _ = await loop.sock_recvfrom(recv_sock, 2048)
                    send_sock.sendto(data, (ip, port))
                except asyncio.CancelledError:
                    break
        finally:
            recv_sock.close()
            send_sock.close()   



async def main():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(lambda: RTSPServerProtocol(), "0.0.0.0", 8554)
    print("🚀 RTSP сервер с RTP запущен на rtsp://localhost:8554/stream")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
