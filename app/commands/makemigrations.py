from ..base.basecommand import BaseCommand
import os
from alembic.config import Config
from alembic import command
from ..settings import settings
from pathlib import Path
from app.db import DATABASE_URL


class MakemigrationsCommand(BaseCommand):

    def get_alembic_config(self) -> Config :
        """Configure Alembic updates with database url in settings
        """
        alembic_ini_location = Path(__file__).resolve().parent.parent.parent / 'alembic.ini'
        if not alembic_ini_location.exists():
            print(f"Error: Could not find alembic.ini at {alembic_ini_location}")
            return
        alembic_cfg = Config(alembic_ini_location)
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
        return alembic_cfg
    
    def handle(self, *args, **kwargs):
        alembic_cfg = self.get_alembic_config()
        try :
            command.revision(alembic_cfg , message="auto-migration", autogenerate=True)
            print('Migration Created Successfully')
        except Exception as e :
            print(f'Failed To migrate Error : {e} ')
            return
        try:
            command.upgrade(alembic_cfg , 'head')
            print('Migrated to database Successfully')
        except Exception as e:
             print(f'Failed To migrate to database Error : {e} ')
             return  
        
            

       



