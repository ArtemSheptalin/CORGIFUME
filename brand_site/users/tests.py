from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class UserAccountTests(TestCase):
    
    def test_new_superuser(self):
        db = get_user_model()
        superuser = db.objects.create_superuser(
            '88888888888', 'test@super.com', 'password')
        self.assertEqual(superuser.phone_number, '88888888888')
        self.assertEqual(superuser.email_field, 'test@super.com')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(str(superuser), superuser.phone_number)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                phone_number='88888888888', email_field='testuser@super.com', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                phone_number='88888888888', email_field='testuser@super.com', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                phone_number='', email_field='testuser@super.com', password='password', is_superuser=True)

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            '88888888888', 'test@super.com', 'password')
        self.assertEqual(user.phone_number, '88888888888')
        self.assertEqual(user.email_field, 'test@super.com')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                phone_number='88888888888', email_field='test@super.com', password='password')

        with self.assertRaises(ValueError):
            db.objects.create_user(
                phone_number='', email_field='test@super.com', password='password')
            
        with self.assertRaises(ValueError):
            db.objects.create_user(
                phone_number='88888888888', email_field='', password='password')
            
        with self.assertRaises(ValueError):
            db.objects.create_user(
                phone_number='', email_field='', password='password')
        
        self.assertTrue(db.objects.filter(phone_number='88888888888').exists())

        created_user = db.objects.get(phone_number='88888888888')
        self.assertEqual(created_user.first_name, '')
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)

        self.assertNotEqual(created_user.password, 'password')
    
    def test_create_user_empty_phone_number(self):
        db = get_user_model()
        
        with self.assertRaises(ValueError) as context:
            db.objects.create_user(phone_number='', email_field='test@super.com', password='password')
        
        self.assertEqual(str(context.exception), _('Это обязательное поле, введите номер телефона!'))
    
    def test_create_user_empty_email(self):
        db = get_user_model()
        
        with self.assertRaises(ValueError) as context:
            db.objects.create_user(phone_number='88888888888', email_field='', password='password')
        
        self.assertEqual(str(context.exception), _('Это обязательное поле, введите адрес электронной почты!'))

