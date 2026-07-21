"""
Settings cho project Django bọc giao diện quanh logic scheduling gốc.
simulator/core/*.py (Process, PriorityQueue, RoundRobinQueue, Schedule) được
giữ NGUYÊN VẸN — file này chỉ thêm chúng vào sys.path để import được.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Core files dùng import phẳng "from Schedule import Schedule" như khi chạy
# độc lập, nên thêm thư mục của chúng vào sys.path thay vì sửa lại import.
CORE_DIR = BASE_DIR / 'simulator' / 'core'
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

SECRET_KEY = 'django-insecure-cpu-scheduler-demo-key-change-if-deployed'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Chỉ giữ những app thực sự dùng tới: sessions (1 simulator/browser-session),
# messages (thông báo lỗi/thành công). CSS đã inline trong template nên
# không cần staticfiles; không dùng admin/auth.
INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'simulator',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'

# Chỉ dùng cho bảng session mặc định của Django — simulator KHÔNG dùng DB
# (state nằm trong RAM, xem _simulators trong simulator/views.py).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

MESSAGE_TAGS = {
    10: 'debug',
    20: 'info',
    25: 'success',
    30: 'warning',
    40: 'error',
}
