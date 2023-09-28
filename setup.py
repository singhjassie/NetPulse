from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_desc = readme.read()

with open("requirements.txt", "r", encoding="utf-8") as packages:
    requirements = packages.read()

setup(
    name="NetPulse",
    version="1.0.0",
    description="Network Traffic Analysis Software",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/singhjassie/NetPulse",
    download_url="https://github.com/singhjassie/NetPulse",
    author="Jaskaran Singh",
    author_email="thecodingwizardd@gmail.com",
    license="Apache2.0",
    packages=find_packages(),
    package_dir={'NetPulse': './'},
    package_data={
        'fonts': ['assets/fonts/*.ttf'],
        'images': ['assets/images/*.png'],
        'configurations': ['./*.json']
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache :: 2.0",
        "Environment :: X11 Applications :: GTK",
        "Operating System :: POSIX :: Linux"
    ],
    data_files=[
        ('share/applications/', ['NetPulse.desktop'])
    ],
    keywords="NetPulse netpulse network traffic analysis wireshark monitor analyze",
    python_requires=">=3.9",
    entry_points={
        'console_scripts':['main']
    }
    
)