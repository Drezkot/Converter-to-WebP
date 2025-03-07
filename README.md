### Описание:
Этот проект представляет собой веб-приложение на Flask для конвертации изображений в формат WebP. Пользователи могут загружать файлы, которые автоматически обрабатываются и конвертируются в WebP с возможностью их скачивания. Приложение поддерживает форматы **JPEG, PNG, BMP, TIFF, HEIC, WEBP** и обеспечивает автоматическое уменьшение слишком больших изображений.

### Функционал:
- Загрузка одного или нескольких изображений
- Проверка и валидация форматов
- Автоматическое уменьшение изображений, если их размер превышает 50 млн пикселей
- Конвертация изображений в WebP с качеством 80–90%
- Кэширование обработанных файлов
- Возможность скачивания конвертированных изображений
- Логирование всех процессов

### Требования:
- Python 3.10+
- Flask
- Pillow
- Werkzeug

### Установка и запуск:
```bash
# Клонирование репозитория
git clone https://github.com/yourusername/flask-webp-converter.git
cd flask-webp-converter

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python app.py
```

После запуска сервер будет доступен по адресу `http://127.0.0.1:5000/`, где можно загружать изображения и скачивать конвертированные файлы.

---

## Project Description (English)

### Name: Flask WebP Image Converter

### Description:
This project is a Flask-based web application for converting images to WebP format. Users can upload files, which are automatically processed and converted to WebP, with an option to download them. The application supports **JPEG, PNG, BMP, TIFF, HEIC, and WEBP** formats and automatically resizes overly large images.

### Features:
- Upload one or multiple images
- Format validation
- Automatic image resizing if exceeding 50 million pixels
- Conversion to WebP format with 80–90% quality
- Processed file caching
- Download option for converted images
- Logging for all operations

### Requirements:
- Python 3.8+
- Flask
- Pillow
- Werkzeug

### Installation and Run:
```bash
# Clone the repository
git clone https://github.com/yourusername/flask-webp-converter.git
cd flask-webp-converter

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Once started, the server will be available at `http://127.0.0.1:5000/`, where users can upload images and download converted files.

