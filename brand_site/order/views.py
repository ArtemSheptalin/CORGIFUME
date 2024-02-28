from typing import Any
from django.http import *
from django.views.generic import *
from utils.utils import UtilitiesFunctions
from users.models import *
from cart.cart import Cart
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from loyal_program.models import *
from product.models import *


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderPay(CreateView):
    model = Order
    form_class = NewUserForm
    template_name = 'payment.html'
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        utilities_object = UtilitiesFunctions(self.request.user)
        profile = Profile.objects.get(user=self.request.user.id)
        total_price = int(cart.get_total_price()) + 199
        birthday_price = utilities_object.birthday_discount(int(cart.get_total_price()))
       
        data.update({'cart': cart, 'total_bonuses': utilities_object.showing_income_balls(int(cart.get_total_price())), 
                     'current_bonuses': int(profile.current_bonuses), 'total_price': total_price,
                     'birthday_discount': total_price - birthday_price, 'birthday_price': birthday_price + 199 })
        return data


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'making.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        utilities_object = UtilitiesFunctions(self.request.user)
        profile = Profile.objects.get(user=self.request.user.id)

        total_price = int(cart.get_total_price())
        birthday = utilities_object.if_birthday()
        birthday_price = utilities_object.birthday_discount(int(cart.get_total_price()))
        
        '''
            Если ДР и сумма заказа > 5000:
                1) Скидка 
                2) Результат
            Если ДР и сумма заказа < 5000:
                1) Скидка
                2) Доставка
                3) Результат
            Если нет ДР и сумма заказа > 5000:
                1) Результат
            Если нет ДР и сумма заказа < 5000:
                1) Доставка
                2) Результат
        '''

        if birthday and total_price >= 5000:
            birthday_discount = total_price - birthday_price
        
        elif birthday and total_price < 5000:
            birthday_discount = total_price - birthday_price
            birthday_price += 199
        
        elif not birthday and total_price >= 5000:
            birthday_discount = 0
            birthday_price = total_price
        
        elif not birthday and total_price < 5000:
            birthday_discount = 0
            birthday_price += 199
        

        data.update({'cart': cart, 'total_bonuses': utilities_object.showing_income_balls(int(cart.get_total_price())), 
                     'current_bonuses': int(profile.current_bonuses), 'total_price': total_price,
                     'birthday_discount': birthday_discount, 'birthday_price': birthday_price })
        return data


    def get_initial(self, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user.id)   
        shipment_date = datetime.now().date() + timedelta(days=2)  
        
        return {'city': profile.city, 'index': profile.index, 
                'street': profile.street, 'house': profile.house,
                'corp': profile.corp, 'room': profile.room,
                'shipment_date': shipment_date }


