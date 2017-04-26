#!/bin/bash
cd /app && python manage.py migrate && exec daphne -b 0.0.0.0 -p 8000 chat.asgi:channel_layer
