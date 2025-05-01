from setuptools import setup, find_packages

setup(
    name="pihace",
    version="0.10.0",
    author="Ahmad Zein Al Wafi",
    author_email="ahmadzeinalwafi@outlook.com",
    description="Python Integrated Health Check - A modular and extensible health check system for services and system resources.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ahmadzeinalwafi/pihace",
    project_urls={
        "Source": "https://github.com/ahmadzeinalwafi/pihace",
        "Tracker": "https://github.com/ahmadzeinalwafi/pihace/issues",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    install_requires=[
        "psutil>=5.9.0",
        "pymongo>=4.3.0",
        "mysql-connector-python>=8.0.30",
        "influxdb-client>=1.36.0",
        "requests>=2.32.3",
        "elasticsearch==8.11.1"
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="healthcheck monitoring system microservice infrastructure",
    license="Apache-2.0",
)
