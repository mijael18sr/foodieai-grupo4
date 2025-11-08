"""
Script para ejecutar SOLO la sección de matriz de confusión
Carga el archivo modelo_limpio.csv existente y genera todas las visualizaciones
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
from collections import Counter
from sklearn.metrics import (
 confusion_matrix,
 classification_report,
 ConfusionMatrixDisplay,
 precision_score,
 recall_score,
 f1_score,
 accuracy_score
)

# Configuración
BASE_DIR = Path('.')
DATA_PROCESSED = BASE_DIR / 'data' / 'processed'
MODELS_DIR = BASE_DIR / 'data' / 'models'
FIGURES_DIR = BASE_DIR / 'docs' / 'figures'
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print(" MATRIZ DE CONFUSIÓN - EJECUCIÓN INDEPENDIENTE")
print("="*80)

# ==============================================
# 1. CARGAR MODELO
# ==============================================
print("\n CARGANDO MODELO DE SENTIMIENTOS...")
modelo_path = MODELS_DIR / 'sentiment_model.pkl'

try:
 model_data = joblib.load(modelo_path)

 if isinstance(model_data, dict):
 vectorizer = model_data.get('vectorizer')
 classifier = model_data.get('classifier')

 print(f" Modelo cargado exitosamente")
 print(f" Tipo vectorizador: {type(vectorizer).__name__}")
 print(f" Tipo clasificador: {type(classifier).__name__}")
 print(f" Vocabulario: {len(vectorizer.vocabulary_):,} términos")

 def predict_sentiment(texts):
 if isinstance(texts, str):
 texts = [texts]
 X = vectorizer.transform(texts)
 return classifier.predict(X)
 else:
 def predict_sentiment(texts):
 if isinstance(texts, str):
 texts = [texts]
 return model_data.predict(texts)

 print(" Función predict_sentiment() lista")

except Exception as e:
 print(f" ERROR al cargar modelo: {e}")
 exit(1)

# ==============================================
# 2. CARGAR DATOS
# ==============================================
print("\n CARGANDO DATOS PARA EVALUACIÓN...")
data_path = DATA_PROCESSED / 'modelo_limpio.csv'

try:
 # Cargar TODOS los datos (sin nrows)
 df_evaluacion = pd.read_csv(data_path)
 print(f" Datos cargados: {len(df_evaluacion):,} registros")

 # Limpiar
 df_evaluacion = df_evaluacion.dropna(subset=['comment', 'sentimiento'])
 df_evaluacion = df_evaluacion[df_evaluacion['comment'].astype(str).str.strip().str.len() > 0]

 print(f" Datos limpios: {len(df_evaluacion):,} registros")

 # Distribución
 print(f"\n Distribución de sentimientos:")
 print(df_evaluacion['sentimiento'].value_counts())

except Exception as e:
 print(f" ERROR al cargar datos: {e}")
 exit(1)

# ==============================================
# 3. GENERAR PREDICCIONES
# ==============================================
print("\n🔮 GENERANDO PREDICCIONES...")

y_true = df_evaluacion['sentimiento'].values
y_pred = predict_sentiment(df_evaluacion['comment'].tolist())

print(f" Predicciones completadas: {len(y_pred):,}")

# Distribuciones
print(f"\n Distribución Real:")
true_counts = Counter(y_true)
for sent in ['negativo', 'neutro', 'positivo']:
 count = true_counts.get(sent, 0)
 pct = (count / len(y_true)) * 100 if len(y_true) > 0 else 0
 print(f" {sent:10s}: {count:5d} ({pct:5.1f}%)")

print(f"\n Distribución Predicha:")
pred_counts = Counter(y_pred)
for sent in ['negativo', 'neutro', 'positivo']:
 count = pred_counts.get(sent, 0)
 pct = (count / len(y_pred)) * 100 if len(y_pred) > 0 else 0
 print(f" {sent:10s}: {count:5d} ({pct:5.1f}%)")

# ==============================================
# 4. MATRIZ DE CONFUSIÓN
# ==============================================
print("\n" + "="*80)
print(" MATRIZ DE CONFUSIÓN - ANÁLISIS DE SENTIMIENTOS")
print("="*80)

cm = confusion_matrix(y_true, y_pred, labels=['negativo', 'neutro', 'positivo'])

print("\n Matriz de Confusión (valores absolutos):")
print("-" * 60)
print(f"{'':>12} {'Pred: Neg':>12} {'Pred: Neu':>12} {'Pred: Pos':>12}")
print("-" * 60)
for i, label in enumerate(['Negativo', 'Neutro', 'Positivo']):
 print(f"{label:>12} {cm[i][0]:>12,} {cm[i][1]:>12,} {cm[i][2]:>12,}")
print("-" * 60)
print(f"{'Total':>12} {cm.sum():>12,}")
print("="*80)

# ==============================================
# 5. VISUALIZACIÓN 1: Matriz Estándar
# ==============================================
print("\n Generando visualización 1: Matriz estándar...")

fig, ax = plt.subplots(figsize=(12, 9))
disp = ConfusionMatrixDisplay(
 confusion_matrix=cm,
 display_labels=['Negativo', 'Neutro', 'Positivo']
)
disp.plot(cmap='Blues', ax=ax, values_format=',.0f', colorbar=True)
plt.title('Matriz de Confusión - Análisis de Sentimientos\nRestaurantes de Lima, Perú',
 fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Sentimiento Predicho', fontsize=14, fontweight='bold')
plt.ylabel('Sentimiento Real', fontsize=14, fontweight='bold')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax.grid(False)
plt.tight_layout()

output_fig1 = FIGURES_DIR / 'confusion_matrix_sentiment.png'
plt.savefig(output_fig1, dpi=300, bbox_inches='tight', facecolor='white')
print(f" Figura guardada en: {output_fig1}")
plt.show()

# ==============================================
# 6. VISUALIZACIÓN 2: Heatmap Detallado
# ==============================================
print("\n Generando visualización 2: Heatmap detallado...")

plt.figure(figsize=(14, 10))
cm_df = pd.DataFrame(
 cm,
 index=['Negativo', 'Neutro', 'Positivo'],
 columns=['Negativo', 'Neutro', 'Positivo']
)
sns.heatmap(
 cm_df, annot=True, fmt=',.0f', cmap='YlGnBu',
 linewidths=3, linecolor='white',
 cbar_kws={'label': 'Número de Predicciones', 'shrink': 0.8},
 square=True, annot_kws={'size': 16, 'weight': 'bold'}
)
plt.title(f'Matriz de Confusión - Clasificación de Sentimientos\n'
 f'Modelo: Ensemble | Dataset: {len(df_evaluacion):,} reseñas',
 fontsize=18, fontweight='bold', pad=25)
plt.ylabel('Sentimiento Real', fontsize=15, fontweight='bold', labelpad=15)
plt.xlabel('Sentimiento Predicho', fontsize=15, fontweight='bold', labelpad=15)
plt.xticks(rotation=0, fontsize=13)
plt.yticks(rotation=0, fontsize=13)
plt.tight_layout()

output_fig2 = FIGURES_DIR / 'confusion_matrix_detailed.png'
plt.savefig(output_fig2, dpi=300, bbox_inches='tight', facecolor='white')
print(f" Figura guardada en: {output_fig2}")
plt.show()

# ==============================================
# 7. VISUALIZACIÓN 3: Matriz Normalizada
# ==============================================
print("\n Generando visualización 3: Matriz normalizada (%)...")

cm_normalized = confusion_matrix(
 y_true, y_pred,
 labels=['negativo', 'neutro', 'positivo'],
 normalize='true'
)
plt.figure(figsize=(14, 10))
cm_norm_df = pd.DataFrame(
 cm_normalized * 100,
 index=['Negativo', 'Neutro', 'Positivo'],
 columns=['Negativo', 'Neutro', 'Positivo']
)
sns.heatmap(
 cm_norm_df, annot=True, fmt='.2f', cmap='RdYlGn',
 linewidths=3, linecolor='white',
 cbar_kws={'label': 'Porcentaje (%)', 'shrink': 0.8},
 square=True, vmin=0, vmax=100,
 annot_kws={'size': 16, 'weight': 'bold'}
)
plt.title('Matriz de Confusión Normalizada (%)\nRecall por Clase - Análisis de Sentimientos',
 fontsize=18, fontweight='bold', pad=25)
plt.ylabel('Sentimiento Real', fontsize=15, fontweight='bold', labelpad=15)
plt.xlabel('Sentimiento Predicho', fontsize=15, fontweight='bold', labelpad=15)
plt.xticks(rotation=0, fontsize=13)
plt.yticks(rotation=0, fontsize=13)
plt.tight_layout()

output_fig3 = FIGURES_DIR / 'confusion_matrix_normalized.png'
plt.savefig(output_fig3, dpi=300, bbox_inches='tight', facecolor='white')
print(f" Figura guardada en: {output_fig3}")
plt.show()

# ==============================================
# 8. REPORTE DE CLASIFICACIÓN
# ==============================================
print("\n" + "="*80)
print(" REPORTE DE CLASIFICACIÓN DETALLADO")
print("="*80)

report = classification_report(
 y_true, y_pred,
 labels=['negativo', 'neutro', 'positivo'],
 target_names=['Negativo', 'Neutro', 'Positivo'],
 digits=4, zero_division=0
)
print(report)

# ==============================================
# 9. MÉTRICAS DETALLADAS POR CLASE
# ==============================================
print("\n" + "="*80)
print(" MÉTRICAS DETALLADAS POR CLASE")
print("="*80)

clases = ['negativo', 'neutro', 'positivo']
clases_nombres = ['NEGATIVO', 'NEUTRO', 'POSITIVO']
colores = ['', '', '']

metricas_resumen = []

for clase, nombre, color in zip(clases, clases_nombres, colores):
 y_true_binary = (y_true == clase).astype(int)
 y_pred_binary = (y_pred == clase).astype(int)

 precision = precision_score(y_true_binary, y_pred_binary, zero_division=0)
 recall = recall_score(y_true_binary, y_pred_binary, zero_division=0)
 f1 = f1_score(y_true_binary, y_pred_binary, zero_division=0)
 soporte = (y_true == clase).sum()

 print(f"\n{color} Clase: {nombre}")
 print(f" {'─'*50}")
 print(f" │ Precisión: {precision:.4f} ({precision*100:6.2f}%)")
 print(f" │ Recall: {recall:.4f} ({recall*100:6.2f}%)")
 print(f" │ F1-Score: {f1:.4f} ({f1*100:6.2f}%)")
 print(f" │ Soporte: {soporte:,} ejemplos")
 print(f" {'─'*50}")

 metricas_resumen.append({
 'Clase': nombre,
 'Precisión': precision,
 'Recall': recall,
 'F1-Score': f1,
 'Soporte': soporte
 })

# ==============================================
# 10. MÉTRICAS GLOBALES
# ==============================================
accuracy = accuracy_score(y_true, y_pred)
macro_precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
macro_recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
weighted_f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

print("\n" + "="*80)
print(" MÉTRICAS GLOBALES DEL MODELO")
print("="*80)
print(f"\n ACCURACY (Exactitud Global): {accuracy:.4f} ({accuracy*100:6.2f}%)")
print(f" MACRO PRECISION: {macro_precision:.4f} ({macro_precision*100:6.2f}%)")
print(f" MACRO RECALL: {macro_recall:.4f} ({macro_recall*100:6.2f}%)")
print(f" MACRO F1-SCORE: {macro_f1:.4f} ({macro_f1*100:6.2f}%)")
print(f"⚖️ WEIGHTED F1-SCORE: {weighted_f1:.4f} ({weighted_f1*100:6.2f}%)")
print("="*80)

# ==============================================
# 11. VISUALIZACIÓN 4: Gráfico de Barras
# ==============================================
print("\n Generando visualización 4: Comparación de métricas por clase...")

df_metricas = pd.DataFrame(metricas_resumen)

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(clases_nombres))
width = 0.25

precision_vals = df_metricas['Precisión'].values
recall_vals = df_metricas['Recall'].values
f1_vals = df_metricas['F1-Score'].values

bars1 = ax.bar(x - width, precision_vals, width, label='Precisión',
 color='#3498db', edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x, recall_vals, width, label='Recall',
 color='#2ecc71', edgecolor='black', linewidth=1.5)
bars3 = ax.bar(x + width, f1_vals, width, label='F1-Score',
 color='#e74c3c', edgecolor='black', linewidth=1.5)

for bars in [bars1, bars2, bars3]:
 for bar in bars:
 height = bar.get_height()
 ax.text(bar.get_x() + bar.get_width()/2., height,
 f'{height:.3f}', ha='center', va='bottom',
 fontsize=10, fontweight='bold')

ax.set_xlabel('Clase de Sentimiento', fontsize=14, fontweight='bold')
ax.set_ylabel('Score', fontsize=14, fontweight='bold')
ax.set_title('Comparación de Métricas por Clase\nModelo de Análisis de Sentimientos',
 fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(clases_nombres, fontsize=12)
ax.legend(fontsize=12, loc='upper right', framealpha=0.9)
ax.set_ylim(0, 1.1)
ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()

output_fig4 = FIGURES_DIR / 'metricas_por_clase.png'
plt.savefig(output_fig4, dpi=300, bbox_inches='tight', facecolor='white')
print(f" Figura guardada en: {output_fig4}")
plt.show()

# ==============================================
# RESUMEN FINAL
# ==============================================
print("\n" + "="*80)
print(" EVALUACIÓN COMPLETADA EXITOSAMENTE")
print("="*80)
print(f"\n Dataset evaluado: {len(df_evaluacion):,} registros")
print(f" Accuracy: {accuracy*100:.2f}%")
print(f"\n Figuras generadas:")
print(f" confusion_matrix_sentiment.png")
print(f" confusion_matrix_detailed.png")
print(f" confusion_matrix_normalized.png")
print(f" metricas_por_clase.png")
print("="*80)

