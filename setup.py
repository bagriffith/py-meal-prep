from setuptools import setup, find_packages

setup(
    name='mealprep',
    version='0.0.1',  
    description='Meal Prep Tools',
    author='Brady Griffith',
    author_email='bradyagriffith@gmail.com',
    packages=find_packages(),
    install_requires=['requests>=2.28.2']
)
