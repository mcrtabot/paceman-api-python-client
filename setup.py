from setuptools import find_packages, setup

setup(
    name="paceman-api-python-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    description="PaceMan API Python Client",
    author="mcrtabot",
    url="https://github.com/mcrtabot/paceman-api-python-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
