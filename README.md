# Evaluacion2 – Software de geolocalización con GraphHopper

Proyecto de la Evaluación Parcial N°2 de la asignatura CUY6142 (Telepresencia y Entornos Innovadores de Colaboración Humana).

El script `graphhopper_parse-json.py` consulta la API **GraphHopper Directions** para entregar a los visitantes de la Biblioteca Nacional la ruta entre un punto de origen y un destino. Respecto del prototipo original se incorporaron estas mejoras:

- Todos los textos de interacción con el usuario están en español.
- Distancias y demás valores numéricos se muestran con un máximo de dos decimales.
- El programa termina al ingresar `s` o `salir` en cualquier pregunta.
- La narrativa del viaje (instrucciones paso a paso) se entrega en español (`locale=es`).

## Requisitos

- Python 3
- Librería `requests` (`pip3 install requests`)
- Un token (API key) de GraphHopper: https://graphhopper.com/dashboard/#/apikeys

## Cómo ejecutar

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/<su-usuario>/Evaluacion2.git
   cd Evaluacion2
   ```
2. Definir el token como variable de entorno (así no queda escrito en el código):
   ```bash
   export GRAPHHOPPER_KEY="su_token_aqui"
   ```
   Si no se define, el script lo pedirá al iniciar.
3. Ejecutar:
   ```bash
   python3 graphhopper_parse-json.py
   ```
4. Ingresar el perfil de vehículo (`auto`, `bicicleta` o `a pie`), la ubicación de origen y el destino. Para terminar, escribir `s` o `salir`.

## Autores

- Nombre Apellido
- Nombre Apellido
