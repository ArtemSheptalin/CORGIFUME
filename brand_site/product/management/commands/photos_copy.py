from django.core.management.base import BaseCommand
import os
from ...models import Product
import time
import shutil


class Command(BaseCommand):

    def handle(self, *args, **options):
        base_path = '/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/main_application/static/images/brands'
        destination_folder = '/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/main_application/static/images/'

        for brand in os.listdir(base_path):
            try:
                for card in os.listdir(f"{base_path}/{brand}"):
                    try:
                        products = Product.objects.filter(name=card)
                        if products:
                            for product in products:
                                photos_path = f"{base_path}/{brand}/{card}/photos"
                                for photo in os.listdir(photos_path):
                                    cleaned_photo = photo.replace('\r', '').replace('\n', '')
                                    try:

                                        unique_path = f"{base_path}/{brand}/{card}/photos/"

                                        renamed_photo = f"{brand} {card} {cleaned_photo}"

                                        source_file = os.path.join(unique_path, photo)

                                        destination_file = os.path.join(destination_folder, renamed_photo)

                                        if not os.path.exists(destination_file):
                                            shutil.move(source_file, destination_file)
                                            print(f"{renamed_photo}\nФотография успешно скопирована!")
                                        else:
                                            print(f"{renamed_photo}\nТакая фотография уже существует в папке назначения.")

                                    except Exception as e:
                                        print(f"Ошибка при обработке фотографии: {e}")
                                        time.sleep(5)

                    except Exception as e:
                        print(f"Ошибка при обработке карточки: {e}")
                        time.sleep(5)
            except Exception as _e:
                pass