from setuptools import setup, find_packages

setup(

    name='Domainker',
    version='1.75',
    description='BugBounty Tool',
    url='https://github.com/BitTheByte/Domainker',
    author='Ahmed Ezzat (BitTheByte)',
    author_email='ahmed.ezzat119@outlook.com',
    classifiers=[ 
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    py_modules=['domainker'],
    entry_points = """
        [console_scripts]
        domainker = domainker:domainker
    """,
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    install_requires=['requests','boto3','colorama','dnspython'],  
    project_urls={
        'Bug Reports': 'https://github.com/BitTheByte/Domainker/issues',
        'Source': 'https://github.com/BitTheByte/Domainker',
    },
)
