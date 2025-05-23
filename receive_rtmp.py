import subprocess
import os

ffmpeg_path = "C:/ffmpeg/ffmpeg.exe"

rtmp_url = "rtmp://127.0.0.1/stream/stream"
output_file = "test_output.mp4"

if os.path.exists(output_file):
    os.remove(output_file)

command = [
    ffmpeg_path,
    "-i", rtmp_url,
    "-c", "copy",
    "-f", "mp4",
    output_file
]

print("📡 Ждём RTMP поток на:", rtmp_url)
print("📥 Сохраняем в:", output_file)

try:
    subprocess.run(command)
except KeyboardInterrupt:
    print("🛑 Остановлено пользователем")
except FileNotFoundError:
    print(f"Ошибка: не найден ffmpeg по пути {ffmpeg_path}")
