# -*- coding: utf-8 -*-
"""
Evaluación 2 - CUY6142
Software de geolocalización con la API GraphHopper Directions.
Mejoras: textos en español, valores con máximo 2 decimales,
salida con "s" o "salir" y narrativa del viaje en español.
"""
import os
import urllib.parse
import requests

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"

# El token se lee desde una variable de entorno para no publicarlo en GitHub.
key = os.environ.get("GRAPHHOPPER_KEY", "")
if key == "":
    key = input("Ingrese su token de GraphHopper: ").strip()

OPCIONES_SALIDA = ("s", "salir")
PERFILES = {"auto": "car", "bicicleta": "bike", "a pie": "foot",
            "car": "car", "bike": "bike", "foot": "foot"}
NOMBRE_PERFIL = {"car": "auto", "bike": "bicicleta", "foot": "a pie"}
KM_POR_MILLA = 1.609344


def quiere_salir(texto):
    return texto.strip().lower() in OPCIONES_SALIDA


def formatear_duracion(milisegundos):
    total_seg = int(milisegundos / 1000)
    horas = total_seg // 3600
    minutos = (total_seg % 3600) // 60
    segundos = total_seg % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def geocoding(location, key):
    while location.strip() == "":
        location = input("Ingrese nuevamente la ubicación: ")
    url = geocode_url + urllib.parse.urlencode(
        {"q": location, "limit": "1", "locale": "es", "key": key})

    respuesta = requests.get(url)
    json_status = respuesta.status_code
    json_data = respuesta.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        value = hit.get("osm_value", "")
        country = hit.get("country", "")
        state = hit.get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"URL de la API de Geocodificación para {new_loc} "
              f"(Tipo de ubicación: {value})\n{url}")
    else:
        lat = None
        lng = None
        new_loc = location
        if json_status != 200:
            print(f"Estado de la API de Geocodificación: {json_status}\n"
                  f"Mensaje de error: {json_data.get('message', '')}")
        else:
            print(f"No se encontraron resultados para: {location}")
    return json_status, lat, lng, new_loc


while True:
    print("\n" + "+" * 50)
    print("Perfiles de vehículo disponibles en GraphHopper:")
    print("+" * 50)
    print("auto, bicicleta, a pie")
    print("+" * 50)
    print("(Escriba 's' o 'salir' en cualquier momento para terminar)")

    vehiculo = input("Ingrese un perfil de vehículo de la lista: ")
    if quiere_salir(vehiculo):
        break
    vehiculo = vehiculo.strip().lower()
    if vehiculo in PERFILES:
        perfil = PERFILES[vehiculo]
    else:
        perfil = "car"
        print("No ingresó un perfil válido. Se usará el perfil auto.")

    loc1 = input("Ubicación de origen: ")
    if quiere_salir(loc1):
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destino: ")
    if quiere_salir(loc2):
        break
    dest = geocoding(loc2, key)

    print("=" * 50)
    if orig[0] == 200 and dest[0] == 200 and orig[1] is not None and dest[1] is not None:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = (route_url
                     + urllib.parse.urlencode({"key": key, "profile": perfil, "locale": "es"})
                     + op + dp)
        respuesta = requests.get(paths_url)
        paths_status = respuesta.status_code
        paths_data = respuesta.json()

        print(f"Estado de la API de Rutas: {paths_status}\nURL de la API de Rutas:\n{paths_url}")
        print("=" * 50)
        print(f"Indicaciones desde {orig[3]} hasta {dest[3]} en {NOMBRE_PERFIL[perfil]}")
        print("=" * 50)

        if paths_status == 200:
            ruta = paths_data["paths"][0]
            km = ruta["distance"] / 1000
            millas = km / KM_POR_MILLA
            print(f"Distancia recorrida: {km:.2f} km / {millas:.2f} millas")
            print(f"Duración del viaje: {formatear_duracion(ruta['time'])}")
            print("=" * 50)
            print("Narrativa del viaje:")
            for numero, paso in enumerate(ruta["instructions"], start=1):
                d_km = paso["distance"] / 1000
                print(f"{numero}. {paso['text']} "
                      f"({d_km:.2f} km / {d_km / KM_POR_MILLA:.2f} millas)")
            print("=" * 50)
        else:
            print("Mensaje de error: " + paths_data.get("message", ""))
            print("*" * 50)
    else:
        print("No fue posible calcular la ruta. Verifique las ubicaciones ingresadas.")

print("Programa finalizado. ¡Hasta pronto!")
