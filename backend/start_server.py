#!/usr/bin/env python3
"""
Script de inicio para el servidor FastAPI
"""
import sys
import os
from pathlib import Path

# Agregar el directorio actual al path de Python
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    try:
        import uvicorn

        print("Iniciando Restaurant Recommender API...")
        print("Backend URL: http://localhost:8000")
        print("API Docs: http://localhost:8000/docs")
        print("Modo desarrollo con auto-reload activado")
        print("-" * 50)

        # Ejecutar el servidor usando string import para permitir reload
        uvicorn.run(
            "src.presentation.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=[str(current_dir)],
        )

    except ImportError as e:
        print(f"Error de importación: {e}")
        print("\nInstala las dependencias:")
        print("pip install fastapi uvicorn pandas numpy")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        sys.exit(1)
