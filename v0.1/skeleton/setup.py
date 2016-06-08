try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'The techlab brain!',
    'author': 'pol',
    'url': 'github.com/paolocavagnolo/',
    'download_url': 'github.com/paolocavagnolo/',
    'author_email': 'paolo.cavagnolo@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['techBrain'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
