from setuptools import setup, find_packages

setup(
    name="asitop-csv-logger",
    version="1.0.8",
    author="Biswareet Panda",
    author_email="biswa.gunu2003@gmail.com",
    description="CLI tool to log Apple Silicon system metrics to terminal and/or CSV",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Intruder2614/asitop_raw_data_csv",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.9.0",
        "dashing>=0.1.0"

    ],
    entry_points={
        "console_scripts": [
            "asitop-csv-logger = asitop_csv_logger.asitop_csv_logger:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X"
    ],
    license="MIT",
)
