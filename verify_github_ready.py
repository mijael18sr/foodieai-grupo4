#!/usr/bin/env python3
"""
🔍 Script de Verificación Pre-GitHub
Verifica que el proyecto esté listo para ser subido a GitHub
"""

import os
import sys
from pathlib import Path
import json

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def check_file(file_path, description):
    """Verifica si un archivo existe"""
    if os.path.exists(file_path):
        print(f"  {Color.GREEN}✅ {description}{Color.END}")
        return True
    else:
        print(f"  {Color.RED}❌ {description} - Archivo no encontrado: {file_path}{Color.END}")
        return False

def check_directory(dir_path, description):
    """Verifica si un directorio existe"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"  {Color.GREEN}✅ {description}{Color.END}")
        return True
    else:
        print(f"  {Color.RED}❌ {description} - Directorio no encontrado: {dir_path}{Color.END}")
        return False

def check_file_size(file_path, min_size_mb=1):
    """Verifica si un archivo tiene un tamaño mínimo"""
    if os.path.exists(file_path):
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb >= min_size_mb:
            print(f"    {Color.BLUE}📊 Tamaño: {size_mb:.2f} MB{Color.END}")
            return True
        else:
            print(f"    {Color.YELLOW}⚠️ Archivo muy pequeño: {size_mb:.2f} MB (mín: {min_size_mb} MB){Color.END}")
            return False
    return False

def main():
    print(f"{Color.BOLD}{Color.BLUE}🔍 VERIFICACIÓN PRE-GITHUB - Restaurant Recommender ML{Color.END}\n")
    
    # Obtener ruta del proyecto
    project_root = Path(__file__).parent.absolute()
    print(f"📁 Directorio del proyecto: {project_root}\n")
    
    all_checks_passed = True
    
    # ==========================================
    # 1. ARCHIVOS DE CONFIGURACIÓN PRINCIPAL
    # ==========================================
    print(f"{Color.BOLD}📋 1. ARCHIVOS DE CONFIGURACIÓN PRINCIPAL{Color.END}")
    
    config_files = [
        ("README.md", "Documentación principal del proyecto"),
        (".gitignore", "Configuración de archivos a ignorar"),
        ("DEPLOYMENT_GUIDE.md", "Guía de despliegue"),
    ]
    
    for file_name, desc in config_files:
        file_path = project_root / file_name
        if not check_file(file_path, desc):
            all_checks_passed = False
    
    print()
    
    # ==========================================
    # 2. BACKEND - ARCHIVOS CRÍTICOS
    # ==========================================
    print(f"{Color.BOLD}🐍 2. BACKEND - ARCHIVOS CRÍTICOS{Color.END}")
    
    backend_root = project_root / "backend"
    
    backend_files = [
        ("requirements.txt", "Dependencias Python"),
        ("start_server.py", "Script de inicio del servidor"),
        ("reentrenar_modelo_limpio.py", "Script de entrenamiento del modelo"),
        ("test_api_funcionando.py", "Tests de la API"),
        (".env.example", "Ejemplo de variables de entorno"),
    ]
    
    for file_name, desc in backend_files:
        file_path = backend_root / file_name
        if not check_file(file_path, desc):
            all_checks_passed = False
    
    print()
    
    # ==========================================
    # 3. DATASETS CRÍTICOS
    # ==========================================
    print(f"{Color.BOLD}📊 3. DATASETS CRÍTICOS{Color.END}")
    
    data_raw_path = backend_root / "data" / "raw"
    
    datasets = [
        ("Lima_Restaurants_2025_08_13_clean.csv", "Dataset principal limpio", 50),
        ("restaurant_metadata.csv", "Metadatos de restaurantes", 1),
    ]
    
    for file_name, desc, min_size in datasets:
        file_path = data_raw_path / file_name
        if check_file(file_path, desc):
            check_file_size(file_path, min_size)
        else:
            all_checks_passed = False
    
    print()
    
    # ==========================================
    # 4. MODELOS DE MACHINE LEARNING
    # ==========================================
    print(f"{Color.BOLD}🤖 4. MODELOS DE MACHINE LEARNING{Color.END}")
    
    models_path = backend_root / "data" / "models"
    
    models = [
        ("sentiment_model.pkl", "Modelo de análisis de sentimientos (84.36% accuracy)", 5),
        ("clustering_model.pkl", "Modelo de clustering de restaurantes", 1),
        ("rating_predictor.pkl", "Predictor de ratings", 1),
        ("recommender_system.pkl", "Sistema de recomendación", 1),
    ]
    
    for file_name, desc, min_size in models:
        file_path = models_path / file_name
        if check_file(file_path, desc):
            check_file_size(file_path, min_size)
        else:
            all_checks_passed = False
    
    print()
    
    # ==========================================
    # 5. FRONTEND - CONFIGURACIÓN
    # ==========================================
    print(f"{Color.BOLD}⚛️ 5. FRONTEND - CONFIGURACIÓN{Color.END}")
    
    frontend_root = project_root / "frontend"
    
    frontend_files = [
        ("package.json", "Configuración y dependencias Node.js"),
        ("vite.config.ts", "Configuración de Vite"),
        ("tailwind.config.js", "Configuración de Tailwind CSS"),
        (".env.example", "Ejemplo de variables de entorno"),
    ]
    
    for file_name, desc in frontend_files:
        file_path = frontend_root / file_name
        if not check_file(file_path, desc):
            all_checks_passed = False
    
    # Verificar package.json específicamente
    package_json_path = frontend_root / "package.json"
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                
            required_scripts = ['dev', 'build', 'preview']
            missing_scripts = [s for s in required_scripts if s not in package_data.get('scripts', {})]
            
            if not missing_scripts:
                print(f"    {Color.GREEN}✅ Scripts npm requeridos están presentes{Color.END}")
            else:
                print(f"    {Color.YELLOW}⚠️ Scripts faltantes: {missing_scripts}{Color.END}")
                
        except Exception as e:
            print(f"    {Color.RED}❌ Error leyendo package.json: {e}{Color.END}")
            all_checks_passed = False
    
    print()
    
    # ==========================================
    # 6. ESTRUCTURA DE DIRECTORIOS
    # ==========================================
    print(f"{Color.BOLD}📁 6. ESTRUCTURA DE DIRECTORIOS{Color.END}")
    
    required_dirs = [
        (backend_root / "src", "Código fuente backend"),
        (backend_root / "data" / "raw", "Datos originales"),
        (backend_root / "data" / "models", "Modelos ML"),
        (frontend_root / "src", "Código fuente frontend"),
        (frontend_root / "src" / "components", "Componentes React"),
        (frontend_root / "src" / "services", "Servicios de API"),
    ]
    
    for dir_path, desc in required_dirs:
        if not check_directory(dir_path, desc):
            all_checks_passed = False
    
    print()
    
    # ==========================================
    # 7. VERIFICACIONES ADICIONALES
    # ==========================================
    print(f"{Color.BOLD}🔍 7. VERIFICACIONES ADICIONALES{Color.END}")
    
    # Verificar que no hay archivos de entorno real
    env_files_check = [
        (backend_root / ".env", "Archivo .env del backend (NO debe estar en repo)"),
        (frontend_root / ".env.local", "Archivo .env.local del frontend (NO debe estar en repo)"),
    ]
    
    for file_path, desc in env_files_check:
        if os.path.exists(file_path):
            print(f"  {Color.YELLOW}⚠️ {desc} - ELIMINAR antes de subir a GitHub{Color.END}")
        else:
            print(f"  {Color.GREEN}✅ {desc} - Correcto, no está presente{Color.END}")
    
    # Verificar .gitignore
    gitignore_path = project_root / ".gitignore"
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        required_patterns = ['.venv', 'node_modules', '__pycache__', '*.log', '.env']
        missing_patterns = [p for p in required_patterns if p not in gitignore_content]
        
        if not missing_patterns:
            print(f"  {Color.GREEN}✅ .gitignore contiene los patrones esenciales{Color.END}")
        else:
            print(f"  {Color.YELLOW}⚠️ .gitignore - Patrones faltantes: {missing_patterns}{Color.END}")
    
    print()
    
    # ==========================================
    # RESULTADO FINAL
    # ==========================================
    print(f"{Color.BOLD}{'=' * 60}{Color.END}")
    
    if all_checks_passed:
        print(f"{Color.GREEN}{Color.BOLD}🎉 ¡PROYECTO LISTO PARA GITHUB! 🚀{Color.END}")
        print(f"{Color.GREEN}✅ Todas las verificaciones pasaron correctamente{Color.END}")
        print(f"\n{Color.BLUE}📋 Próximos pasos:{Color.END}")
        print(f"  1. git add .")
        print(f"  2. git commit -m '🎉 Initial commit: Restaurant Recommender ML System'")
        print(f"  3. git push origin main")
        print(f"\n{Color.YELLOW}💡 Tip: Revisa DEPLOYMENT_GUIDE.md para más detalles{Color.END}")
    else:
        print(f"{Color.RED}{Color.BOLD}❌ PROYECTO NO ESTÁ LISTO{Color.END}")
        print(f"{Color.RED}Algunos archivos críticos están faltando{Color.END}")
        print(f"\n{Color.YELLOW}🔧 Pasos para corregir:{Color.END}")
        print(f"  1. Revisa los archivos marcados con ❌")
        print(f"  2. Ejecuta los comandos de setup del README.md")
        print(f"  3. Vuelve a ejecutar este script")
    
    print(f"{Color.BOLD}{'=' * 60}{Color.END}")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())