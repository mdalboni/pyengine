from setuptools import setup, find_packages

setup(
    name='pyengine',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame~=2.5.2',
        'deep-translator~=1.11.4',
        'pyinstaller~=6.3.0',
        'ipdb~=0.13.9',
    ],
    entry_points={
        'console_scripts': [
          'pyengine = cli.__main__:main'
        ],
    },
    author='MDalboni',
    author_email='maxwell@dalboni.land',
    description='An game engine experiment created with python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mdalboni/pyengine',
)
