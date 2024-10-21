import shutil
import os
upload_directory = os.getenv("UPLOAD_DIRECTORY")


def create_file(file):
    try:
        # Создаем директорию, если она не существует
        os.makedirs(upload_directory, exist_ok=True)

        # Формируем полный путь для сохранения файла
        file_location = os.path.join(upload_directory, file.filename)

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
