import os
from setuptools import setup
from pkg_resources import parse_requirements

version = "0.0.8"

def get_requirements(source):
    with open(source) as f:
        return sorted({str(req) for req in parse_requirements(f.read())})

# Lovingly stolen from https://tinyurl.com/2fwt4c99
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

migration_files = package_files('medialogue/migrations')
template_files = package_files('medialogue/templates')

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
    package_data= {
            '': migration_files,
            '': template_files
        },
    install_requires=get_requirements('build-requirements.txt'),
    url="https://github.com/derek-adair/medialogue",
    )
