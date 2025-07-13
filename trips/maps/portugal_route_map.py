#!/usr/bin/env python3
"""
Generador de mapa para el itinerario de Portugal 2025
Crea un mapa visual mostrando la ruta completa con todos los puntos de parada
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Coordenadas de todas las paradas del itinerario
route_points = [
    # Día, Ubicación, Lat, Lon, Tipo de actividad
    (0, "Sevilla (Inicio)", 37.3891, -5.9845, "inicio"),
    (1, "Mérida", 38.9358, -6.3050, "camping"),
    (2, "Zamora (Descanso)", 41.5035, -5.7438, "descanso"),
    (2, "Peneda-Gerês", 41.7653, -8.1547, "montaña"),
    (3, "Peneda-Gerês", 41.7653, -8.1547, "montaña"),
    (4, "Viana do Castelo", 41.6789, -8.8156, "playa"),
    (5, "Labruja", 41.7536, -8.5833, "pueblo"),
    (6, "Labruja", 41.7536, -8.5833, "trekking"),
    (7, "Coimbra", 40.188974, -8.399933, "ciudad"),
    (8, "Coimbra", 40.188974, -8.399933, "ciudad"),
    (9, "Nazaré", 39.5972, -9.0764, "playa"),
    (10, "Nazaré", 39.5972, -9.0764, "playa"),
    (11, "Óbidos", 39.3600, -9.1567, "pueblo"),
    (12, "Peniche", 39.3500, -9.3833, "playa"),
    (13, "Ericeira", 38.9500, -9.4167, "playa"),
    (14, "Setúbal", 38.5240, -8.8930, "ferry"),
    (14, "Tróia", 38.4933, -8.8867, "playa"),
    (15, "Praia da Galé (Algarve)", 37.0500, -8.3000, "playa"),
    (15, "Sagres", 37.0294, -8.9378, "playa"),
    (16, "Sagres", 37.0294, -8.9378, "playa"),
    (17, "Sevilla (Final)", 37.3891, -5.9845, "final"),
]

# Colores y símbolos por tipo de actividad
activity_colors = {
    "inicio": "#FF0000",      # Rojo para inicio
    "final": "#FF0000",       # Rojo para final
    "camping": "#8B4513",     # Marrón para camping
    "montaña": "#228B22",     # Verde para montaña/naturaleza
    "playa": "#1E90FF",       # Azul para playas
    "ciudad": "#800080",      # Púrpura para ciudades
    "pueblo": "#FF8C00",      # Naranja para pueblos
    "trekking": "#006400",    # Verde oscuro para trekking
    "ferry": "#00CED1",       # Turquesa para ferry
    "descanso": "#FFD700",    # Dorado para descansos
}

activity_markers = {
    "inicio": "★",
    "final": "★", 
    "camping": "▲",
    "montaña": "♦",
    "playa": "●",
    "ciudad": "■",
    "pueblo": "▼",
    "trekking": "♠",
    "ferry": "⚓",
    "descanso": "◆",
}

def create_route_map():
    # Configurar la figura
    fig, ax = plt.subplots(figsize=(14, 16))
    
    # Definir los límites del mapa para centrar en la ruta
    lat_min, lat_max = 36.5, 42.5
    lon_min, lon_max = -10.0, -4.5
    
    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)
    
    # Configurar el mapa base
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#E6F3FF')  # Fondo azul claro para simular agua
    
    # Dibujar contornos aproximados de España y Portugal
    # Contorno simplificado de la Península Ibérica
    iberia_x = [-9.5, -9.0, -8.5, -8.8, -8.0, -7.0, -6.0, -5.0, -4.5, -5.0, -6.0, -7.0, -8.0, -9.0, -9.5]
    iberia_y = [42.0, 41.5, 40.0, 39.0, 38.0, 37.0, 36.5, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 42.2, 42.0]
    
    # Dibujar el contorno de la península
    polygon = patches.Polygon(list(zip(iberia_x, iberia_y)), 
                            closed=True, facecolor='#F5F5DC', 
                            edgecolor='#8B4513', linewidth=2, alpha=0.7)
    ax.add_patch(polygon)
    
    # Extraer coordenadas para la línea de ruta
    route_lats = [point[2] for point in route_points]
    route_lons = [point[3] for point in route_points]
    
    # Dibujar la línea de ruta principal
    ax.plot(route_lons, route_lats, 'b-', linewidth=3, alpha=0.7, 
            label='Ruta principal', zorder=2)
    
    # Dibujar línea de ferry especial (Setúbal - Tróia)
    setúbal_idx = next(i for i, point in enumerate(route_points) if "Setúbal" in point[1])
    tróia_idx = next(i for i, point in enumerate(route_points) if "Tróia" in point[1])
    
    ax.plot([route_points[setúbal_idx][3], route_points[tróia_idx][3]], 
            [route_points[setúbal_idx][2], route_points[tróia_idx][2]], 
            'c--', linewidth=3, alpha=0.8, label='Ferry Setúbal-Tróia', zorder=2)
    
    # Dibujar puntos de parada
    for i, (day, location, lat, lon, activity_type) in enumerate(route_points):
        color = activity_colors.get(activity_type, "#000000")
        marker = activity_markers.get(activity_type, "o")
        
        # Tamaño especial para inicio y final
        size = 200 if activity_type in ["inicio", "final"] else 120
        
        ax.scatter(lon, lat, c=color, s=size, marker='o', 
                  edgecolors='black', linewidth=1, zorder=5, alpha=0.9)
        
        # Añadir etiquetas de día
        if day > 0:
            ax.annotate(f'D{day}', (lon, lat), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, 
                       fontweight='bold', ha='left', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    # Añadir ciudades principales como referencia
    major_cities = [
        ("Madrid", 40.4168, -3.7038),
        ("Lisboa", 38.7223, -9.1393),
        ("Porto", 41.1579, -8.6291),
        ("Barcelona", 41.3851, 2.1734),  # Fuera del mapa pero como referencia
    ]
    
    for city, lat, lon in major_cities:
        if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
            ax.scatter(lon, lat, c='red', s=50, marker='s', alpha=0.6, zorder=3)
            ax.annotate(city, (lon, lat), xytext=(5, 5), 
                       textcoords='offset points', fontsize=9, 
                       style='italic', alpha=0.7)
    
    # Crear leyenda personalizada
    legend_elements = []
    unique_activities = {}
    for _, _, _, _, activity_type in route_points:
        if activity_type not in unique_activities:
            unique_activities[activity_type] = (activity_colors[activity_type], 
                                              activity_markers[activity_type])
    
    for activity, (color, marker) in unique_activities.items():
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                        markerfacecolor=color, markersize=10, 
                                        label=activity.capitalize()))
    
    # Añadir líneas a la leyenda
    legend_elements.append(plt.Line2D([0], [0], color='blue', linewidth=3, 
                                    label='Ruta por carretera'))
    legend_elements.append(plt.Line2D([0], [0], color='cyan', linewidth=3, 
                                    linestyle='--', label='Ferry'))
    
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98), 
             framealpha=0.9, fontsize=10)
    
    # Títulos y etiquetas
    ax.set_title('Itinerario Portugal 2025 - Ruta en Autocaravana\n17 días: Sevilla → Norte de Portugal → Algarve → Sevilla', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Longitud (°W)', fontsize=12)
    ax.set_ylabel('Latitud (°N)', fontsize=12)
    
    # Añadir información en la esquina inferior derecha
    info_text = (
        "Distancia total: ~2,200 km\n"
        "Duración: 17 días\n"
        "8 días de playa\n" 
        "2 días de montaña\n"
        "1 ferry requerido\n"
        "Apto para autocaravanas"
    )
    
    ax.text(0.98, 0.02, info_text, transform=ax.transAxes, 
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
           verticalalignment='bottom', horizontalalignment='right',
           fontsize=10)
    
    # Añadir rosa de los vientos
    compass_x, compass_y = 0.05, 0.15
    ax.annotate('N', xy=(compass_x, compass_y), xycoords='axes fraction',
               ha='center', va='center', fontsize=14, fontweight='bold')
    ax.annotate('↑', xy=(compass_x, compass_y-0.03), xycoords='axes fraction',
               ha='center', va='center', fontsize=16)
    
    plt.tight_layout()
    
    # Guardar el mapa
    output_file = '/Users/carlosrodlop/code/github/carlosrodlop/carlosrodlop/docs/trips/portugal_route_map.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"Mapa guardado como: {output_file}")
    plt.show()
    
    return fig, ax

if __name__ == "__main__":
    create_route_map()
