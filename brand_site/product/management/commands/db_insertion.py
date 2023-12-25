from django.core.management.base import BaseCommand
from django.core.files import File
from typing import Any
import os
import openpyxl
import re
from ...models import *


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:

        # Получить пути к файлам

        price_file_path = f'/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/prices.xlsx'
       
        base_path = f'/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/brands'

        # Распарсить прайс лист

        workbook2 = openpyxl.load_workbook(price_file_path)
        sheet2 = workbook2.active
        for column in sheet2.iter_rows(min_row=1, values_only=True):
            product_name = column[1]
            product_price = column[2]
            current_color = column[3]

            # Выкидывает ошибку, если дошел до конца файла, так как там None

            if re.search(r'\bTESTER\b', product_name):
                tester = True
            else:
                tester = False
            
            for brand_name in os.listdir(base_path):

                # Проверяем, есть ли папка и является ли папка директорией 

                card_path = f"{base_path}/{brand_name}"
                    
                if os.path.exists(card_path) and os.path.isdir(card_path):
    
                    
                    # Проверить, нужна ли нам эта карточка и есть ли она она в прайс листе
                     
                    for dirname in os.listdir(card_path):
                                            
                        if brand_name in product_name and dirname.upper() in product_name:

                            # Проверяем, есть ли xlsx файл и фото в папке

                            excel_file = f'{card_path}/{dirname}/{dirname}.xlsx'
                            file_count = len(os.listdir(f'{card_path}/{dirname}/photos/'))

                            # Если есть, то парсим карточку
                            
                            if os.path.exists(excel_file) and file_count > 0:

                                workbook = openpyxl.load_workbook(excel_file)

                                sheet = workbook.active

                                match = re.search(r'(\d+(?:\.\d+)?)ml', product_name)

                                if match:
                                    ml = match.group(1)

                                category_keys = ()
                                category_values = ()
                                                
                                for column in sheet.iter_rows(min_row=1, values_only=True):

                                    category_key = column[0] 
                                    category_value = column[1] 

                                    category_keys += (category_key,)
                                    category_values += (category_value,)     

                                dictionary = dict(zip(category_keys, category_values))
                                dictionary['Наименование товара'] = dirname
                                dictionary['Размер флакончика'] = ml
                                dictionary['Цена'] = product_price
                                dictionary['Тестер'] = tester

                                try:
                                    category_name = dictionary['Пол']
                                    category = Category.objects.get(name=category_name)
                                except KeyError:
                                    category = Category.objects.get(id=1)
      
                                try:
                                    upper_notes = dictionary['Верхние ноты']
                                except KeyError:
                                    try:
                                        upper_notes = dictionary['Группы']
                                    except KeyError:
                                        upper_notes = 'Не указано'
                                        
                                try:
                                    medium_notes = dictionary['Средние ноты']
                                except KeyError:
                                    try:
                                        all_notes = dictionary['Ноты'].split(',')
                                        half_index = len(all_notes) // 2 
                                        first_half = all_notes[:half_index]
                                        medium_notes = ', '.join(first_half)
                                    except KeyError:
                                        medium_notes = 'Не указано'
                                        
                                try:
                                    lower_notes = dictionary['Базовые ноты']
                                except KeyError:
                                    try:
                                        all_notes = dictionary['Ноты'].split(',')
                                        half_index = len(all_notes) // 2 
                                        second_half = all_notes[half_index:]
                                        lower_notes = ', '.join(second_half)
                                    except KeyError:
                                        lower_notes = 'Не указано'
                                
                                if dictionary['Тестер']:
                                    tester_slugfield = 'tester'
                                else:
                                    tester_slugfield = 'not-tester'

                                slug_field = dirname.lower().replace(' ', '-') + '-' + tester_slugfield + '-' + str(dictionary['Размер флакончика']) + '-' + str(dictionary['Цена'])

                                try:
                                    if dictionary['Тестер'] == True:
                                        color = current_color
                                        product = Product.objects.create(
                                            category=category,
                                            name=dictionary['Наименование товара'],
                                            slug=slug_field,
                                            upper_notes=upper_notes,
                                            medium_notes=medium_notes,
                                            lower_notes=lower_notes,
                                            year=dictionary['Год создания'],
                                            brand=dictionary['Бренд'],
                                            available=True,
                                            ml=dictionary['Размер флакончика'],
                                            price=dictionary['Цена'],
                                            tester=dictionary['Тестер'],
                                            top_season=False,
                                            present=False,
                                            orders_amount='0',
                                            color=color,
                                        )
                                   
                                    else:
                                        product = Product.objects.create(
                                            category=category,
                                            name=dictionary['Наименование товара'],
                                            slug=slug_field,
                                            upper_notes=upper_notes,
                                            medium_notes=medium_notes,
                                            lower_notes=lower_notes,
                                            year=dictionary['Год создания'],
                                            brand=dictionary['Бренд'],
                                            available=True,
                                            ml=dictionary['Размер флакончика'],
                                            price=dictionary['Цена'],
                                            tester=dictionary['Тестер'],
                                            top_season=False,
                                            present=False,
                                            orders_amount='0',
                                        )

                                    print(f"{dictionary['Бренд']}: {dictionary['Наименование товара']}: {dictionary['Размер флакончика']}: {dictionary['Тестер']}: {dictionary['Цена']} добавлен в PostgreSQL!\n")
                                    for photo in os.listdir(f"{card_path}/{dirname}/photos/"):
                                        cleaned_photo = photo.replace('\r', '').replace('\n', '')
                                        try:
                                            Image.objects.create(
                                                product=product,
                                                image=f"images/{brand_name} {dirname} {cleaned_photo}",
                                            )
                                            
                                            print(f"{dictionary['Бренд']} - {dictionary['Наименование товара']} - {cleaned_photo} добавлен в PostgreSQL!\n\n")
                                            
                                        except Exception as _ex:
                                            print(f"{_ex}")

                                    
                                                        
                                except Exception as _e:
                                    print(f"{_e} с товаром {dictionary['Бренд']}: {dictionary['Наименование товара']}")
       
