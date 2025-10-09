"""
Script de Análisis Exploratorio de Datos (EDA)
Generado desde el notebook 01_exploratory_data_analysis.ipynb
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

print("="*70)
print("📊 INICIANDO ANÁLISIS EXPLORATORIO DE DATOS (EDA)")
print("="*70)

# Crear carpeta para figuras
figures_path = Path('docs/figures')
figures_path.mkdir(parents=True, exist_ok=True)
print(f"✅ Carpeta de figuras creada: {figures_path}")

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================
print("\n" + "="*70)
print("1. CARGA DE DATOS PROCESADOS")
print("="*70)

DATA_PATH = Path('data/processed')

df_limpio = pd.read_csv(DATA_PATH / 'restaurantes_limpio.csv')
df_sin_anomalias = pd.read_csv(DATA_PATH / 'restaurantes_sin_anomalias.csv')
df_alta_calidad = pd.read_csv(DATA_PATH / 'restaurantes_alta_calidad.csv')
df_reviews = pd.read_csv(DATA_PATH / 'reviews_limpio.csv')

print(f"📂 Restaurantes limpios: {df_limpio.shape}")
print(f"📂 Sin anomalías: {df_sin_anomalias.shape}")
print(f"📂 Alta calidad: {df_alta_calidad.shape}")
print(f"📂 Reviews: {df_reviews.shape}")

df = df_alta_calidad.copy()
print(f"\n✅ Dataset principal: {df.shape[0]} restaurantes de alta calidad")

# ============================================================================
# 2. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================================
print("\n" + "="*70)
print("2. ESTADÍSTICAS DESCRIPTIVAS")
print("="*70)

print(f"\n📍 Total de restaurantes: {len(df)}")
print(f"📍 Distritos únicos: {df['district'].nunique()}")
print(f"📍 Categorías únicas: {df['category_clean'].nunique()}")
print(f"\n⭐ Rating promedio: {df['stars'].mean():.2f}")
print(f"⭐ Rating mediana: {df['stars'].median():.2f}")
print(f"⭐ Rating mínimo: {df['stars'].min():.1f}")
print(f"⭐ Rating máximo: {df['stars'].max():.1f}")
print(f"\n💬 Total de reviews: {df['reviews'].sum():,}")
print(f"💬 Promedio de reviews: {df['reviews'].mean():.0f}")
print(f"💬 Mediana de reviews: {df['reviews'].median():.0f}")
print(f"\n📏 Distancia promedio al centro: {df['distance_to_center_km'].mean():.2f} km")
print(f"📏 Distancia máxima: {df['distance_to_center_km'].max():.2f} km")
print(f"\n🏆 Popularity score promedio: {df['popularity_score'].mean():.2f}")

# ============================================================================
# 3. VISUALIZACIÓN 1: DISTRIBUCIÓN DE RATINGS
# ============================================================================
print("\n" + "="*70)
print("3. GENERANDO VISUALIZACIÓN 1: Distribución de Ratings")
print("="*70)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Histograma
axes[0].hist(df['stars'], bins=30, edgecolor='black', alpha=0.7, color='#2ecc71')
axes[0].axvline(df['stars'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Media: {df["stars"].mean():.2f}')
axes[0].axvline(df['stars'].median(), color='blue', linestyle='--', linewidth=2,
                label=f'Mediana: {df["stars"].median():.2f}')
axes[0].set_xlabel('Rating (Estrellas)', fontsize=12)
axes[0].set_ylabel('Frecuencia', fontsize=12)
axes[0].set_title('Distribución de Ratings', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Boxplot
axes[1].boxplot(df['stars'], vert=True)
axes[1].set_ylabel('Rating (Estrellas)', fontsize=12)
axes[1].set_title('Boxplot de Ratings', fontsize=14, fontweight='bold')
axes[1].set_xticklabels(['Ratings'])
axes[1].grid(alpha=0.3)

# KDE
df['stars'].plot(kind='kde', ax=axes[2], linewidth=2, color='#3498db')
axes[2].set_xlabel('Rating (Estrellas)', fontsize=12)
axes[2].set_ylabel('Densidad', fontsize=12)
axes[2].set_title('Densidad de Ratings', fontsize=14, fontweight='bold')
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / 'distribucion_ratings.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: distribucion_ratings.png")
print(f"   - Desviación estándar: {df['stars'].std():.3f}")
print(f"   - Skewness: {df['stars'].skew():.3f}")

# ============================================================================
# 4. VISUALIZACIÓN 2: DISTRIBUCIÓN DE REVIEWS
# ============================================================================
print("\n" + "="*70)
print("4. GENERANDO VISUALIZACIÓN 2: Distribución de Reviews")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(df['reviews'], bins=50, edgecolor='black', alpha=0.7, color='#e74c3c')
axes[0].axvline(df['reviews'].mean(), color='blue', linestyle='--', linewidth=2,
                label=f'Media: {df["reviews"].mean():.0f}')
axes[0].axvline(df['reviews'].median(), color='green', linestyle='--', linewidth=2,
                label=f'Mediana: {df["reviews"].median():.0f}')
axes[0].set_xlabel('Número de Reviews', fontsize=12)
axes[0].set_ylabel('Frecuencia', fontsize=12)
axes[0].set_title('Distribución de Reviews (Escala Normal)', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].hist(df['reviews'], bins=50, edgecolor='black', alpha=0.7, color='#9b59b6')
axes[1].set_xlabel('Número de Reviews', fontsize=12)
axes[1].set_ylabel('Frecuencia', fontsize=12)
axes[1].set_title('Distribución de Reviews (Escala Log-Y)', fontsize=14, fontweight='bold')
axes[1].set_yscale('log')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / 'distribucion_reviews.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: distribucion_reviews.png")
print(f"   - Percentil 90%: {df['reviews'].quantile(0.90):.0f}")

# ============================================================================
# 5. VISUALIZACIÓN 3: CORRELACIÓN REVIEWS VS RATING
# ============================================================================
print("\n" + "="*70)
print("5. GENERANDO VISUALIZACIÓN 3: Correlación Reviews vs Rating")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].scatter(df['reviews'], df['stars'], alpha=0.5, s=50, c=df['popularity_score'],
                cmap='viridis', edgecolors='black', linewidth=0.5)
axes[0].set_xlabel('Número de Reviews', fontsize=12)
axes[0].set_ylabel('Rating (Estrellas)', fontsize=12)
axes[0].set_title('Correlación Reviews vs Rating', fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

z = np.polyfit(df['reviews'], df['stars'], 1)
p = np.poly1d(z)
axes[0].plot(df['reviews'], p(df['reviews']), "r--", linewidth=2, label='Tendencia lineal')
axes[0].legend()

hb = axes[1].hexbin(df['reviews'], df['stars'], gridsize=30, cmap='YlOrRd', mincnt=1)
axes[1].set_xlabel('Número de Reviews', fontsize=12)
axes[1].set_ylabel('Rating (Estrellas)', fontsize=12)
axes[1].set_title('Densidad de Puntos (Hexbin)', fontsize=14, fontweight='bold')
plt.colorbar(hb, ax=axes[1], label='Cantidad')

plt.tight_layout()
plt.savefig(figures_path / 'correlacion_reviews_rating.png', dpi=300, bbox_inches='tight')
plt.close()

pearson_corr = df[['reviews', 'stars']].corr().iloc[0, 1]
print(f"✅ Guardado: correlacion_reviews_rating.png")
print(f"   - Correlación Pearson: {pearson_corr:.3f}")

# ============================================================================
# 6. VISUALIZACIÓN 4: MATRIZ DE CORRELACIÓN
# ============================================================================
print("\n" + "="*70)
print("6. GENERANDO VISUALIZACIÓN 4: Matriz de Correlación")
print("="*70)

numeric_cols = ['stars', 'reviews', 'distance_to_center_km', 'popularity_score']
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=2, fmt='.3f', cbar_kws={'label': 'Correlación'})
plt.title('Matriz de Correlación - Variables Numéricas', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(figures_path / 'matriz_correlacion.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: matriz_correlacion.png")

# ============================================================================
# 7. VISUALIZACIÓN 5: CATEGORÍAS DE RESTAURANTES
# ============================================================================
print("\n" + "="*70)
print("7. GENERANDO VISUALIZACIÓN 5: Categorías de Restaurantes")
print("="*70)

category_counts = df['category_clean'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

category_counts.head(15).plot(kind='barh', ax=axes[0], color='#3498db', edgecolor='black')
axes[0].set_xlabel('Cantidad de Restaurantes', fontsize=12)
axes[0].set_ylabel('Categoría', fontsize=12)
axes[0].set_title('Top 15 Categorías de Restaurantes', fontsize=14, fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

top_categories = category_counts.head(10)
others = category_counts[10:].sum()
if others > 0:
    top_categories = top_categories.copy()
    top_categories['Otros'] = others

colors = plt.cm.Set3(range(len(top_categories)))
axes[1].pie(top_categories.values, labels=top_categories.index, autopct='%1.1f%%',
            startangle=90, colors=colors, textprops={'fontsize': 10})
axes[1].set_title('Distribución de Categorías (Top 10)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(figures_path / 'categorias_restaurantes.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: categorias_restaurantes.png")
print(f"   - Total categorías: {df['category_clean'].nunique()}")

# ============================================================================
# 8. VISUALIZACIÓN 6: RATINGS POR CATEGORÍA
# ============================================================================
print("\n" + "="*70)
print("8. GENERANDO VISUALIZACIÓN 6: Ratings por Categoría")
print("="*70)

top_10_categories = category_counts.head(10).index
df_top_cat = df[df['category_clean'].isin(top_10_categories)]

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

sns.boxplot(data=df_top_cat, y='category_clean', x='stars', ax=axes[0],
            palette='Set2', order=top_10_categories)
axes[0].set_xlabel('Rating (Estrellas)', fontsize=12)
axes[0].set_ylabel('Categoría', fontsize=12)
axes[0].set_title('Distribución de Ratings por Categoría', fontsize=14, fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

category_stats = df_top_cat.groupby('category_clean')['stars'].mean().sort_values(ascending=True)
category_stats.plot(kind='barh', ax=axes[1], color='#e74c3c', edgecolor='black')
axes[1].set_xlabel('Rating Promedio', fontsize=12)
axes[1].set_ylabel('Categoría', fontsize=12)
axes[1].set_title('Rating Promedio por Categoría', fontsize=14, fontweight='bold')
axes[1].grid(axis='x', alpha=0.3)
axes[1].axvline(df['stars'].mean(), color='blue', linestyle='--', linewidth=2, label='Media global')
axes[1].legend()

plt.tight_layout()
plt.savefig(figures_path / 'ratings_por_categoria.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: ratings_por_categoria.png")

# ============================================================================
# 9. VISUALIZACIÓN 7: DISTRITOS
# ============================================================================
print("\n" + "="*70)
print("9. GENERANDO VISUALIZACIÓN 7: Distribución por Distritos")
print("="*70)

district_counts = df['district'].value_counts().head(20)

plt.figure(figsize=(14, 8))
district_counts.plot(kind='barh', color='#16a085', edgecolor='black')
plt.xlabel('Cantidad de Restaurantes', fontsize=12)
plt.ylabel('Distrito', fontsize=12)
plt.title('Top 20 Distritos con Más Restaurantes', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(figures_path / 'distritos_restaurantes.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: distritos_restaurantes.png")
print(f"   - Total distritos: {df['district'].nunique()}")

# ============================================================================
# 10. VISUALIZACIÓN 8: MAPA GEOESPACIAL
# ============================================================================
print("\n" + "="*70)
print("10. GENERANDO VISUALIZACIÓN 8: Mapa Geoespacial")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

scatter = axes[0].scatter(df['long'], df['lat'],
                         c=df['stars'], cmap='RdYlGn',
                         s=df['reviews']/50, alpha=0.6,
                         edgecolors='black', linewidth=0.5)
axes[0].set_xlabel('Longitud', fontsize=12)
axes[0].set_ylabel('Latitud', fontsize=12)
axes[0].set_title('Mapa de Restaurantes por Rating\n(tamaño = número de reviews)',
                  fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)
cbar1 = plt.colorbar(scatter, ax=axes[0])
cbar1.set_label('Rating (Estrellas)', fontsize=11)

scatter2 = axes[1].scatter(df['long'], df['lat'],
                          c=df['popularity_score'], cmap='plasma',
                          s=df['reviews']/50, alpha=0.6,
                          edgecolors='black', linewidth=0.5)
axes[1].set_xlabel('Longitud', fontsize=12)
axes[1].set_ylabel('Latitud', fontsize=12)
axes[1].set_title('Mapa de Restaurantes por Popularity Score\n(tamaño = número de reviews)',
                  fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
cbar2 = plt.colorbar(scatter2, ax=axes[1])
cbar2.set_label('Popularity Score', fontsize=11)

center_lat, center_long = -12.0464, -77.0428
axes[0].scatter(center_long, center_lat, marker='*', s=500, c='red',
               edgecolors='black', linewidth=2, label='Centro de Lima', zorder=5)
axes[0].legend(fontsize=10)
axes[1].scatter(center_long, center_lat, marker='*', s=500, c='red',
               edgecolors='black', linewidth=2, zorder=5)

plt.tight_layout()
plt.savefig(figures_path / 'mapa_geoespacial.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: mapa_geoespacial.png")

# ============================================================================
# 11. VISUALIZACIÓN 9: DISTANCIA VS RATING
# ============================================================================
print("\n" + "="*70)
print("11. GENERANDO VISUALIZACIÓN 9: Distancia vs Rating")
print("="*70)

fig, ax = plt.subplots(figsize=(12, 6))
scatter = ax.scatter(df['distance_to_center_km'], df['stars'],
                    c=df['reviews'], cmap='viridis', s=100, alpha=0.6,
                    edgecolors='black', linewidth=0.5)
ax.set_xlabel('Distancia al Centro de Lima (km)', fontsize=12)
ax.set_ylabel('Rating (Estrellas)', fontsize=12)
ax.set_title('Relación entre Distancia al Centro y Rating', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Número de Reviews', fontsize=11)

z = np.polyfit(df['distance_to_center_km'], df['stars'], 1)
p = np.poly1d(z)
ax.plot(df['distance_to_center_km'], p(df['distance_to_center_km']),
        "r--", linewidth=2, label='Tendencia')
ax.legend()

plt.tight_layout()
plt.savefig(figures_path / 'distancia_vs_rating.png', dpi=300, bbox_inches='tight')
plt.close()

corr_dist_rating = df[['distance_to_center_km', 'stars']].corr().iloc[0, 1]
print(f"✅ Guardado: distancia_vs_rating.png")
print(f"   - Correlación Distancia-Rating: {corr_dist_rating:.3f}")

# ============================================================================
# 12. VISUALIZACIÓN 10: TOP RESTAURANTES
# ============================================================================
print("\n" + "="*70)
print("12. GENERANDO VISUALIZACIÓN 10: Top Restaurantes")
print("="*70)

top_15 = df.nlargest(15, 'popularity_score')

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top_15)), top_15['popularity_score'], color='#e67e22', edgecolor='black')
ax.set_yticks(range(len(top_15)))
ax.set_yticklabels(top_15['title'], fontsize=10)
ax.set_xlabel('Popularity Score', fontsize=12)
ax.set_title('Top 15 Restaurantes por Popularity Score', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for i, (bar, score) in enumerate(zip(bars, top_15['popularity_score'])):
    ax.text(score + 0.1, i, f'{score:.2f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(figures_path / 'top_restaurantes.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: top_restaurantes.png")

# ============================================================================
# 13. VISUALIZACIÓN 11: DISTRIBUCIÓN DE TIERS
# ============================================================================
print("\n" + "="*70)
print("13. GENERANDO VISUALIZACIÓN 11: Distribución de Tiers")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

quality_counts = df['quality_tier'].value_counts()
colors_quality = ['#2ecc71', '#f39c12', '#e74c3c']
axes[0].pie(quality_counts.values, labels=quality_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors_quality, textprops={'fontsize': 12})
axes[0].set_title('Distribución por Quality Tier', fontsize=14, fontweight='bold')

review_counts = df['review_tier'].value_counts()
colors_review = plt.cm.Blues(np.linspace(0.3, 0.9, len(review_counts)))
axes[1].pie(review_counts.values, labels=review_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors_review, textprops={'fontsize': 12})
axes[1].set_title('Distribución por Review Tier', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(figures_path / 'distribucion_tiers.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Guardado: distribucion_tiers.png")

# ============================================================================
# 14. EXPORTAR RESUMEN
# ============================================================================
print("\n" + "="*70)
print("14. EXPORTANDO RESUMEN EJECUTIVO")
print("="*70)

summary_file = Path('docs/eda_summary.txt')
summary_file.parent.mkdir(parents=True, exist_ok=True)

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("="*100 + "\n")
    f.write("RESUMEN EJECUTIVO - ANÁLISIS EXPLORATORIO DE DATOS\n")
    f.write("Sistema de Recomendación de Restaurantes - Lima\n")
    f.write("="*100 + "\n\n")

    f.write(f"Dataset: {len(df)} restaurantes de alta calidad\n")
    f.write(f"Reviews: {df_reviews.shape[0]:,} reseñas individuales\n")
    f.write(f"Distritos: {df['district'].nunique()}\n")
    f.write(f"Categorías: {df['category_clean'].nunique()}\n\n")

    f.write("MÉTRICAS CLAVE:\n")
    f.write(f"  - Rating promedio: {df['stars'].mean():.2f} ⭐\n")
    f.write(f"  - Reviews promedio: {df['reviews'].mean():.0f}\n")
    f.write(f"  - Popularity score promedio: {df['popularity_score'].mean():.2f}\n")
    f.write(f"  - Distancia promedio al centro: {df['distance_to_center_km'].mean():.2f} km\n\n")

    f.write("TOP 10 RESTAURANTES:\n")
    top_10 = df.nlargest(10, 'popularity_score')
    for i, row in enumerate(top_10.itertuples(), 1):
        f.write(f"  {i}. {row.title}: {row.stars}⭐ ({row.reviews} reviews) - Score: {row.popularity_score}\n")

    f.write("\n" + "="*100 + "\n")
    f.write("CORRELACIONES:\n")
    f.write(f"  - Reviews vs Rating: {pearson_corr:.3f}\n")
    f.write(f"  - Distancia vs Rating: {corr_dist_rating:.3f}\n\n")

    f.write("TOP 5 CATEGORÍAS:\n")
    for i, (cat, count) in enumerate(category_counts.head(5).items(), 1):
        pct = (count / len(df)) * 100
        f.write(f"  {i}. {cat}: {count} ({pct:.1f}%)\n")

    f.write("\nTOP 5 DISTRITOS:\n")
    for i, (dist, count) in enumerate(district_counts.head(5).items(), 1):
        pct = (count / len(df)) * 100
        f.write(f"  {i}. {dist}: {count} ({pct:.1f}%)\n")

print(f"✅ Resumen exportado: {summary_file}")

# ============================================================================
# 15. CONCLUSIONES
# ============================================================================
print("\n" + "="*70)
print("📋 CONCLUSIONES DEL ANÁLISIS EXPLORATORIO")
print("="*70)

print(f"\n✅ {len(df)} restaurantes de alta calidad analizados")
print(f"✅ {df['district'].nunique()} distritos de Lima cubiertos")
print(f"✅ {df['category_clean'].nunique()} categorías de restaurantes")
print(f"✅ {df_reviews.shape[0]:,} reviews individuales disponibles")

print(f"\n📊 Rating promedio: {df['stars'].mean():.2f} ⭐")
print(f"📊 Reviews promedio: {df['reviews'].mean():.0f}")
print(f"📊 Popularity score: {df['popularity_score'].mean():.2f}")

print(f"\n📊 Correlación Reviews-Rating: {pearson_corr:.3f} (débil)")
print(f"📊 Correlación Distancia-Rating: {corr_dist_rating:.3f}")

print("\n🏆 TOP 5 RESTAURANTES:")
top_5 = df.nlargest(5, 'popularity_score')
for i, row in enumerate(top_5.itertuples(), 1):
    print(f"   {i}. {row.title}: {row.stars}⭐ ({row.reviews} reviews) - Score: {row.popularity_score}")

print("\n" + "="*70)
print("✅ ANÁLISIS EXPLORATORIO COMPLETADO")
print(f"📁 11 visualizaciones guardadas en: {figures_path}")
print(f"📄 Resumen exportado en: {summary_file}")
print("="*70)

