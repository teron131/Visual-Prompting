"""Setup configuration for Visual Prompting package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

# Read requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    requirements = (this_directory / "requirements.txt").read_text().strip().split("\n")

setup(
    name="visual-prompting",
    version="0.1.0",
    author="Visual Prompting Team",
    author_email="contact@visualprompting.ai",
    description="AI-powered structured prompt generation for visual media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/visual-prompting/visual-prompting",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.1.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    include_package_data=True,
    keywords="ai, prompt, generation, visual, image, video, llm, structured",
    project_urls={
        "Bug Reports": "https://github.com/visual-prompting/visual-prompting/issues",
        "Source": "https://github.com/visual-prompting/visual-prompting",
        "Documentation": "https://visual-prompting.readthedocs.io/",
    },
)
