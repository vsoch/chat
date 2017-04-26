#!/bin/bash
cd /app && python manage.py migrate && python manage.py runworker
