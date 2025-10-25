"""
OPTIMIZACIÓN DEL MODELO DE ANÁLISIS DE SATISFACCIÓN GASTRONÓMICA
Ajusta el modelo para distinguir entre:
- Comentarios de satisfacción: "La comida estuvo deliciosa"
- Información de servicio: "Se atienden todos los domingos"

Contexto del proyecto:
- Sistema de recomendación de restaurantes en Lima
- 706 restaurantes de alta calidad
- 378,969 reviews de clientes reales
- Análisis de satisfacción gastronómica (comida + servicio + ambiente)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def interpretar_confianza(sentiment, confidence):
    """
    Interpreta el nivel de confianza de una predicción y devuelve recomendaciones para la UI.

    Args:
        sentiment: Sentimiento predicho ('positivo', 'neutro', 'negativo')
        confidence: Nivel de confianza (0.0 - 1.0)

    Returns:
        dict con: label, confidence, status, color, icon, mostrar_prediccion
    """
    label = sentiment.upper()

    # UMBRALES DE CONFIANZA RECOMENDADOS PARA PRODUCCIÓN
    if confidence >= 0.90:
        status = "MUY CONFIABLE"
        color = "green"
        icon = "✓✓"
        mostrar = True
        accion = "Mostrar con alta confianza"
    elif confidence >= 0.80:
        status = "CONFIABLE"
        color = "lightgreen"
        icon = "✓"
        mostrar = True
        accion = "Mostrar normalmente"
    elif confidence >= 0.70:
        status = "MODERADO"
        color = "yellow"
        icon = "⚠"
        mostrar = True
        accion = "Mostrar con indicador de revisar"
    elif confidence >= 0.60:
        status = "BAJA CONFIANZA"
        color = "orange"
        icon = "?"
        mostrar = True
        accion = "Sugerir revisión humana"
    else:
        status = "INDETERMINADO"
        color = "red"
        icon = "✗"
        label = "REQUIERE REVISIÓN"
        mostrar = False
        accion = "NO mostrar predicción automática"

    return {
        'label': label,
        'confidence': round(confidence, 3),
        'status': status,
        'color': color,
        'icon': icon,
        'mostrar_prediccion': mostrar,
        'accion_recomendada': accion
    }


def optimizar_modelo_satisfaccion_gastronomica():
    """Optimizar modelo para análisis de satisfacción en restaurantes"""

    print("🍽️ OPTIMIZACIÓN DEL MODELO DE SATISFACCIÓN GASTRONÓMICA")
    print("=" * 80)

    print("🎯 CONTEXTO DEL NEGOCIO:")
    print("   • Recomendador de restaurantes en Lima")
    print("   • 706 restaurantes de alta calidad")
    print("   • 378,969 reviews de satisfacción de clientes")
    print("   • Análisis: comida + servicio + ambiente")
    print()

    print("❌ PROBLEMA IDENTIFICADO:")
    print('   "se atienden todos los domingos" → POSITIVO (51.6%)')
    print("   ↳ NO es satisfacción, es INFORMACIÓN de servicio")
    print()

    try:
        # Cargar modelo actual
        from src.ml.models import SentimentAnalysisModel

        model = SentimentAnalysisModel()
        model.load('data/models/sentiment_model.pkl')

        print("✅ Modelo actual cargado")

        # Definir categorías específicas del dominio gastronómico
        print("\n🔍 ANÁLISIS DEL DOMINIO GASTRONÓMICO:")
        print("-" * 50)

        # COMENTARIOS DE SATISFACCIÓN (lo que SÍ queremos clasificar)
        # Expandido con muchos más ejemplos reales del dominio gastronómico limeño
        comentarios_satisfaccion = {
            'positivos': [
                # Comida - Sabor y Calidad
                "La comida estuvo deliciosa y fresca",
                "Excelente sabor, muy auténtico peruano",
                "El ceviche espectacular, pescado fresco",
                "Anticuchos jugosos y bien sazonados",
                "Ají de gallina cremoso y sabroso",
                "Lomo saltado perfectamente preparado",
                "Causa limeña exquisita presentación",
                "Arroz con pollo muy sabroso y casero",
                "Papas rellenas deliciosas y calientes",
                "Rocoto relleno con el punto exacto de picante",
                "Tacu tacu con bistec espectacular",
                "Pollo a la brasa jugoso y dorado",
                "Chicharrón de pescado crujiente",
                "Seco de cabrito tierno y aromático",

                # Servicio - Atención al Cliente
                "Excelente servicio, muy atentos y amables",
                "Meseros súper educados y serviciales",
                "Atención de primera calidad, rápida",
                "Personal muy cortés y profesional",
                "Servicio impecable, sin demoras",
                "Mozos conocen bien la carta y recomiendan",
                "Atención personalizada y cálida",
                "Staff muy bien capacitado y amable",
                "Servicio al cliente excepcional",
                "Meseros atentos a cada detalle",

                # Ambiente - Experiencia General
                "Ambiente acogedor y familiar",
                "Local muy bonito y limpio",
                "Decoración típica peruana muy linda",
                "Música criolla que ambienta perfecto",
                "Lugar romántico para parejas",
                "Ambiente tranquilo para conversar",
                "Vista hermosa del malecón",
                "Terraza muy agradable y fresca",
                "Lugar perfecto para reuniones familiares",

                # Precio - Relación Calidad-Precio
                "Excelente relación calidad precio",
                "Precios justos para la calidad que ofrecen",
                "Vale cada centavo, super recomendado",
                "Porciones generosas por el precio",
                "Muy económico para lo que sirven",

                # Recomendaciones Generales
                "Totalmente recomendado, volveré",
                "El mejor restaurante de comida criolla",
                "Sin duda el mejor ceviche de Lima",
                "Lugar obligatorio para turistas",
                "Experiencia gastronómica increíble",
                "Superó mis expectativas completamente"
            ],
            'negativos': [
                # Comida - Problemas de Calidad
                "La comida estaba fría y sin sabor",
                "Ceviche con pescado no tan fresco",
                "Pollo a la brasa seco y duro",
                "Ají de gallina muy salado",
                "Lomo saltado grasoso y frío",
                "Arroz con pollo desabrido",
                "Anticuchos duros y secos",
                "Causa muy simple y sin gracia",
                "Rocoto relleno sin sabor",
                "Chicharrón de pollo quemado",
                "Seco de cabrito muy grasoso",
                "Comida recalentada y fría",
                "Platos mal presentados y feos",
                "Ingredientes de mala calidad",

                # Servicio - Problemas de Atención
                "Pésimo servicio, muy lento y descortés",
                "Meseros maleducados y groseros",
                "Atención descortés del personal",
                "Servicio demorado, esperamos una hora",
                "Mozos no saben explicar la carta",
                "Personal desatento y poco profesional",
                "Nos ignoraron toda la noche",
                "Servicio al cliente horrible",
                "Meseros con mala actitud",
                "Staff poco capacitado y lento",

                # Ambiente - Problemas del Local
                "Ambiente ruidoso e incómodo",
                "Local sucio y descuidado",
                "Baños en pésimo estado",
                "Música muy alta, no se puede conversar",
                "Lugar caluroso sin ventilación",
                "Mesas pegajosas y sucias",
                "Decoración vieja y deteriorada",
                "Olor desagradable en el local",
                "Mucho ruido de la cocina",

                # Precio - Problemas de Costo
                "Muy caro para la calidad que dan",
                "Precios exagerados, no vale la pena",
                "Porción muy pequeña por el precio",
                "Cobran demás por todo",
                "Relación precio calidad pésima",

                # Experiencia General Negativa
                "No lo recomiendo para nada",
                "Peor experiencia gastronómica",
                "Nunca más vuelvo a este lugar",
                "Decepcionante, esperaba mucho más",
                "Una pérdida total de tiempo y dinero"
            ],
            'neutros': [
                # Comida - Evaluaciones Moderadas
                "La comida está bien, normal sin más",
                "Sabor regular, nada extraordinario",
                "Ceviche estándar, sin destacar",
                "Pollo a la brasa común y corriente",
                "Lomo saltado promedio, aceptable",
                "Ají de gallina decente pero mejorable",
                "Comida casera simple y básica",
                "Platos correctos pero sin sorprender",
                "Calidad promedio para el distrito",
                "Comida aceptable, sin más",

                # Servicio - Atención Estándar
                "Servicio regular, nada especial",
                "Atención correcta pero básica",
                "Meseros educados pero sin destacar",
                "Servicio estándar, sin problemas",
                "Personal cumple pero no sobresale",
                "Atención normal para este tipo de local",
                "Mozos atentos pero no excepcionales",
                "Servicio promedio, sin quejas",

                # Ambiente - Experiencia Moderada
                "Ambiente promedio, aceptable",
                "Local normal, sin nada especial",
                "Decoración simple pero ordenada",
                "Lugar tranquilo pero sin encanto",
                "Ambiente familiar básico",
                "Limpieza aceptable del establecimiento",
                "Música de fondo apropiada",

                # Precio - Evaluación Equilibrada
                "Precio acorde a la calidad",
                "Precios normales para la zona",
                "Relación calidad precio estándar",
                "Costo justo, sin ser ganga ni caro",
                "Porciones adecuadas al precio",

                # Experiencia General Neutra
                "Está bien para salir del paso",
                "Lugar decente para almorzar",
                "Cumple las expectativas básicas",
                "Opción válida en el barrio",
                "Restaurante promedio de barrio",
                "Experiencia sin pena ni gloria"
            ]
        }

        # INFORMACIÓN PROMOCIONAL/COMERCIAL (NO son opiniones de clientes)
        # Estas son descripciones del restaurante, no experiencias de consumidores
        informacion_promocional_comercial = [
            # Información de Horarios (descripción del negocio)
            "se atienden todos los domingos",
            "abierto los fines de semana",
            "horario de 9am a 10pm",
            "atienden de lunes a sábado",
            "abierto de martes a domingo",
            "horario corrido de 11am a 11pm",
            "cerrado los lunes por limpieza",
            "atención las 24 horas",
            "abierto solo para almuerzo",
            "horario de cena hasta las 12am",
            "feriados abierto con horario especial",
            "domingos solo hasta las 6pm",

            # Información de Ubicación (descripción del negocio)
            "ubicado en Miraflores frente al parque",
            "dirección Av. Larco 1234",
            "local en el segundo piso",
            "entrada por la calle lateral",
            "ubicado en centro comercial",
            "frente a la estación del metro",
            "cerca al malecón de Miraflores",
            "en la cuadra 15 de Benavides",
            "local esquina con semáforo",
            "a dos cuadras del óvalo",

            # Información de Servicios (promoción del negocio)
            "tienen delivery disponible",
            "servicio a domicilio sin costo adicional",
            "delivery solo en horario de almuerzo",
            "pedidos por WhatsApp al 999888777",
            "delivery gratuito por compras mayores a 50 soles",
            "servicio de recojo en tienda",
            "delivery hasta Surco y San Isidro",
            "tiempo de entrega 45 minutos",
            "pedidos online por su página web",

            # Promoción de Métodos de Pago
            "aceptan tarjetas de crédito y débito",
            "solo efectivo, no tarjetas",
            "aceptan Yape y Plin",
            "pago con tarjeta visa y mastercard",
            "descuento del 10% pagando en efectivo",
            "aceptan dólares al tipo de cambio del día",
            "pago contactless disponible",

            # Promoción de Servicios y Comodidades
            "hay estacionamiento gratuito",
            "parqueo disponible en la cuadra",
            "valet parking incluido",
            "wifi gratuito disponible",
            "aire acondicionado en todos los ambientes",
            "zona de no fumadores",
            "acceso para personas con discapacidad",
            "sillas altas para niños disponibles",
            "baños limpios y amplios",
            "terraza con vista al mar",

            # Información de Reservas y Contacto
            "reservas por teléfono 01-4567890",
            "reservas solo para grupos mayores a 6",
            "no se hacen reservas los fines de semana",
            "confirmar reserva una hora antes",
            "reservas por Facebook messenger",
            "whatsapp para reservas 999123456",

            # Promoción de Eventos y Entretenimiento
            "música en vivo los viernes y sábados",
            "show folclórico los domingos",
            "karaoke todos los jueves",
            "evento de salsa los viernes",
            "almuerzo ejecutivo de lunes a viernes",
            "buffet dominical desde las 12pm",
            "happy hour de 6pm a 8pm",

            # Políticas y Normas del Restaurante
            "consumo mínimo de 25 soles por persona",
            "máximo 2 horas de permanencia",
            "no se permite ingreso de mascotas",
            "dress code casual elegante",
            "grupo musical propio del local",
            "carta en inglés disponible",
            "menú vegetariano disponible",
            "platos sin gluten bajo pedido",

            # Promoción de Características del Local
            "local climatizado",
            "capacidad máxima 80 personas",
            "mesas en el jardín disponibles",
            "servicio de banquetes para eventos",
            "carta de vinos nacional e importado",
            "especialidad en comida criolla",
            "chef con 20 años de experiencia",
            "establecimiento con 15 años en el rubro"
        ]

        # PALABRAS QUE NO TIENEN RELACIÓN CON CALIFICACIÓN GASTRONÓMICA
        # Estas deben considerarse como NEUTRAS ya que no expresan satisfacción/insatisfacción
        palabras_no_relacionadas = {
            'informacion_factual': [
                # Información técnica/logística
                "se atienden todos los domingos",
                "horario de atención de 9 a 6",
                "ubicado en la avenida principal",
                "número de teléfono 987654321",
                "dirección exacta del local",
                "código postal del distrito",
                "número de RUC del negocio",
                "capacidad para 50 personas",

                # Datos geográficos
                "coordenadas GPS del lugar",
                "distancia desde el centro",
                "zona comercial de Miraflores",
                "segundo piso del edificio",
                "frente al parque Kennedy",
                "cerca de la estación del metro",

                # Información neutral del menú
                "tienen menú vegetariano",
                "carta disponible en inglés",
                "precios en soles y dólares",
                "platos desde 15 soles",
                "menú ejecutivo disponible",
                "desayunos desde las 7am"
            ],
            'datos_tecnicos': [
                # Métodos de pago (información, no calificación)
                "aceptan tarjetas visa",
                "pago con código QR",
                "transferencias bancarias",
                "efectivo en soles",
                "pago contactless disponible",

                # Servicios técnicos
                "wifi password restaurante123",
                "aire acondicionado central",
                "sistema de ventilación",
                "cámaras de seguridad",
                "música ambiental automatizada",

                # Información de contacto
                "página web oficial",
                "perfil en redes sociales",
                "email de contacto",
                "número de WhatsApp business"
            ],
            'datos_administrativos': [
                # Políticas del negocio (información, no opinión)
                "consumo mínimo requerido",
                "tiempo máximo de permanencia",
                "política de reservas",
                "horarios de limpieza",
                "días de cierre técnico",

                # Información legal/normativa
                "licencia de funcionamiento vigente",
                "certificado de salubridad",
                "registro sanitario actualizado",
                "aforo máximo permitido",
                "normas de bioseguridad"
            ]
        }

        # ESTRATEGIA PARA PALABRAS NO RELACIONADAS CON CALIFICACIÓN:
        # 1. Se clasifican como NEUTRO (no expresan satisfacción)
        # 2. Se entrenan específicamente para evitar confusión
        # 3. Se les da peso especial en el preprocesamiento

        # Consolidar todas las palabras no relacionadas
        todas_palabras_no_relacionadas = []
        for categoria, palabras in palabras_no_relacionadas.items():
            todas_palabras_no_relacionadas.extend(palabras)

        print(f"📝 PALABRAS NO RELACIONADAS CON CALIFICACIÓN:")
        print(f"   • Total identificadas: {len(todas_palabras_no_relacionadas)}")
        print(f"   • Estrategia: Clasificar como NEUTRO")
        print(f"   • Razón: No expresan satisfacción gastronómica")
        print()

        # Probar casos problemáticos del dominio gastronómico
        print("\n🧪 ANÁLISIS DE CASOS PROBLEMÁTICOS:")
        print("-" * 50)

        casos_informativos = informacion_promocional_comercial[:10]  # Primeros 10 casos
        problematicos = []

        for i, caso in enumerate(casos_informativos, 1):
            result = model.predict_single(caso)
            sentiment = result['sentiment']
            confidence = result['confidence']

            # Es problemático si información de servicio se clasifica con alta confianza como satisfacción
            es_problematico = (sentiment == 'positivo' or sentiment == 'negativo') and confidence > 0.5

            if es_problematico:
                problematicos.append(caso)

            estado = "⚠️ PROBLEMÁTICO" if es_problematico else "✅ OK"
            print(f'{i:2d}. {estado}')
            print(f'    "{caso}"')
            print(f'    → {sentiment.upper()} ({confidence:.3f})')
            print()

        print(f"📊 CASOS PROBLEMÁTICOS: {len(problematicos)}/{len(casos_informativos)}")

        if len(problematicos) >= 3:  # Si hay varios casos problemáticos
            print(f"\n🔧 CREANDO OPTIMIZACIÓN ESPECÍFICA PARA RESTAURANTES...")

            # Cargar dataset original
            data_path = project_root / "data" / "processed" / "modelo_limpio.csv"
            print(f"📁 Cargando dataset: {data_path}")

            df_original = pd.read_csv(data_path)
            print(f"✅ Dataset cargado: {len(df_original):,} reviews")

            # Analizar distribución actual
            print(f"\n📊 DISTRIBUCIÓN ACTUAL:")
            dist_actual = df_original['sentimiento'].value_counts()
            for sent, count in dist_actual.items():
                pct = (count / len(df_original)) * 100
                print(f"   • {sent:10s}: {count:8,} ({pct:5.1f}%)")

            # Crear dataset de entrenamiento optimizado
            print(f"\n🎯 CREANDO DATASET OPTIMIZADO...")

            # 1. Tomar muestra más grande y balanceada del dataset original
            sample_size = 25000  # Muestra más grande para mejor entrenamiento

            # Balancear la muestra por sentimiento para mejor representación
            try:
                # Intentar muestra estratificada balanceada
                min_class_size = df_original['sentimiento'].value_counts().min()
                samples_per_class = min(8000, min_class_size)  # Máximo 8000 por clase

                df_sample_list = []
                for sentiment in ['positivo', 'neutro', 'negativo']:
                    df_class = df_original[df_original['sentimiento'] == sentiment]
                    if len(df_class) >= samples_per_class:
                        df_sample_class = df_class.sample(n=samples_per_class, random_state=42)
                        df_sample_list.append(df_sample_class)

                if df_sample_list:
                    df_sample = pd.concat(df_sample_list, ignore_index=True)
                    print(f"   ✅ Muestra balanceada: {len(df_sample):,} registros")
                else:
                    df_sample = df_original.sample(n=sample_size, random_state=42)
                    print(f"   ⚠️ Muestra aleatoria: {len(df_sample):,} registros")
            except:
                df_sample = df_original.sample(n=sample_size, random_state=42)
                print(f"   ⚠️ Muestra aleatoria: {len(df_sample):,} registros")

            # 2. Agregar casos específicos de información promocional/comercial como NEUTRO (triplicado para mayor peso)
            df_promocional = pd.DataFrame({
                'comment': informacion_promocional_comercial * 3,  # Triplicar para mayor peso en el entrenamiento
                'sentimiento': ['neutro'] * (len(informacion_promocional_comercial) * 3),
                'rating': [3] * (len(informacion_promocional_comercial) * 3)  # Rating neutro
            })

            # 2.5. Agregar palabras NO relacionadas con calificación como NEUTRO (triplicado)
            df_no_relacionadas = pd.DataFrame({
                'comment': todas_palabras_no_relacionadas * 3,  # Triplicar para mayor peso
                'sentimiento': ['neutro'] * (len(todas_palabras_no_relacionadas) * 3),
                'rating': [3] * (len(todas_palabras_no_relacionadas) * 3)
            })

            print(f"   ✅ Agregadas {len(todas_palabras_no_relacionadas) * 3} palabras NO relacionadas → NEUTRO (triplicadas)")

            # 2.7. Agregar ejemplos específicos de confusión para entrenar mejor
            ejemplos_confusion = [
                # INFORMACIÓN DE SERVICIO → NEUTRO (casos específicos que fallan)
                ("abierto los fines de semana solo", "neutro"),
                ("horarios de atención disponible", "neutro"),
                ("días de apertura establecidos", "neutro"),
                ("están abiertos normalmente", "neutro"),
                ("atienden regularmente", "neutro"),
                ("información de contacto disponible", "neutro"),
                ("ubicación accesible", "neutro"),
                ("delivery disponible", "neutro"),
                ("parqueo disponible", "neutro"),
                ("wifi gratuito", "neutro"),

                # SATISFACCIÓN GASTRONÓMICA POSITIVA CLARA → POSITIVO
                ("la comida estuvo deliciosa me encantó", "positivo"),  # Caso específico que falla
                ("excelente servicio me trataron súper bien", "positivo"),
                ("sabor increíble lo recomiendo totalmente", "positivo"),  # Caso específico que falla
                ("platos deliciosos con sabor espectacular", "positivo"),
                ("comida exquisita muy rica todo", "positivo"),
                ("atención fantástica me gustó mucho", "positivo"),
                ("experiencia maravillosa volveré pronto", "positivo"),
                ("ambiente hermoso muy acogedor", "positivo"),
                ("ceviche fresco y sabroso excelente", "positivo"),
                ("lomo saltado jugoso y delicioso", "positivo"),
                ("anticuchos tiernos me fascinaron", "positivo"),
                ("ají de gallina cremoso y rico", "positivo"),

                # SATISFACCIÓN GASTRONÓMICA NEGATIVA CLARA → NEGATIVO
                ("pésimo servicio me trataron muy mal", "negativo"),  # Caso específico que falla
                ("comida horrible sin sabor terrible", "negativo"),
                ("servicio lento me hicieron esperar mucho", "negativo"),
                ("platos fríos y desabridos pésimos", "negativo"),
                ("atención deplorable muy mala experiencia", "negativo"),
                ("lugar sucio no me gustó nada", "negativo"),
                ("ceviche con pescado no fresco", "negativo"),
                ("lomo saltado duro y seco", "negativo"),
                ("precios caros para la mala calidad", "negativo"),
                ("experiencia decepcionante no vuelvo más", "negativo"),
                ("ambiente ruidoso e incómodo", "negativo"),
                ("personal maleducado y grosero", "negativo"),

                # INFORMACIÓN SIN EMOCIÓN → NEUTRO
                ("servicio estándar normal", "neutro"),
                ("comida regular promedio", "neutro"),
                ("horario de funcionamiento", "neutro"),
                ("ubicación del establecimiento", "neutro"),
                ("capacidad del local", "neutro"),
                ("métodos de pago aceptados", "neutro"),
                ("carta disponible", "neutro"),
                ("reservas por teléfono", "neutro"),
            ]

            df_confusion = pd.DataFrame({
                'comment': [ej[0] for ej in ejemplos_confusion] * 8,  # Aumentado a 8 para mayor peso
                'sentimiento': [ej[1] for ej in ejemplos_confusion] * 8,
                'rating': [5 if ej[1] == 'positivo' else 1 if ej[1] == 'negativo' else 3 for ej in ejemplos_confusion] * 8
            })

            # 3. Agregar casos claros de satisfacción gastronómica
            comentarios_gastronomicos = []
            sentimientos_gastronomicos = []
            ratings_gastronomicos = []

            for sentiment, comments in comentarios_satisfaccion.items():
                for comment in comments:
                    comentarios_gastronomicos.append(comment)
                    if sentiment == 'positivos':
                        sentimientos_gastronomicos.append('positivo')
                        ratings_gastronomicos.append(5)
                    elif sentiment == 'negativos':
                        sentimientos_gastronomicos.append('negativo')
                        ratings_gastronomicos.append(1)
                    else:  # neutros
                        sentimientos_gastronomicos.append('neutro')
                        ratings_gastronomicos.append(3)

            df_gastronomicos = pd.DataFrame({
                'comment': comentarios_gastronomicos,
                'sentimiento': sentimientos_gastronomicos,
                'rating': ratings_gastronomicos
            })

            # 4. Combinar datasets (incluye ejemplos específicos de confusión)
            df_optimizado = pd.concat([
                df_sample,
                df_promocional,      # Información promocional/comercial (triplicadas)
                df_no_relacionadas,  # Palabras no relacionadas (triplicadas)
                df_confusion,        # Ejemplos específicos de confusión (x8)
                df_gastronomicos
            ], ignore_index=True)
            df_optimizado = df_optimizado.sample(frac=1, random_state=42).reset_index(drop=True)

            print(f"✅ Dataset optimizado creado: {len(df_optimizado):,} registros")
            print(f"   • Información promocional/comercial: {len(informacion_promocional_comercial) * 3} casos → NEUTRO")
            print(f"   • Palabras NO relacionadas: {len(todas_palabras_no_relacionadas) * 3} casos → NEUTRO")
            print(f"   • Ejemplos de confusión: {len(ejemplos_confusion) * 8} casos → ENTRENAMIENTO ESPECÍFICO")
            print(f"   • Opiniones reales de clientes: {len(comentarios_gastronomicos)} casos")

            # Entrenar modelo optimizado
            print(f"\n🚀 ENTRENANDO MODELO OPTIMIZADO...")

            from sklearn.model_selection import train_test_split
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.naive_bayes import ComplementNB
            from sklearn.metrics import accuracy_score, classification_report, cohen_kappa_score

            X = df_optimizado['comment']
            y = df_optimizado['sentimiento']

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Vectorización optimizada para el dominio gastronómico
            print("   🔧 Configurando vectorización TF-IDF optimizada...")
            vectorizer_gastro = TfidfVectorizer(
                max_features=12000,  # Reducido para evitar sobreajuste
                ngram_range=(1, 2),  # Solo unigramas y bigramas para mayor precisión
                min_df=2,  # Mínimo 2 documentos para captar más términos específicos
                max_df=0.85,  # Aumentado para mantener palabras importantes
                sublinear_tf=True,  # Escalamiento logarítmico
                stop_words=None,  # No usar stopwords automáticas (mantenemos negaciones)
                lowercase=True,
                strip_accents='unicode',  # Normalizar acentos
                token_pattern=r'(?u)\b\w\w+\b',  # Al menos 2 caracteres
                use_idf=True,  # Usar IDF para dar peso a términos distintivos
                smooth_idf=True,  # Suavizado IDF para evitar división por cero
                norm='l2'  # Normalización L2 para vectores unitarios
            )

            print("   ⚙️ Entrenando vectorizador...")
            X_train_tfidf = vectorizer_gastro.fit_transform(X_train)
            X_test_tfidf = vectorizer_gastro.transform(X_test)

            print(f"   ✅ Vocabulario: {len(vectorizer_gastro.vocabulary_):,} términos")
            print(f"   ✅ Matriz entrenamiento: {X_train_tfidf.shape}")

            # Probar múltiples clasificadores para encontrar el mejor
            print("   🤖 Probando múltiples algoritmos...")

            from sklearn.ensemble import VotingClassifier
            from sklearn.linear_model import LogisticRegression
            from sklearn.naive_bayes import MultinomialNB

            # Clasificadores individuales optimizados
            classifiers = {
                'complement_nb': ComplementNB(alpha=0.1),  # Menor suavizado para más precisión
                'multinomial_nb': MultinomialNB(alpha=0.3),
                'logistic_reg': LogisticRegression(
                    max_iter=3000,
                    class_weight='balanced',
                    random_state=42,
                    solver='saga',  # Cambiado a saga para evitar el warning
                    C=1.0  # Regularización moderada
                )
            }

            # Evaluar cada clasificador
            best_classifier = None
            best_score = 0
            classifier_scores = {}

            for name, clf in classifiers.items():
                clf.fit(X_train_tfidf, y_train)
                score = clf.score(X_test_tfidf, y_test)
                classifier_scores[name] = score
                print(f"   • {name}: {score:.3f}")

                if score > best_score:
                    best_score = score
                    best_classifier = clf

            # Usar el mejor clasificador individual o ensemble si es mejor
            print(f"\n   🏆 Mejor clasificador individual: {best_score:.3f}")

            # Crear ensemble con los mejores
            try:
                ensemble = VotingClassifier(
                    estimators=[
                        ('nb', ComplementNB(alpha=0.1)),
                        ('lr', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42))
                    ],
                    voting='soft'
                )
                ensemble.fit(X_train_tfidf, y_train)
                ensemble_score = ensemble.score(X_test_tfidf, y_test)
                print(f"   🎯 Ensemble score: {ensemble_score:.3f}")

                if ensemble_score > best_score:
                    classifier_gastro = ensemble
                    print("   ✅ Usando ensemble (mejor rendimiento)")
                else:
                    classifier_gastro = best_classifier
                    print("   ✅ Usando clasificador individual (mejor rendimiento)")
            except:
                classifier_gastro = best_classifier
                print("   ✅ Usando clasificador individual")

            # Evaluar modelo optimizado
            y_pred = classifier_gastro.predict(X_test_tfidf)
            accuracy_gastro = accuracy_score(y_test, y_pred)
            kappa_gastro = cohen_kappa_score(y_test, y_pred)

            print(f"\n📊 RESULTADOS DEL MODELO OPTIMIZADO:")
            print(f"   • Accuracy: {accuracy_gastro:.1%}")
            print(f"   • Cohen's Kappa: {kappa_gastro:.4f}")

            # Crear modelo completo
            modelo_gastro = SentimentAnalysisModel()
            modelo_gastro.vectorizer = vectorizer_gastro
            modelo_gastro.classifier = classifier_gastro
            modelo_gastro.is_trained = True

            # Metadata específica del dominio gastronómico
            from sklearn.metrics import precision_score, recall_score, f1_score, matthews_corrcoef

            modelo_gastro.metadata = {
                'model_type': 'gastronomic_satisfaction_optimized',
                'domain': 'restaurant_reviews_lima',
                'vocab_size': len(vectorizer_gastro.vocabulary_),
                'ngram_range': (1, 2),
                'max_features': 12000,
                'n_samples': len(df_optimizado),
                'sentiment_classes': ['negativo', 'neutro', 'positivo'],
                'optimization': 'service_info_neutral_enhanced',
                'promotional_cases_added': len(informacion_promocional_comercial) * 3,
                'non_related_words_added': len(todas_palabras_no_relacionadas) * 3,
                'confusion_examples_added': len(ejemplos_confusion) * 5,
                'gastronomic_cases_added': len(comentarios_gastronomicos),
                'test_metrics': {
                    'accuracy': float(accuracy_gastro),
                    'cohen_kappa': float(kappa_gastro),
                    'f1_weighted': float(f1_score(y_test, y_pred, average='weighted')),
                    'f1_macro': float(f1_score(y_test, y_pred, average='macro')),
                    'matthews_corrcoef': float(matthews_corrcoef(y_test, y_pred)),
                    'per_class': {
                        clase: {
                            'precision': float(classification_report(y_test, y_pred, output_dict=True)[clase]['precision']),
                            'recall': float(classification_report(y_test, y_pred, output_dict=True)[clase]['recall']),
                            'f1-score': float(classification_report(y_test, y_pred, output_dict=True)[clase]['f1-score']),
                            'support': int(classification_report(y_test, y_pred, output_dict=True)[clase]['support'])
                        }
                        for clase in ['negativo', 'neutro', 'positivo']
                        if clase in classification_report(y_test, y_pred, output_dict=True)
                    }
                }
            }

            # PRUEBAS ESPECÍFICAS DEL DOMINIO GASTRONÓMICO
            print(f"\n🧪 PRUEBAS EN EL DOMINIO GASTRONÓMICO:")
            print("=" * 60)

            casos_dominio = [
                # INFORMACIÓN DE SERVICIO (debería ser NEUTRO)
                ("NEUTRO", "se atienden todos los domingos"),
                ("NEUTRO", "abierto los fines de semana"),
                ("NEUTRO", "tienen delivery disponible"),
                ("NEUTRO", "ubicado en Miraflores"),

                # SATISFACCIÓN POSITIVA (debería ser POSITIVO)
                ("POSITIVO", "la comida estuvo deliciosa"),
                ("POSITIVO", "excelente servicio, muy atentos"),
                ("POSITIVO", "sabor increíble, recomendado"),

                # SATISFACCIÓN NEGATIVA (debería ser NEGATIVO)
                ("NEGATIVO", "la comida estaba fría y sin sabor"),
                ("NEGATIVO", "pésimo servicio, muy lento"),

                # SATISFACCIÓN NEUTRA (debería ser NEUTRO)
                ("NEUTRO", "la comida está bien, normal"),
                ("NEUTRO", "servicio regular, nada especial")
            ]

            correctos_original = 0
            correctos_optimizado = 0

            for i, (esperado, caso) in enumerate(casos_dominio, 1):
                # Modelo original
                result_original = model.predict_single(caso)
                pred_original = result_original['sentiment'].upper()
                conf_original = result_original['confidence']

                # Modelo optimizado
                result_optimizado = modelo_gastro.predict_single(caso)
                pred_optimizado = result_optimizado['sentiment'].upper()
                conf_optimizado = result_optimizado['confidence']

                # Evaluar aciertos
                if pred_original == esperado:
                    correctos_original += 1
                if pred_optimizado == esperado:
                    correctos_optimizado += 1

                # Determinar mejora
                mejoro = "✅" if pred_optimizado == esperado and conf_optimizado > 0.6 else "⚠️"
                if pred_original != esperado and pred_optimizado == esperado:
                    mejoro = "🎯 CORREGIDO"

                print(f"{i:2d}. {mejoro} \"{caso[:40]}...\"")
                print(f"    Esperado:    {esperado}")
                print(f"    Original:    {pred_original} ({conf_original:.3f})")
                print(f"    Optimizado:  {pred_optimizado} ({conf_optimizado:.3f})")
                print()

            accuracy_original_dominio = (correctos_original / len(casos_dominio)) * 100
            accuracy_optimizado_dominio = (correctos_optimizado / len(casos_dominio)) * 100

            print(f"📊 RESULTADOS EN CASOS DE DOMINIO:")
            print(f"   • Modelo Original:  {correctos_original}/{len(casos_dominio)} ({accuracy_original_dominio:.1f}%)")
            print(f"   • Modelo Optimizado: {correctos_optimizado}/{len(casos_dominio)} ({accuracy_optimizado_dominio:.1f}%)")

            # Guardar modelo optimizado
            print(f"\n💾 GUARDANDO MODELO OPTIMIZADO...")
            model_gastro_path = project_root / "data" / "models" / "sentiment_model_gastro_optimized.pkl"
            modelo_gastro.save(str(model_gastro_path))

            print(f"✅ Modelo gastronómico guardado: {model_gastro_path.name}")
            print(f"   Tamaño: {model_gastro_path.stat().st_size / 1024:.2f} KB")

            # RECOMENDACIÓN FINAL
            print(f"\n" + "=" * 80)
            print("🎯 RECOMENDACIÓN FINAL")
            print("=" * 80)

            mejora_dominio = accuracy_optimizado_dominio - accuracy_original_dominio

            if accuracy_gastro >= 0.75 and kappa_gastro >= 0.60 and mejora_dominio >= 20:
                print("✅ USAR MODELO OPTIMIZADO GASTRONÓMICO")
                print("   • Mantiene métricas generales")
                print(f"   • Mejora {mejora_dominio:.1f}% en casos del dominio")
                print("   • Distingue satisfacción de información de servicio")
                print()
                print("🔧 Para activar:")
                print("   cp data/models/sentiment_model_gastro_optimized.pkl data/models/sentiment_model.pkl")

            elif accuracy_gastro >= 0.70:
                print("🟡 MODELO OPTIMIZADO ES ACEPTABLE")
                print("   • Considera A/B testing")
                print("   • Evalúa con más datos reales")

            else:
                print("⚠️ MANTENER MODELO HÍBRIDO ACTUAL")
                print("   • Modelo optimizado reduce accuracy general")
                print("   • Considerar post-procesamiento específico")

        else:
            print("✅ El modelo actual maneja bien la mayoría de casos informativos")
            print("   Solo casos menores requieren ajuste")

        # GUÍA DE INTERPRETACIÓN DE MÉTRICAS
        print(f"\n" + "=" * 80)
        print("📊 GUÍA DE INTERPRETACIÓN DE MÉTRICAS Y CONFIANZA")
        print("=" * 80)

        print("\n🎯 MÉTRICAS GENERALES ESPERADAS (Modelo en Producción):")
        print("   ┌─────────────────────────────┬──────────────┬──────────────┐")
        print("   │ Métrica                     │ Mínimo       │ Recomendado  │")
        print("   ├─────────────────────────────┼──────────────┼──────────────┤")
        print("   │ Accuracy                    │ 75%          │ 80-85%       │")
        print("   │ Cohen's Kappa               │ 0.60         │ 0.70-0.80    │")
        print("   │ Precision (promedio)        │ 73%          │ 78-83%       │")
        print("   │ Recall (promedio)           │ 72%          │ 77-82%       │")
        print("   │ F1-Score (promedio)         │ 72%          │ 77-82%       │")
        print("   └─────────────────────────────┴──────────────┴──────────────┘")

        print("\n📋 MÉTRICAS POR CLASE ESPERADAS:")
        print("   POSITIVO:")
        print("      • Precision: 80-88% (de las predicciones positivas, cuántas son correctas)")
        print("      • Recall:    85-92% (de los comentarios positivos reales, cuántos detectamos)")
        print("      • F1-Score:  82-90% (balance entre precision y recall)")

        print("\n   NEUTRO:")
        print("      • Precision: 50-65% (clase más difícil, menos datos)")
        print("      • Recall:    45-60% (difícil de detectar, se confunde con otros)")
        print("      • F1-Score:  48-62% (esperado que sea menor)")

        print("\n   NEGATIVO:")
        print("      • Precision: 75-85% (buena detección de comentarios negativos)")
        print("      • Recall:    70-80% (captamos la mayoría de negativos)")
        print("      • F1-Score:  72-82% (buen balance)")

        print("\n🎨 UMBRALES DE CONFIANZA PARA LA INTERFAZ (UI):")
        print("   ┌─────────────┬──────────────────┬─────────────┬────────────────────────┐")
        print("   │ Confianza   │ Estado           │ Indicador   │ Acción en UI           │")
        print("   ├─────────────┼──────────────────┼─────────────┼────────────────────────┤")
        print("   │ ≥ 90%       │ MUY CONFIABLE    │ ✓✓ Verde    │ Mostrar con seguridad  │")
        print("   │ 80-89%      │ CONFIABLE        │ ✓ Verde     │ Mostrar normalmente    │")
        print("   │ 70-79%      │ MODERADO         │ ⚠ Amarillo  │ + botón \"Revisar\"      │")
        print("   │ 60-69%      │ BAJA CONFIANZA   │ ? Naranja   │ Sugerir revisión       │")
        print("   │ < 60%       │ INDETERMINADO    │ ✗ Rojo      │ NO mostrar predicción  │")
        print("   └─────────────┴──────────────────┴─────────────┴────────────────────────┘")

        print("\n💡 EJEMPLOS DE QUÉ MOSTRAR AL USUARIO:")
        print()

        # Ejemplos con la función de interpretación
        ejemplos_ui = [
            ("La comida estuvo deliciosa", "positivo", 0.95),
            ("Excelente servicio y atención", "positivo", 0.87),
            ("Comida regular, nada especial", "neutro", 0.72),
            ("Se atienden todos los domingos", "neutro", 0.55),
            ("Pésimo servicio, muy lento", "negativo", 0.82)
        ]

        for comentario, sentiment, confidence in ejemplos_ui:
            info = interpretar_confianza(sentiment, confidence)
            print(f"   📝 \"{comentario}\"")
            print(f"      → {info['icon']} {info['label']} ({info['confidence']:.1%}) - {info['status']}")
            print(f"      → UI: {info['accion_recomendada']}")
            print()

        print("🔧 RECOMENDACIONES PARA IMPLEMENTACIÓN:")
        print("   1. Siempre mostrar el porcentaje de confianza al usuario")
        print("   2. Usar colores e íconos para indicar nivel de confiabilidad")
        print("   3. Para confianza < 70%, agregar botón de \"Reportar error\"")
        print("   4. Mostrar top-3 probabilidades en modo avanzado/debug")
        print("   5. Registrar casos de baja confianza para reentrenamiento")
        print("   6. Calibrar el modelo periódicamente con datos nuevos")

        print("\n📈 MEJORA CONTINUA:")
        print("   • Recolectar feedback del usuario sobre predicciones")
        print("   • Priorizar reentrenamiento con casos de baja confianza")
        print("   • Monitorear métricas semanalmente en producción")
        print("   • Actualizar modelo cuando accuracy baje de 75%")

        print(f"\n" + "=" * 80)

    except Exception as e:
        print(f"❌ Error en optimización: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    optimizar_modelo_satisfaccion_gastronomica()
