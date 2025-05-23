import subprocess
import os

def rtmp2rtp():
    
    ffmpeg_path = "C:/ffmpeg/ffmpeg.exe"

    rtmp_url = "rtmp://127.0.0.1/stream/stream"

    rtp_host = "127.0.0.1"
    rtp_port = 5004
    rtp_url = f"rtp://{rtp_host}:{rtp_port}"

    command = [
        ffmpeg_path,
        "-re",  # имитировать реальное время
        "-i", rtmp_url,  # входной RTMP поток
        "-an",  # отключить аудио (для начала)
        "-c:v", "copy",  # без перекодирования
        "-f", "rtp",  # выходной формат
        rtp_url
    ]

    print(f"📡 Ожидаем RTMP поток на: {rtmp_url}")
    print(f"📤 Транслируем в RTP на: {rtp_url}")

    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print("🛑 Остановлено пользователем")
    except FileNotFoundError:
        print(f"Ошибка: не найден ffmpeg по пути {ffmpeg_path}")
