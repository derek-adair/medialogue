import os.path as path
from setuptools import setup
from pkg_resources import parse_requirements
cwd = path.dirname(__file__)
version = "0.0.1"

def get_requirements(source):
    with open(source) as f:
        return sorted({str(req) for req in parse_requirements(f.read())})
setup(
    name='django-medialogue',
    author='Derek Adair',
    author_email='d@derekadair.comm',
    version=version,
    description='An Extention of django-photologue with video support',
    zip_safe=False,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Utilities'],
    packages=['medialogue'],
    install_requires=get_requirements('build-requirements.txt'),
    url="https://github.com/derek-adair/medialogue",
    )