def check_bonuses(request):

    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user.id)
        cart = Cart(request)
        current_bonuses = int(profile.current_bonuses)
        bonuses = request.POST.get('input_bonuses')  
        promocode = request.POST.get('input_promo') 
        order_price = request.POST.get('order_price')

        items = cart.get_content()
        products_dict = []
        for item in items:
            product = Product.objects.get(id=item[0])
            values = item[1]
            
            products_dict.append({
                product.full_name: values
            })

        data_dictionary = {
            'name': profile.first_name,
            'last_name': profile.last_name,
            'phone_number': profile.user.phone_number,
            'region': 'Москва' if request.POST.get('delivery') == 'moscow' else 'Регион, уточнять по адресу',
            'shipment_type': 'Обычная' if request.POST.get('shipment_type') == 'usual' else 'Экспресс',
            'city': request.POST.get('city') if not None else '',
            'index': request.POST.get('index') if not None else '',
            'street': request.POST.get('street') if not None else '',
            'house': request.POST.get('house') if not None else '',
            'corp': request.POST.get('corp') if not None else '',
            'room': request.POST.get('room') if not None else '',
            'shipment_date': request.POST.get('shipment_date') if not None else '',
            'promocode': request.POST.get('input_promo') if not None else '',
            'bonuses': request.POST.get('input_bonuses') if not None else '',
            'order_price': order_price.replace(',00 RUB', ''),
            'loyal_status': profile.loyal_status,
            'products': products_dict,
            'comment': request.POST.get('comment') if not None else '',
        }
        
        try:
            input_bonuses = int(bonuses)
        except (TypeError, ValueError):
            input_bonuses = None
        
        try:
            promocode = str(promocode)
        except (TypeError, ValueError):
            promocode = ''

        '''
            views.py

            1) Если оба поля не пустые:
                А) Если промокод есть в БД и бонусы <= доступным (+ +)
                    return JsonResponse({'success': True, 'both_correct': True})
                Б) Если промокод есть в базе данных, а бонусы > доступных (+ -)
                    return JsonResponse({'success': True, 'promocode': True, 'bonuses': False })
                В) Если промокода нет в БД, а бонусы <= доступным (- +)
                    return JsonResponse({'success': True, 'promocode': False, 'bonuses': True })
                Г) Если промокода нет в БД и бонусы > доступным (- -)
                    return JsonResponse({'success': True, 'both_correct': False })
            2) Если заполнено только поле промокод:
                А) Если промокод есть в БД (+)
                    return JsonResponse({'success': True, 'both_correct': True })
                Б) Если промокода нет в БД (-)
                    return JsonResponse({'success': True, 'promocode': False, 'bonuses': True })
            3) Если заполнено только поле бонусов:
                А) Если бонусы <= доступным (+)
                    return JsonResponse({'success': True, 'both_correct': True})
                Б) Если бонусы > доступных (-)
                    return JsonResponse({'success': True, 'promocode': True, 'bonuses': False })
            4) Если оба поля пустые:
                return JsonResponse({'success': True, 'both_correct': True })
            
            ajax.js

            if (response.success && response.both_correct) 
                $('#promo_formID').addClass('promocode_ok');
                $('#bonuses_formID').addClass('promocode_ok');
                window.location.href = 'http://127.0.0.1:8000/order/order-pay/';
            } else if (response.success && response.promocode && response.bonuses === False) {
                $('#promo_formID').addClass('promocode_ok');
                $('#bonuses_formID').addClass('promocode_error');
            } else if (response.success && response.promocode === False && response.bonuses) {
                $('#promo_formID').addClass('promocode_error');
                $('#bonuses_formID').addClass('promocode_ok');
            } else {
                $('#promo_formID').addClass('promocode_ok');
                $('#bonuses_formID').addClass('promocode_ok');
                window.location.href = 'http://127.0.0.1:8000/order/order-pay/';
            }
            
        '''
        exists = promocode_exists(promocode)
        
        if promocode != '' and input_bonuses != None:
            
            if exists and input_bonuses <= current_bonuses:
                order_price = int(data_dictionary['order_price']) - input_bonuses
                create_order(data_dictionary, profile, order_price, promocode)
                return JsonResponse({'success': True, 'both_correct': True})
            elif exists and input_bonuses > current_bonuses:
                return JsonResponse({'success': True, 'promocode': True, 'bonuses': False })
            elif exists == False and input_bonuses <= current_bonuses:
                return JsonResponse({'success': True, 'promocode': False, 'bonuses': True })
            else:
                return JsonResponse({'success': True, 'both_correct': False })
        elif promocode != '' and input_bonuses == None:
            if exists:
                input_bonuses = 0
                order_price = int(data_dictionary['order_price']) - input_bonuses
                create_order(data_dictionary, profile, order_price, promocode)
                return JsonResponse({'success': True, 'both_correct': True })
            else:
                return JsonResponse({'success': True, 'promocode': False, 'bonuses': True })
        elif promocode == '' and input_bonuses != None:
            if input_bonuses <= current_bonuses:
                order_price = int(data_dictionary['order_price']) - input_bonuses
                create_order(data_dictionary, profile, order_price, promocode)
                return JsonResponse({'success': True, 'both_correct': True})
            else:
                return JsonResponse({'success': True, 'promocode': True, 'bonuses': False })
        else:
            input_bonuses = 0
            order_price = int(data_dictionary['order_price']) - input_bonuses
            create_order(data_dictionary, profile, order_price, promocode)
            return JsonResponse({'success': True, 'both_correct': True })


def promocode_exists(promocode):
    promocode_exists = PromoCode.objects.filter(title=promocode).exists()
    return promocode_exists
       

def create_order(data_dictionary, profile, order_price, promocode):

    print(f"\nИтоговая цена: {order_price}\nВведённый промокод: {promocode}\n")

    exists = promocode_exists(promocode)
    
    if exists:
        promocode_discount = PromoCode.objects.get(title=promocode)
        order_price = order_price - promocode_discount.discount  

    try:
        order = Order.objects.create(
            profile=profile,
            first_name=data_dictionary['name'],
            last_name=data_dictionary['last_name'],
            phone_number=data_dictionary['phone_number'],
            shipment_type=data_dictionary['shipment_type'],
            region=data_dictionary['region'],
            city=data_dictionary['city'],
            index=data_dictionary['index'],
            street=data_dictionary['street'],
            house=data_dictionary['house'],
            corp=data_dictionary['corp'],
            room=data_dictionary['room'],
            shipment_date=data_dictionary['shipment_date'],
            order_price=order_price,
            loyal_status=data_dictionary['loyal_status'],
            product=data_dictionary['products'],
            comment=data_dictionary['comment'],
        )
    except Exception as _:
        print(f"\nОшибка: {_}\n")
    


class TinkoffPay(TemplateView):
    template_name = 'tinkoff-kassa.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user.id)
        order = profile.orders.order_by('-id').first() 
        client_name = f"{profile.last_name} {profile.first_name}"
        form = PaymentForm(initial={
            'amount': int(order.order_price), 
            'name': client_name,  
            'email': self.request.user.email_for_reset, 
            'phone': order.phone_number  
        })
        data['form'] = form
        return data


    


    
    

