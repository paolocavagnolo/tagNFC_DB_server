try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'theBrain - the big brain of the techlab',
    'author': 'Paolo Cavagnolo',
    'url': '',
    'download_url': 'Where to download it.',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
