from typing import Any
from django.core.management.base import BaseCommand
import pandas as pd
from movie.models import Movie
from sqlalchemy import create_engine

class Command(BaseCommand):
    help = "A command to add data from Excel file to the database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        
        csv_file = 'imdbtop250.csv'
        df = pd.read_csv(csv_file)

        engine = create_engine('postgresql://postgres:Nalamala!!1@localhost:5432/movies')

        df.to_sql(Movie._meta.db_table, if_exists='replace',con=engine,index=False)
        