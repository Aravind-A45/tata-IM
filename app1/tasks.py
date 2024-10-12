from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import *
from celery import shared_task
import os
import xlrd
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.contrib.auth.models import User
from django.contrib import messages
from openpyxl import load_workbook
from django.core.files.base import ContentFile


@shared_task
def process_excel_file(id, uploader_id):
    try:
        file_obj = File.objects.get(id=id)
        df = pd.read_excel(file_obj.file)

        for index, row in df.iterrows():
            created_by = User.objects.get(id=uploader_id)

            Components.objects.create(
                material_no=row['material_no'],
                material_name=row['material_name'],
                movement_type=row['movement_type'],
                centre=row['centre'],
                description=row['description'],
                unit_of_entry=row['unit_of_entry'],
                plant_no=row['plant_no'],
                receiving_storage_location=row['receiving_storage_location'],
                created_by=created_by
            )

        return "Success"
    except Exception as e:
        return f"An error occurred: {e}"