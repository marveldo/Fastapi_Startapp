from ..base.basecommand import BaseCommand
import re
from users.models import User
from ..db import get_db
import importlib

class CreatesuperuserCommand(BaseCommand):

    def handle(self, *args, **kwargs):
        importlib.import_module(('app.tokens.models'))
        db = next(get_db())
        x = True
        while x :
           email = input('Enter Your email Address: ')

           email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
           if re.match(email_regex , email):
               user = User.objects.get(email = email , db=db)
               if user is not None :
                   print('User Already exists !!!')
               else :
                   x = False
           else :
               print('Invalid Email')
        
        y = True
        while y :
            password = input('Enter Your password: ')
            second_password = input('Enter the password again: ')
            if password == second_password :
                y = False
            else:
                print('Passwords Dont match')
        User.objects.create_super_user(
            db=db,
            email = email,
            password = password
        )
        print('Superuser created successfully !! ')

            
        

        
        