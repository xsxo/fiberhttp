from setuptools import setup, find_packages

README_FILE = open('README.md', 'r')
README = README_FILE.read()
README_FILE.close()

setup(
    name='fiberhttp',
    version='2.0',
    author='xsxo',
    description='High Performance HTTP Requests Library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/xsxo/fiberhttp',
    packages=find_packages(),
    install_requires=[
        'certifi>=2017.4.17',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)