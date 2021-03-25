import os
import setuptools

INSTALL_REQUIRES_FILE = os.path.join(
    os.path.dirname(__file__), 'requirements.txt')
with open(INSTALL_REQUIRES_FILE, 'r') as requires_file:
    REQUIREMENTS = [line.strip() for line in requires_file if line != '\n']

setuptools.setup(
    name="legions-common",
    version="2.1.4",
    author="SRE",
    author_email="sre@shipt.com",
    description="A legion-common package for load test",
    install_requires=REQUIREMENTS,
    url="https://github.com/shipt/legions-common",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
