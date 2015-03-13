from setuptools import setup, find_packages
from cubbie import __version__ as cubbie_version

setup(
    name="cubbie",
    version=cubbie_version,
    author="Rich Wareham",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cubbie = cubbie.manager:main',
            'cubbieui = cubbieui.manager:main',
        ],
    },
    install_requires=[
        # Flask-related modules
        "flask",
        "flask-bower",
        "flask-migrate",
        "flask-script",
        "flask-sqlalchemy",

        # Postgres and database support
        "sqlalchemy",
        "psycopg2",

        # Generating fake data in development
        "mixer",

        # Authorisation via JWTs
        "pyjwt",
        "flask-jwt",

        # Third-party authentication methods
        "oauth2client",
        "google-api-python-client",

        # Misc packages
        "pydenticon",
    ],
    tests_require=[
        "tox",
    ],
)
