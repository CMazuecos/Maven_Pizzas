# Maven_Pizzas
Este programa consistirá en que el programa hará un informe sobre los ficheros de la pizzería Maven y hará una recomendación de compra de ingredientes para cada semana.
### Archivos necesitados
- 'data_dictionary.csv': archivo csv que explican cada columna de los diferentes csvs.
- 'Maven_pizza_recommendation.py': programa python que hace el informa de datos y la recomendación.
- 'order_details.csv': archivo con los detalles de los pedidos.
- 'orders.csv': archivo que registra cuando se hace cada pedido.
- 'pizza_types.csv': archivo con los detalles de cada pizza.
- 'pizzas.csv': archivo que registra detalles sobre cada pizza id.
- 'requirements.txt': contiene todos las librerías necesarias para el correcto funcionamiento del programa.
### Outputs
- Fichero 'Informe_Calidad_Datos.txt': fichero txt con un informe con el número de Nulls, tipología de datos y número de Nans en cada columna de cada fichero.
- Fichero 'ingredients_per_week.csv': fichero csv con la compra de los ingredientes necesarios para cada semana.
### Forma de ejecución
- Descargamos los archivos csv, el requirements.txt y el archivo python en una misma carpeta.
- Ejecutar en la terminal 'pip install requirements.txt'.
- Ejecutar 'Maven_pizza_recommendation.py' y automáticamente se ejecutará el programa. 
- En primer lugar, se leen los datos de cada csv y se realizará el informe de datos. Se mostrará por pantalla y se escribirá en un fichero txt.
- Después, con los datos ya leídos se organizarán los pedidos por semanas.
- Cuando se organizan los pedidos por semanas, se ve que pizza contiene cada pedido.
- De cada pizza, se sacan los ingredientes de cada pizza y se van añadiendo a los pedidos de cada semana.
- Cuando ya se tiene la recomendación hecha, se escirbe en un archivo csv y se muestra por pantalla la compra recomendada para cada semana.  
Para más aclaraciones, código explicado en el texto.
