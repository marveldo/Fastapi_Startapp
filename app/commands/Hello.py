from ..base.basecommand import BaseCommand

import importlib

class HelloCommand(BaseCommand):

    def handle(self, *args, **kwargs):
        from sqlalchemy import inspect
        from app.db import engine
    
 
        inspector = inspect(engine)
        print(inspector.get_table_names())
       