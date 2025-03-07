import atexit
import logging
import os
import shutil
import tempfile
import time
import uuid

from PIL import Image, UnidentifiedImageError
from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Flask приложение
app = Flask(__name__)

# Поддерживаемые форматы
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".heic", ".webp"}
MAX_PIXELS = 50_000_000  # Ограничение на размер изображения (50 млн пикселей)

# Временная папка для хранения файлов
temp_dir = tempfile.TemporaryDirectory()
TEMP_FOLDER = temp_dir.name


# Очистка временной папки при завершении работы сервера
def cleanup_temp_folder():
    """Очищает временную папку при завершении работы сервера."""
    shutil.rmtree(TEMP_FOLDER, ignore_errors=True)
    logging.info("🧹 Временная папка очищена")


atexit.register(cleanup_temp_folder)


def convert_to_webp(image_file, output_path):
    """Конвертирует изображение в WebP и сохраняет во временной папке."""
    start_time = time.time()
    try:
        img = Image.open(image_file)

        if img.size[0] * img.size[1] > MAX_PIXELS:
            img.thumbnail((2048, 2048))
            quality = 75  # Снижаем качество при больших изображениях
            logging.info("⚠️ Изображение уменьшено для соответствия ограничениям")
        else:
            quality = 90

        img.save(output_path, "WEBP", quality=quality)
        elapsed_time = time.time() - start_time
        logging.info(f"✅ Успешная конвертация {image_file.filename} - ⏱ {elapsed_time:.2f} сек")
        return output_path
    except UnidentifiedImageError:
        logging.error(f"❌ Ошибка: файл {image_file.filename} не является изображением")
    except Exception as e:
        logging.error(f"❌ Ошибка: {type(e).__name__} - {e}", exc_info=True)
    return None


@app.route("/", methods=["GET", "POST"])
def upload_files():
    """Обрабатывает загрузку нескольких изображений."""
    try:
        if request.method == "POST":
            files = request.files.getlist("files")
            if not files or all(file.filename == "" for file in files):
                return "Файлы не выбраны", 400

            converted_files = []

            for file in files:
                filename = secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[-1].lower()

                if file_ext not in SUPPORTED_FORMATS:
                    logging.warning(f"⚠️ Файл {filename} имеет неподдерживаемый формат, пропускаем.")
                    continue

                unique_filename = f"{uuid.uuid4().hex}.webp"
                output_path = os.path.join(TEMP_FOLDER, unique_filename)

                if convert_to_webp(file, output_path):
                    converted_files.append(unique_filename)

            if converted_files:
                return render_template("success.html", files=converted_files)
            else:
                return "Ошибка при конвертации всех файлов", 500

        return render_template("index.html")
    except Exception as e:
        logging.error(f"Ошибка при загрузке файлов: {e}", exc_info=True)
        return "Произошла ошибка на сервере", 500


@app.route("/download/<filename>")
def download_file(filename):
    """Позволяет скачать конвертированное изображение из временной папки."""
    file_path = os.path.join(TEMP_FOLDER, filename)
    if os.path.exists(file_path):
        logging.info(f"Файл {filename} скачан пользователем {request.remote_addr}")
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype="image/webp")
    abort(404, "Файл не найден")


if __name__ == "__main__":
    app.run(debug=True)
