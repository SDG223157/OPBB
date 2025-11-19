"""Setup for openbb-roic provider package."""
from setuptools import setup, find_packages

setup(
    name="openbb-roic",
    version="1.0.0",
    description="ROIC provider for OpenBB Platform",
    author="OpenBB Community",
    packages=find_packages(include=["openbb_roic", "openbb_roic.*"]),
    install_requires=[
        "openbb-core>=1.0.0",
        "pandas>=1.5.0",
        "pydantic>=2.0.0",
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="openbb finance roic quality investing metrics",
    entry_points={
        "openbb_provider_extension": [
            "roic = openbb_roic:roic_provider",
        ],
    },
)
