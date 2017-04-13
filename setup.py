from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "requirements.txt")) as f:
    requirements = []
    for line in f:
        # Skip lines with hash values
        if not line.strip().startswith("--"):
            requirements.append(line.split()[0])

setup(
    name='BucketList API',
    version='1.0',
    long_description=__doc__,
    author="Bolaji Olajide",
    author_email="bolaji.olajide@andela.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    url="https://github.com/andela-bolajide/BucketListAPI",
)
