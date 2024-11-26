
# myapp/context_processors.py
from pathlib import Path
import os
from django.conf import settings

# myapp/context_processors.py
def versioned_static(request):
    version = 'v1.1'  # Increment this version number
    return {
        'STATIC_VERSION': version,
    }
# Untuk menambahkan versioning ke file CSS di Django, Anda dapat menggunakan query string untuk cache busting.
