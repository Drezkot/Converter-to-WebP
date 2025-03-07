import logging
import os
import time
import uuid
from PIL import Image, UnidentifiedImageError
from flask import Flask, request, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Flask приложение
app = Flask(__name__)

# Директории для загрузки и конвертированных изображений
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

# Поддерживаемые форматы
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".heic", ".webp"}
MAX_PIXELS = 50_000_000  # Ограничение на размер изображения (50 млн пикселей)
AUTO_RESIZE = True  # Уменьшать слишком большие изображения
CACHE_ENABLED = True  # Включить кэширование обработанных файлов

# Ограничение размера загружаемых файлов (10MB)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Создание папок, если они не существуют
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

processed_cache = set()  # Кэш обработанных файлов


def convert_to_webp(input_path: str, output_path: str, quality: int = 80) -> bool:
    """Конвертирует изображение в WebP."""
    start_time = time.time()

    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        logging.error(f"❌ Ошибка с файлом {input_path}")
        return False

    try:
        with Image.open(input_path) as img:
            # Автоматическое уменьшение размеров при необходимости
            if img.size[0] * img.size[1] > MAX_PIXELS:
                img.thumbnail((2048, 2048))
                logging.info(f"⚠️ Изображение {input_path} было уменьшено")

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, "WEBP", quality=quality)
            elapsed_time = time.time() - start_time
            logging.info(f"✅ Успешная конвертация: {output_path} - ⏱ {elapsed_time:.2f} сек")
            return True
    except UnidentifiedImageError:
        logging.error(f"❌ Ошибка: {input_path} не является изображением")
    except Exception as e:
        logging.error(f"❌ Ошибка: {type(e).__name__} - {e}", exc_info=True)

    return False


@app.route("/", methods=["GET", "POST"])
def upload_files():
    """Обрабатывает загрузку нескольких изображений."""
    try:
        if request.method == "POST":
            if "files" not in request.files:
                return "Файлы не загружены", 400

            files = request.files.getlist("files")
            if not files or all(file.filename == "" for file in files):
                return "Файлы не выбраны", 400

            converted_files = []

            for file in files:
                filename = secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[1].lower()

                if file_ext not in SUPPORTED_FORMATS:
                    logging.warning(f"⚠️ Файл {filename} имеет неподдерживаемый формат, пропускаем.")
                    continue

                # Уникальное имя файла
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                input_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
                file.save(input_path)

                output_filename = os.path.splitext(unique_filename)[0] + ".webp"
                output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_filename)

                if convert_to_webp(input_path, output_path, quality=90):
                    converted_files.append(output_filename)

                # Удаляем исходный файл после обработки
                os.remove(input_path)

            if converted_files:
                return render_template("success.html", files=converted_files)
            else:
                return "Ошибка при конвертации всех файлов", 500

        return render_template("index.html")
    except Exception as e:
        logging.error(f"Ошибка при загрузке файлов: {e}", exc_info=True)
        return "Произошла ошибка на сервере", 500


@app.route("/output/<filename>")
def download_file(filename):
    """Позволяет скачать конвертированное изображение."""
    try:
        return send_from_directory(app.config["OUTPUT_FOLDER"], filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, "Файл не найден")


if __name__ == "__main__":
    app.run(debug=True)
