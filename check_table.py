import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
cursor = connection.cursor()

# Check if config_location table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config_location';")
if cursor.fetchone():
    print('config_location table exists')
else:
    print('config_location table does not exist')
    # Create the table
    cursor.execute('''
        CREATE TABLE "config_location" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(100) NOT NULL UNIQUE,
            "description" varchar(200) NOT NULL,
            "icon" varchar(10) NOT NULL,
            "color" varchar(7) NOT NULL,
            "image" varchar(100) NULL,
            "is_active" bool NOT NULL,
            "latitude" decimal NULL,
            "longitude" decimal NULL,
            "created_at" datetime NOT NULL,
            "updated_at" datetime NOT NULL
        );
    ''')
    print('Created config_location table')