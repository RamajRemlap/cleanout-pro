"""
Setup script for CleanoutPro backend
Ensures proper package structure for deployment
"""

from setuptools import setup, find_packages

setup(
    name="cleanout-pro",
    version="1.0.0",
    description="CleanoutPro Backend API",
    author="CleanoutPro Team",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    python_requires=">=3.8",
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "sqlalchemy==2.0.25",
        "psycopg[binary]>=3.2.0",
        "alembic==1.13.1",
        "redis==5.0.1",
        "pydantic==2.5.3",
        "pydantic-settings==2.1.0",
        "requests==2.31.0",
        "httpx==0.26.0",
        "Pillow==10.2.0",
        "aiofiles==23.2.1",
        "reportlab==4.0.9",
        "websockets==12.0",
        "python-socketio==5.10.0",
        "pytest==7.4.4",
        "pytest-asyncio==0.23.3",
        "pytest-cov==4.1.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-dateutil==2.8.2",
        "structlog==24.1.0",
    ],
)
