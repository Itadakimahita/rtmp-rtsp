# RTMP → RTSP Конвертер

## 🧠 Описание

Этот проект — конвертер видеопотоков из RTMP в RTSP. Он позволяет получать RTMP-потоки (например, с дронов или OBS), транслировать их в RTP (через ffmpeg), а затем публиковать как RTSP-потоки (через Python-библиотеку `aiortc`).

Поддерживается **одновременная трансляция нескольких потоков**, управление осуществляется через HTTP API.

---

## ⚙️ Техническое задание

**Задача**: во многих системах видеопоток передается через RTMP, однако принимающая система работает только с RTSP. Необходимо разработать сервис, который:
- принимает RTMP-потоки
- транслирует их в RTP
- публикует их как RTSP-потоки

---

## 📦 Требования

### Установи:

- Python 3.9+ (рекомендуется 3.10 или 3.11)
- ffmpeg (должен быть доступен в `PATH`)
- pip зависимости:

```bash
pip install -r requirements.txt
```

## Установка ffmpeg

Скачай с https://ffmpeg.org/download.html
На Windows положи ffmpeg.exe в C:/ffmpeg и добавь C:/ffmpeg/bin в системную переменную PATH.

## 📁 Структура проекта
```bash
.
├── rtmp2rtp.py        # Получает RTMP → RTP
├── rtsp_server.py     # Публикует RTP → RTSP
├── requirements.txt
└── README.md
```

## 🚀 Как запустить

В файле rtmp2rtp.py указать путь к ffmpeg
line 7: 

```py
ffmpeg_path = "C:/ffmpeg/ffmpeg.exe"  # путь к ffmpeg
```

### 1. Запуск RTMP → RTP ретранслятора
```bash
python rtmp2rtp.py
```

### 📥 По умолчанию поток RTMP принимается по адресу:
```bash
rtmp://<ваш_сервер>/stream/<stream_key>
```

🎯 Он перенаправляется в RTP (порт подбирается автоматически) и сохраняется в словарь активных потоков.



Примеры API:

  Начать приём потока:
```bash
curl -X POST http://localhost:8080/start -H "Content-Type: application/json" -d '{"stream_key": "stream"}'
```
  Получить список активных потоков:
```bash
curl http://localhost:8080/streams
```
  Остановить поток:
```bash
curl -X POST http://localhost:8080/stop -H "Content-Type: application/json" -d '{"stream_key": "stream2"}'
```

### 2. Запуск RTSP-сервера
```bash
python rtsp_server.py
```
RTSP-сервер запускается на `rtsp://localhost:8554/<stream_key>`
Пример воспроизведения:
```bash
ffplay rtsp://localhost:8554/<stream_key>
```
Или в VLC:

Media → Open Network Stream → `rtsp://localhost:8554/<stream_key>`

### Примечание: 
Грубо меняемые порты на RTSP-сервере(порты и ключи нужно прописывать вручную)



## 🧬 Как работает конвертер

  ### 📡 rtmp2rtp.py запускает ffmpeg для каждого RTMP-потока:
  
  1) ffmpeg читает RTMP-поток

  2) транслирует его в RTP

  3) ffmpeg отправляет видео по UDP на порт 5000+N

  ### 🛰️ rtsp_server.py использует библиотеку aiortc, чтобы:

  4) слушать порты RTP

  5) раздавать потоки через RTSP (WebRTC поверх RTSP)

  ### 💡 Управление осуществляется через HTTP API:

  6) запуск/остановка потока

  7) отображение активных потоков

## 📌 Примечания

  * Потоки RTMP должны поступать в формате H264 + AAC

  * Каждый поток получает уникальный RTP порт (например, 5004, 5006, 5008 и т.д.)

 *  Система логирует действия и ошибки

## 📈 Возможности

* RTMP → RTP трансляция

* RTP → RTSP публикация

* Поддержка нескольких потоков одновременно

* HTTP API для управления

* Простая интеграция в микросервисную архитектуру

* Масштабируемость с Docker

## 📮 Авторы

### Разработано в рамках хакатона 🤖
Связь: kadyrovdias8b@gmail.com; tg: @itadakimashita
