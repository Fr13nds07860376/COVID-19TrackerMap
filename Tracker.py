import folium
import requests

# Obtener datos reales de COVID-19 de la API de la Universidad Johns Hopkins
url = "https://corona.lmao.ninja/v3/covid-19/countries"
response = requests.get(url)
data = response.json()

# Crear un mapa centrado en una ubicación inicial
mapa = folium.Map(location=[20, 0], zoom_start=2)

# Crear una leyenda para mostrar datos de COVID-19
legend_html = """
<div style="position: fixed; 
     top: 50px; right: 50px; width: 250px; height: 250px; 
     background-color: rgba(255, 255, 255, 0.8);
     border-radius: 5px;
     z-index:9999;
     font-size:14px;">
     &nbsp; COVID-19 Datos<br>
     &nbsp; Casos: <i class="fa fa-circle" style="color:red"></i><br>
     &nbsp; Muertes: <i class="fa fa-circle" style="color:darkred"></i>
</div>
"""
mapa.get_root().html.add_child(folium.Element(legend_html))

# Agregar marcadores al mapa para mostrar la propagación del coronavirus por país
for pais_info in data:
    pais = pais_info['country']
    casos = pais_info['cases']
    muertes = pais_info['deaths']
    lat = pais_info['countryInfo']['lat']
    lon = pais_info['countryInfo']['long']

    # Ajustar el tamaño de las esferas en el radar del país
    radius = min(casos / 100000, 10)  # Limita el tamaño máximo de las esferas

    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=f'País: {pais}<br>Casos: {casos}<br>Muertes: {muertes}'
    ).add_to(mapa)

# Guardar el mapa interactivo en un archivo HTML
mapa.save('mapa_coronavirus.html')

# Abre el mapa interactivo en tu navegador web
import webbrowser
webbrowser.open('mapa_coronavirus.html')
