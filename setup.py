from setuptools import setup, find_packages

setup(
    name="redacao_detector",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-multipart>=0.0.5",
        "rich>=10.0.0",
        "pillow>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "redacao-detector=redacao_detector.cli:main",
        ],
    },
    python_requires=">=3.6",
)