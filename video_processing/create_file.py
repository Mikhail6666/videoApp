import os
import shutil

# Путь для сохранения загруженных файлов
UPLOAD_DIRECTORY = "/home/mikhail/PycharmProjects/videoApp/upload_files/"

def create_file(file):
    try:
        # Создаем директорию, если она не существует
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

        # Формируем полный путь для сохранения файла
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

        # Открываем файл для записи в бинарном режиме
        with open(file_location, "wb+") as file_object:
            # Копируем содержимое загруженного файла
            shutil.copyfileobj(file.file, file_object)
            return file_location
    except Exception as e:
        return {"message": f"There was an error uploading the file: {str(e)}"}
    finally:
        # Закрываем файл
        file.file.close()
