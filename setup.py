from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wekeza-bank-analytics",
    version="0.1.0",
    author="Wekeza Bank",
    description="Advanced Analytics Workflows for Wekeza Bank",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eodenyire/WekezaBank",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.14.0",
        "statsmodels>=0.14.0",
        "prophet>=1.1.0",
        "sqlalchemy>=2.0.0",
        "prefect>=2.10.0",
        "reportlab>=4.0.0",
        "jinja2>=3.1.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
    ],
)
