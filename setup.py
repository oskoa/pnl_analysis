
from setuptools import setup, find_packages, Command
import os


PYPI_REQUIREMENTS = []
if os.path.exists('requirements.txt'):
    for line in open('requirements.txt'):
        PYPI_REQUIREMENTS.append(line.strip())

setup(
    name='pnl_analysis',
    version='0.10',
    description=(
        'The program analyzes quotes and trades and output paired trades'
    ),
    long_description=open('README.md').read(),
    author='Ali Oskooei',
    author_email='ali.oskooei@gmail.com',
    packages=find_packages('.'),
    install_requires=PYPI_REQUIREMENTS,
    zip_safe=False
)
