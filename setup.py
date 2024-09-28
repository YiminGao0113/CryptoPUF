from setuptools import setup, find_packages

setup(
    name='CryptoPUF',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A Python wrapper for TinyJAMBU encryption and decryption',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yimin Gao',
    author_email='yg9bq@virginia.edu',
    url='https://github.com/YiminGao0113/CryptoPUF.git',  # Replace with your repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
