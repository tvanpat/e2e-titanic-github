from setuptools import setup

setup(
    name='e2e-titanicapi',
    version='0.0.1',
    description='This is a simple api to predict titanic survivability',
    author_email='tyson@descriptdata.com',
    url='www.descriptdata.com',
    install_requires=[
        'scikit-learn == 0.24.1',
        'PyYAML == 5.3.1',
        'pymongo == 3.11.4',
        'python-dotenv == 0.15.0'
    ]
)