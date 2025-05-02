from setuptools import setup, find_packages

setup(
    name="redacao_detector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "redacao-detector=redacao_detector.cli:main",
        ],
    },
    python_requires=">=3.7",
)