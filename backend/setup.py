from setuptools import setup, find_packages

setup(
    name="concert_booking",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Django>=5.0.0,<5.1.0',
        'djangorestframework>=3.15.1,<4.0.0',
        'django-cors-headers>=4.4.0,<5.0.0',
        'Pillow>=10.2.0,<11.0.0',
        'gunicorn>=21.2.0,<23.0.0',
        'dj-database-url>=2.1.0,<3.0.0',
        'psycopg2-binary>=2.9.9,<3.0.0',
        'whitenoise>=6.6.0,<7.0.0',
        'python-dotenv>=1.0.0,<2.0.0',
        'drf-yasg>=1.21.7,<2.0.0',
    ],
)
