# Flask Image Converter to WebP

## Overview
This is a Flask-based web application that allows users to upload images, convert them to WebP format, and download the processed files. The application supports multiple image formats and includes automatic EXIF orientation correction and temporary file management.

## Features
- **Multi-format support**: JPG, JPEG, PNG, BMP, TIFF, HEIC, WEBP
- **Automatic EXIF orientation correction**
- **File size and resolution optimization**
- **Temporary storage with automatic cleanup** (Files older than 1 hour are deleted)
- **Secure file handling** with `secure_filename`
- **Logging and error handling**

## Requirements
- Python 3.x
- Flask
- Pillow (PIL)
- APScheduler
- Werkzeug

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/image-webp-converter.git
   cd image-webp-converter
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```sh
   python app.py
   ```
4. Open the browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## How It Works
1. Upload an image (or multiple images) via the web interface.
2. The images are processed and converted to WebP format.
3. Download the converted images from the provided links.

---

# Конвертер изображений во WebP на Flask

## Обзор
Это веб-приложение на Flask, которое позволяет загружать изображения, конвертировать их в формат WebP и скачивать обработанные файлы. Поддерживает различные форматы изображений, автоматически исправляет ориентацию (EXIF) и управляет временным хранилищем файлов.

## Возможности
- **Поддержка нескольких форматов**: JPG, JPEG, PNG, BMP, TIFF, HEIC, WEBP
- **Автоматическая коррекция EXIF-ориентации**
- **Оптимизация размера и разрешения изображений**
- **Временное хранилище с автоматической очисткой** (удаление файлов старше 1 часа)
- **Безопасная обработка файлов** с `secure_filename`
- **Логирование и обработка ошибок**

## Требования
- Python 3.x
- Flask
- Pillow (PIL)
- APScheduler
- Werkzeug

## Установка
1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/yourusername/image-webp-converter.git
   cd image-webp-converter
   ```
2. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
3. Запустите приложение Flask:
   ```sh
   python app.py
   ```
4. Откройте браузер и перейдите по адресу:
   ```
   http://127.0.0.1:5000/
   ```

## Как использовать
1. Загрузите изображение (или несколько изображений) через веб-интерфейс.
2. Файлы будут обработаны и преобразованы в формат WebP.
3. Скачайте конвертированные изображения по предоставленным ссылкам.

