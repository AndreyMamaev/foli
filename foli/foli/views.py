import folium
import pandas as pd
from django.shortcuts import render


def map(request):
    """Создает карту и сохраняет в html-страницу."""
    map = folium.Map(
        location = [56.3287, 44.002],
        zoom_start = 13,
    )
    folium.TileLayer('Stamen Terrain').add_to(map)
    data = import_markers('data/markers.csv')
    create_markers(data, map)
    folium.LayerControl().add_to(map)
    map.save('templates/foli/index.html')
    return render(request, 'foli/index.html')

def import_markers(path):
    """Импортирует данные о точках на карте из файла."""
    data = pd.read_csv(
        path, delimiter=';',
        names=['latitude', 'longitude', 'tooltip', 'popup','group']
    )
    return data

def create_markers(data, map):
    """Создает точки и добавляет их на карту."""
    for group_name, group_markers in data.groupby('group'):
        feature_group = folium.FeatureGroup(group_name)
        for row in group_markers.itertuples():
            folium.Marker(
                location=[row.latitude, row.longitude],
                tooltip=row.tooltip,
                popup=row.popup
                ).add_to(feature_group)
        feature_group.add_to(map)
