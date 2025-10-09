"""
Train ML Models Script
Script para entrenar todos los modelos ML.

Uso:
    python scripts/train_models.py
"""

import sys
from pathlib import Path

# Agregar proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ml.training.trainer import ModelTrainer

if __name__ == "__main__":
    # Crear trainer
    trainer = ModelTrainer(
        data_path='data/processed/restaurantes_sin_anomalias.csv',
        models_dir='data/models'
    )

    # Entrenar todos los modelos
    models = trainer.train_all()

    print("\n🎉 ¡Listo! Los modelos están entrenados y guardados.")
    print("\n🚀 Siguiente paso: Reinicia la API para usar los nuevos modelos")
    print("   python -m src.presentation.api.main")