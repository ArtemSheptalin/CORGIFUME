from django.core.management.base import BaseCommand
import os
from ...models import Product
import time
import shutil


class Command(BaseCommand):

    def handle(self, *args, **options):
        base_path = '/Users/ArtemBoss/Desktop/Kwork/CORGIFUME/brand_site/brands'
        for brand in os.listdir(base_path):
            try:
                if os.path.isdir(f"{base_path}/{brand}/"):
                    for card in os.listdir(f"{base_path}/{brand}"):
                        if os.path.isdir(f"{base_path}/{brand}/{card}/"):
                            photos_path = f"{base_path}/{brand}/{card}/photos"
                            if not os.path.exists(photos_path):
                                shutil.rmtree(f"{base_path}/{brand}/{card}")
            except Exception as _e:
                print(f"{_e}")
