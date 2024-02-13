from users.models import *
from datetime import date
from datetime import datetime, timedelta
from django.utils import timezone


class UtilitiesFunctions():
    
    def __init__(self, user):
        self.user = user
        self.profile = Profile.objects.get(user=user.id)
        self.begginer_price = 400
        self.amateur = 600
        self.knower = 800
        self.expert = 1000
        self.master = 1000
        self.month_minus = 2
    
    '''
        Функции для отображения статуса профиля.
    '''

    def get_user(self):
        return self.user.id
    

    def get_user_profile(self):
        return self.profile


    def get_aroma_balls(self):
        return self.profile.aroma_balls


    def get_current_bonuses(self):
        return self.profile.current_bonuses
    

    def get_loyal_status(self):
        return self.profile.loyal_status
    

    def future_balls(self):
        
        if self.profile.loyal_status == 'Новичок':
            return 21 - self.profile.aroma_balls 
        
        elif self.profile.loyal_status == 'Любитель':
            return 41 - self.profile.aroma_balls
        
        elif self.profile.loyal_status == 'Знаток':
            return 61 - self.profile.aroma_balls
        
        elif self.profile.loyal_status == 'Эксперт':
            return 81 - self.profile.aroma_balls
    
    '''
        Функции для осуществления рассчетов (основа программы).

        Выполняются после успешной оплаты (смотри файл работы с API).
    '''

    def increasing_balls(self, order_price):

        if self.profile.loyal_status == 'Новичок' and order_price >= self.begginer_price:
            self.profile.aroma_balls += 1
        
        elif self.profile.loyal_status == 'Любитель' and order_price >= self.amateur:
            self.profile.aroma_balls += 1

        elif self.profile.loyal_status == 'Знаток' and order_price >= self.knower:
            self.profile.aroma_balls += 1
        
        elif self.profile.loyal_status == 'Эксперт' and order_price >= self.expert:
            self.profile.aroma_balls += 1
        
        elif self.profile.loyal_status == 'Мастер ароматов' and order_price >= self.master:
            self.profile.aroma_balls += 1

        self.profile.save()


    def set_loyal_status(self):

        if self.profile.aroma_balls <= 20:
            self.profile.loyal_status = 'Новичок'

        elif 20 < self.profile.aroma_balls <= 40:
            self.profile.loyal_status = 'Любитель'

        elif 40 < self.profile.aroma_balls <= 60:
            self.profile.loyal_status = 'Знаток'

        elif 60 < self.profile.aroma_balls <= 80:
            self.profile.loyal_status = 'Эксперт'

        elif 80 < self.profile.aroma_balls <= 100:
            self.profile.loyal_status = 'Мастер ароматов'
        
        self.profile.save()
    

    def count_discount(self, order_price):

        if self.profile.loyal_status == 'Новичок':
            result = int(order_price // 100 * 1)
            self.profile.current_bonuses += result
        
        elif self.profile.loyal_status == 'Любитель':
            result = int(order_price // 100 * 1.1)
            self.profile.current_bonuses += result

        elif self.profile.loyal_status == 'Знаток':
            result = int(order_price // 100 * 1.2)
            self.profile.current_bonuses += result
        
        elif self.profile.loyal_status == 'Эксперт':
            result = int(order_price // 100 * 1.3)
            self.profile.current_bonuses += result
        
        elif self.profile.loyal_status == 'Мастер ароматов':
            result = int(order_price // 100 * 1.5)
            self.profile.current_bonuses += result

        self.profile.save()
    

    def showing_income_balls(self, order_price):
        
        if self.profile.loyal_status == 'Новичок':
            result = int(order_price // 100 * 1)
        
        elif self.profile.loyal_status == 'Любитель':
            result = int(order_price // 100 * 1.1)

        elif self.profile.loyal_status == 'Знаток':
            result = int(order_price // 100 * 1.2)
        
        elif self.profile.loyal_status == 'Эксперт':
            result = int(order_price // 100 * 1.3)

        
        elif self.profile.loyal_status == 'Мастер ароматов':
            result = int(order_price // 100 * 1.5)
        
        return result

    
    '''
        Доп.функция, запускающаяся раз в сутки и проверяющая, сколько прошло времени с регистрации,
        если больше месяца, то вычитает два арома бонуса.
    '''

    def decreasing_balls(self):

        difference = date.today() - self.profile.date_of_register
        if str(difference) == '0:00:00' and self.profile.aroma_balls > 20:
            self.profile.aroma_balls -= self.month_minus
        
        self.profile.save()
 
    
    '''
        Функция, делающая скидку на заказ в др (в зависимости от статуса),
        действует на 1 покупку на сумму до 100 тысяч рублей.

        Выполняет в момент формирования заказа (см. файл работы с API)
    '''

    def birthday_discount(self, order_price):

        current_date = timezone.now().date()
        specific_date_string = self.profile.date_of_birth

        today_year = timezone.now().year
        specific_date = datetime.strptime(specific_date_string, '%d.%m.%Y').date()
        specific_date = specific_date.replace(year=today_year)

        start_date = specific_date - timedelta(days=14)
        end_date = specific_date + timedelta(days=14)

        if start_date <= current_date <= end_date and self.profile.has_birthday_present == False and order_price <= 100000:
            
            if self.profile.loyal_status == 'Новичок':
                discount = int(order_price // 100 * 3)
                self.profile.has_birthday_present = True
                return order_price - discount
        
            elif self.profile.loyal_status == 'Любитель':
                discount = int(order_price // 100 * 5)
                self.profile.has_birthday_present = True
                return order_price - discount

            elif self.profile.loyal_status == 'Знаток':
                discount = int(order_price // 100 * 7)
                self.profile.has_birthday_present = True
                return order_price - discount
            
            elif self.profile.loyal_status == 'Эксперт':
                discount = int(order_price // 100 * 10)
                self.profile.has_birthday_present = True
                return order_price - discount
            
            elif self.profile.loyal_status == 'Мастер ароматов':
                discount = int(order_price // 100 * 15)
                self.profile.has_birthday_present = True
                return order_price - discount
        else:
            return 0
    
    
    '''
        Функция, высчитывающая стоимость продукта с учетом скидки в честь др.
    '''

    def birthday_catalog_price(self, product_price):
        current_date = timezone.now().date()
        specific_date_string = self.profile.date_of_birth

        today_year = timezone.now().year
        specific_date = datetime.strptime(specific_date_string, '%d.%m.%Y').date()
        specific_date = specific_date.replace(year=today_year)

        start_date = specific_date - timedelta(days=14)
        end_date = specific_date + timedelta(days=14)

        if start_date <= current_date <= end_date and self.profile.has_birthday_present == False:
            
            if self.profile.loyal_status == 'Новичок':
                discount = int(product_price // 100 * 3)
                return product_price - discount
        
            elif self.profile.loyal_status == 'Любитель':
                discount = int(product_price // 100 * 5)
                return product_price - discount

            elif self.profile.loyal_status == 'Знаток':
                discount = int(product_price // 100 * 7)
                return product_price - discount
            
            elif self.profile.loyal_status == 'Эксперт':
                discount = int(product_price // 100 * 10)
                return product_price - discount
            
            elif self.profile.loyal_status == 'Мастер ароматов':
                discount = int(product_price // 100 * 15)
                return product_price - discount
        else:
            return 0
