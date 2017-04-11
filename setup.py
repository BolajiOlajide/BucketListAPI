from setuptools import setup, find_packages

setup(
    name='BucketList API',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'alembic==0.9.1',
        'autopep8==1.3',
        'coverage==4.3.4',
        'coveralls',
        'Flask'
        'Flask-HTTPAuth==3.2.2',
        'Flask-Migrate==2.0.3',
        'Flask-Script==2.0.5',
        'Flask-SQLAlchemy==2.2',
        'Flask-SSLify==0.1.5',
        'gunicorn==19.7.1',
        'nose==1.3.7',
        'passlib==1.7.1',
        'psycopg2==2.7.1',
        'python-dotenv==0.6.4',
        'SQLAlchemy==1.1.6'
    ]
)