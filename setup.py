from setuptools import setup, find_packages

setup(
    name="codex-ia",
    version="0.1.0",
    description="Advanced Agentic AI Coding Assistant",
    author="Mauricio Dias Silva",
    packages=find_packages(),
    install_requires=[
        "google-genai",
        "typer[all]",
        "rich",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "codex=codex_ia.main:app",
        ],
    },
    python_requires=">=3.9",
)
