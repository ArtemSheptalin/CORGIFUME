from django.core.management.base import BaseCommand
from typing import Any
import openpyxl
import re
from ...models import *
import time
import os
from django.core.files import File



class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:

        # Получить пути к файлам

        data_path = f'/root/projects/CORGIFUME/brand_site/price_corg.xlsx'
       
        # Объединить файлы

        workbook1 = openpyxl.load_workbook(data_path)
        sheet1 = workbook1.active

        for column in sheet1.iter_rows(min_row=2, values_only=True):
            article = column[0]
            product_full = column[1]
            product_name = column[2]
            product_brand = column[3]
            product_country = column[4]
            product_category = column[5]
            product_year = column[6]
            product_description = column[8]
            product_notes = column[9]
            product_size = column[10]
            helped_photo = column[11]
            product_photos = column[13]  
            inner_article = column[20]          
            tester = True if re.search(r'\bTESTER\b', product_full) else False
            product_price = column[22]    

            cleaned_helped_photo = []
            res = []

            try:
                if product_category == 'Мужской':

                    product_category = Category.objects.get(name='Для мужчин')
                
                elif product_category == 'Женский':
                    product_category = Category.objects.get(name='Для женщин')
                
                else:
                    product_category = Category.objects.get(name='Унисекс')
            except Exception:
                product_category = Category.objects.get(name='Унисекс')

            try:
                if 'edt' in product_full:
                    product_type = 'Туалетная вода'
                elif 'edp' in product_full:
                    product_type = 'Парфюмерная вода'
                elif 'edc' in product_full:
                    product_type = 'Одеколон'
                elif 'parfume' in product_full:
                    product_type = 'Парфюм'
                elif 'b/spray' in product_full:
                    product_type = 'Спрей для тела'
                elif 'b/cream' or 'b/lotion' in product_full:
                    product_type = 'Лосьон для тела'
                elif 'sh/g' in product_full:
                    product_type = 'Гель для душа'
                elif 'deo stick' or 'deo' in product_full:
                    product_type = 'Дезодорант'
                elif 'af/sh' in product_full:
                    product_type = 'Лосьон после бритья'
                elif 'soap' in product_full:
                    product_type = 'Мыло'
                elif 'candle' in product_full:
                    product_type = 'Свеча'
                elif 'shampoo' in product_full:
                    product_type = 'Шампунь'
                elif 'пробник' in product_full:
                    product_type = 'Пробник'
                else:
                    product_type = ''

            except Exception:
                product_type = ''

            try:
                ml = int(product_size.replace('мл', '').replace('\xa0', '').strip())
            except Exception as _e:
                ml = 0

            try:
                brand = product_brand
            except Exception as _e:
                brand = 'None'

            try:
                price = product_price
            except Exception as _e:
                price = 0.0
            
            try:
                cleaned_helped_photo = [helped_photo]
            except Exception as _e:
                helped_photo = ['']
            
            try:
                notes = product_notes.capitalize().replace(',', ', ')
            except Exception:
                notes = ''
            
            try:
                inner_article = inner_article.replace(' ', '')
            except Exception:
                inner_article = ''
            
            try:
                product = Product.objects.create(
                    category=product_category,
                    full_name=product_full,
                    name=product_name,
                    notes=notes,
                    year=product_year,
                    country=product_country,
                    description=product_description,
                    brand=brand,
                    ml=ml,
                    tester=tester,
                    article=article,
                    inner_article=inner_article,
                    price=price,
                    parfum_type=product_type,
                )
                
                cleaned_product_photos = product_photos.split(',')
                all_cleaned_photos = cleaned_helped_photo + cleaned_product_photos

                for photo in all_cleaned_photos:
                    final_image = photo.replace('\xa0', '\u00A0').split('/')[-1]
                    res.append(final_image)

                cleaned_photos = list(set(res))

                for image_instance in cleaned_photos:

                    image_path = f"/root/projects/CORGIFUME/brand_site/main_application/static/images/!ALL_IMAGES/{image_instance}"

                    with open(image_path, 'rb') as f:
                        image_file = File.open(f)

                        image = Image(product=product)
                        image.image.save(image_instance, image_file)
                        image.save()

                print(f"Done with {product_full}!\n\n")
                    
            except Exception as _e:
                print(f"ОШИБКА:\n{_e}\n")
                

            time.sleep(3)


       
