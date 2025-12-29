from setuptools import setup, find_packages

# Read version from VERSION file
with open("VERSION", "r") as f:
    version = f.read().strip()

# Read long description from README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open("risk_engine/requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="equity-risk-system",
    version=version,
    author="Emmanuel Odenyire",
    author_email="eodenyire@gmail.com",
    description="Comprehensive open-source risk management system for financial institutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eodenyire/equity-risk-system",
    project_urls={
        "Bug Tracker": "https://github.com/eodenyire/equity-risk-system/issues",
        "Documentation": "https://github.com/eodenyire/equity-risk-system/blob/main/README.md",
        "Source Code": "https://github.com/eodenyire/equity-risk-system",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "equity-risk=start_system:main",
            "risk-engine=risk_engine.main:main",
            "generate-data=test_data.generate_sample_data:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
    },
    keywords="risk management, financial services, fraud detection, transaction monitoring, banking",
)