from setuptools import find_packages, setup

setup(
    name='Mathematical_Library',
    packages=find_packages(include=['MathLibrary']),
    version='1.0.0',
    description='This Python library implements obscure algorithms from a variety of mathematical fields.',
    author='Victor Halter, Fernando Arreola, Sicily Guo, Connor Eide, Benjamin Hudson',
    license='Public Domain',
    install_requires=['numpy', 'mmh3', 'bitarray',]
)