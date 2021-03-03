import glob
from setuptools import setup, find_packages
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(APP_DIR, 'README.md')
LICENSE_PATH = os.path.join(APP_DIR, 'LICENSE')
REQUIREMENTS_PATH = os.path.join(APP_DIR, 'requirements.txt')

print ("APP_DIR: ", APP_DIR)
print ("README_PATH: ", README_PATH)
print ("LICENSE_PATH: ", LICENSE_PATH)
print ("REQUIREMENTS_PATH: ", REQUIREMENTS_PATH)

with open(REQUIREMENTS_PATH) as f:
    required = f.read().splitlines()

setup(
    name='rest_apiserver',
    version='0.1.1',  # Required
    license='GPL-3.0',
    author="Ashutosh Mishra",
    author_email="ashutoshdtu@gmail.com",
    description="REST APIs for Cloud Provisioning Assistant",
    long_description_content_type="text/markdown",
    url="https://github.com/ashutoshdtu/assistant-rest-apiserver",
    packages=find_packages("src", exclude=['contrib', 'docs', 'tests']),  # Required
    package_dir={"": "src"},
    py_modules=[os.path.splitext(os.path.basename(i))[0] for i in glob.glob("src/*.py")],
    # package_data={'': ['LICENSE', 'logger.conf']},
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "License :: GPL-3.0",
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ]
)
