from setuptools import find_packages, setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name='safeworkproject',
    version='2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
)