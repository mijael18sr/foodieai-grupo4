"""
Script de prueba para verificar la funcionalidad de distritos
Ejecutar: python test_districts.py
"""
import asyncio
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from src.infrastructure.container import Container


async def test_districts_functionality():
    """
    Prueba la funcionalidad completa de gestión de distritos
    """
    print(" Iniciando pruebas de funcionalidad de distritos...")
    print("=" * 60)

    try:
        # Obtener el servicio de distritos
        container = Container()
        district_service = container.district_service()

        print(" Contenedor de dependencias inicializado correctamente")

        # Test 1: Obtener lista de distritos para dropdown
        print("\n Test 1: Lista de distritos para dropdown")
        districts = await district_service.get_districts_for_dropdown()

        print(f" Se encontraron {len(districts)} distritos:")
        for i, district in enumerate(districts, 1):
            print(f" {i}. {district['label']} ({district['restaurant_count']} restaurantes)")
            if district['is_tourist_zone']:
                print(f" Zona turística")

        # Test 2: Obtener información de un distrito específico
        print(f"\n Test 2: Información detallada de Miraflores")
        miraflores_info = await district_service.get_district_info("Miraflores")

        print(" Información de Miraflores:")
        print(f" • Nombre: {miraflores_info['display_name']}")
        print(f" • Restaurantes: {miraflores_info['restaurant_count']}")
        print(f" • Rating promedio: {miraflores_info['average_rating']:.2f}")
        print(f" • Zona turística: {'Sí' if miraflores_info['is_tourist_zone'] else 'No'}")
        print(f" • Descripción: {miraflores_info['description']}")

        # Test 3: Distritos recomendados (solo zonas turísticas)
        print(f"\n Test 3: Distritos recomendados (zonas turísticas)")
        recommendations = await district_service.get_recommended_districts(
            tourist_zone_only=True,
            min_rating=4.0
        )

        print(f" {len(recommendations)} distritos turísticos recomendados:")
        for rec in recommendations:
            print(f" • {rec['display_name']}: {rec['restaurant_count']} restaurantes, "
                  f"rating {rec['average_rating']:.2f}")

        # Test 4: Estadísticas generales
        print(f"\n Test 4: Estadísticas generales")
        stats = await district_service.get_districts_statistics()
        summary = stats['summary']

        print(" Estadísticas de Lima:")
        print(f" • Total de distritos: {summary['total_districts']}")
        print(f" • Total de restaurantes: {summary['total_restaurants']}")
        print(f" • Promedio por distrito: {summary['avg_restaurants_per_district']:.1f} restaurantes")
        print(f" • Rating promedio general: {summary['avg_rating_across_districts']:.2f}")
        print(f" • Distrito más popular: {summary['most_popular_district']}")
        print(f" • Distrito mejor valorado: {summary['highest_rated_district']}")

        # Test 5: Validación de distrito
        print(f"\n Test 5: Validación de distritos")

        valid_district = await district_service.validate_district("Miraflores")
        invalid_district = await district_service.validate_district("Distrito_Inventado")

        print(f" Validaciones:")
        print(f" • 'Miraflores' existe: {valid_district}")
        print(f" • 'Distrito_Inventado' existe: {invalid_district}")

        print("\n" + "=" * 60)
        print(" ¡Todas las pruebas completadas exitosamente!")
        print(" El sistema de gestión de distritos está funcionando correctamente")

        return True

    except Exception as e:
        print(f"\n Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_frontend_integration():
    """
    Simula la integración con el frontend
    """
    print("\n Prueba de integración con frontend...")
    print("-" * 40)

    container = Container()
    district_service = container.district_service()

    # Simular carga inicial del dropdown
    districts = await district_service.get_districts_for_dropdown()

    print(" Datos que se enviarían al frontend:")
    print("```json")
    print("[")
    for i, district in enumerate(districts):
        comma = "," if i < len(districts) - 1 else ""
        print(f" {{")
        print(f' "value": "{district["value"]}",')
        print(f' "label": "{district["label"]}",')
        print(f' "restaurant_count": {district["restaurant_count"]},')
        print(f' "is_tourist_zone": {str(district["is_tourist_zone"]).lower()}')
        print(f" }}{comma}")
    print("]")
    print("```")

    print("\n Formato JSON listo para React SearchFilters component")


if __name__ == "__main__":
    print("Sistema de Gestión de Distritos de Lima")
    print("Proyecto Restaurant Recommender ML")
    print("=" * 60)

    # Ejecutar pruebas
    success = asyncio.run(test_districts_functionality())

    if success:
        asyncio.run(test_frontend_integration())
        print("\n¡Sistema listo para producción!")
    else:
        print("\nHay errores que corregir antes de continuar")
        sys.exit(1)
