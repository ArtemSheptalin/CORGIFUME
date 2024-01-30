import os
from PIL import Image

folder_path = "/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/main_application/static/images/!ALL_IMAGES" # папка проекта
desired_width = 200 # ширина
desired_height = 254 # высота
background_color = (255, 255, 255)  # Белый фон

def is_image_file(file):
    # Проверяем расширение файла
    return file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))

def resize_image(image_path):
    try:
        # Открываем изображение
        image = Image.open(image_path)

        # Рассчитываем новые размеры, сохраняя пропорции и фон
        image.thumbnail((desired_width, desired_height), Image.LANCZOS)
        new_image = Image.new("RGB", (desired_width, desired_height), background_color)
        new_image.paste(image, ((desired_width - image.width) // 2, (desired_height - image.height) // 2))

        # Заменяем оригинальное изображение обработанным
        new_image.save(image_path)
    except:
        # Пропускаем недопустимые файлы
        pass

def process_images(folder_path):
    # Проходимся по всем файлам и папкам в указанной папке
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Проверяем, что файл - изображение
            if is_image_file(file):
                # Получаем путь к изображению
                image_path = os.path.join(root, file)
                # Вызываем функцию изменения размера
                resize_image(image_path)

# Пример использования

process_images(folder_path)
