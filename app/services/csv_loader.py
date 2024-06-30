# Load data from CVS files
import csv
from app import db
from app.models import Item
from flask import current_app


def load_csv_data():
    csv_file_path = current_app.config['CSV_FILE_PATH']
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            # Create a new Item object for each row
            item = Item(
                asin=row['asin'],
                title=row['title'],
                stars=float(row['stars']) if row['stars'] else None,
                reviews=int(row['reviews']) if row['reviews'] else None,
                price=float(row['price']) if row['price'] else None
            )
            db.session.add(item)

        db.session.commit()
    print("CSV data loaded successfully")
