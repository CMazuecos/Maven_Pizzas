import pandas as pd
import csv
import datetime
import numpy as np


def informe_calidad_datos (fichero, name):
    #Print name of the file, nans, nulls and data types
    print('Nombre del fichero:', name)
    print (fichero.isnull().sum()) 
    print (fichero.dtypes)
    print (fichero.isna().sum())
    #We write the file in a txt
    with open('Informe_Calidad_Datos.txt', 'a') as file:
        file.write('Nombre del fichero: ' + name + '\n')
        file.write(str(fichero.isnull().sum()) + '\n')
        file.write(str(fichero.dtypes) + '\n')
        file.write(str(fichero.isna().sum()) + '\n')
        

def cargar_datos (order_details, pizzas, pizza_types, orders):
    dictionary_pizza_type = {}
    for i in range(len(pizza_types)):
        #We create a dictionary with the ingredients of each pizza type
        dictionary_pizza_type [pizza_types ['pizza_type_id'][i]] = pizza_types ['ingredients'] [i]
    for key, value in dictionary_pizza_type.items():
        print(key, ':', value)
    semanas, dias_semana = organizar_por_semanas(orders) #We organize the orders by weeks
    pedidos = organizar_por_pedidos(semanas, order_details) 
    pizzas_semana = transform_pizza_id(pedidos, pizzas) #We transform the pizza id into the pizza type id
    ingredients = transform_pizza_into_ingredients(pizzas_semana, pizza_types, dias_semana) #We transform the pizza type id into the ingredients
    return ingredients


    
def organizar_por_semanas(orders):
    #We organize the orders by weeks and count the days of each week    
    numero_pedido = 1
    semanas, dias_semana = [], []
    number_week = 1
    number_weekdays = [0, 0, 0, 0, 0, 0, 0]
    for i in range (len(orders)):
        #We get the day of the week of the order and the number of the week
        fecha = orders['date'][i]
        fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
        numero_semana = fecha.isocalendar().week
        numero_dia = fecha.isocalendar().weekday
        #We count the days of each week
        if numero_semana != number_week:
            dias_venta = 0
            #We count the days of the week that have orders
            for j in range (len(number_weekdays)):
                if number_weekdays[j] > 0:
                    dias_venta += 1
            number_week = numero_semana
            number_weekdays = [0, 0, 0, 0, 0, 0, 0]
            semanas.append(numero_pedido)
            dias_semana.append(dias_venta)
        #We add one to the day of the week of the order
        else:
            number_weekdays[numero_dia-1] += 1
        numero_pedido += 1

    return semanas, dias_semana
    
def organizar_por_pedidos(semanas, order_details):
    pedidos = []
    order_details_number = 0
    for i in range (len(semanas)):
        #We create a list with the orders of each week
        pedidos_semana = []
        try:
            #We add the orders of each week to the list until we reach the next week
            while order_details['order_id'][order_details_number] <= semanas[i]:
                pedidos_semana.append([order_details['pizza_id'][order_details_number], order_details['quantity'][order_details_number]])
                order_details_number += 1
        except:
            pass
        #We add the list of orders of a week to the list of all the weeks
        pedidos.append(pedidos_semana)
    return pedidos

def transform_pizza_id(pedido, pizzas):
    
    pizzas_semana = []
    #We create a list with the pizzas of each week
    for i in range (len(pedido)):
        pedidos_mod = {}
        for j in range (len(pizzas)):
            pedidos_mod [pizzas['pizza_type_id'][j]] = 0
        pedidos_mod = pizza_tamano(pedido[i], pizzas, pedidos_mod)
        pizzas_semana.append(pedidos_mod)
        print('Se ha cargado la semana', i + 1)
    return pizzas_semana

def pizza_tamano(pedido, pizzas, pedidos_mod):  
    tamanos = {'S': 1, 'M': 2, 'L': 3, 'XL': 4, 'XXL': 5}
    #We transform the quantity of pizzas of each size into the quantity multiplied by the size
    for i in range(len(pedido)):
        for j in range(len(pizzas)):
            if pedido[i][0] == pizzas['pizza_id'][j]:
                pedidos_mod [pizzas ['pizza_type_id'][j]] += (pedido [i][1] * tamanos [pizzas['size'][j]])
    return pedidos_mod  

def transform_pizza_into_ingredients(pizzas_semana, pizza_types, dias_semana):    
    ingredients_per_week = []
    for k in range(len(pizzas_semana)):
        ingredients = {}
        # we create a dictionary with the all the different ingredients 
        for i in range (len(pizza_types)):
            for j in range (len(pizza_types['ingredients'][i].split(', '))):
                ingredients [pizza_types['ingredients'][i].split(', ')[j]] = 0
        ingredients = get_ingredients(pizzas_semana [k], pizza_types, ingredients)
        for key in ingredients.items():
            #We make the recommendation of the ingredients for a week of 7 days
            ingredients[key[0]] = int(np.ceil((key[1] / dias_semana[k]) * 7))        
        ingredients_per_week.append(ingredients)
    return ingredients_per_week
    
def get_ingredients(pizzas_semana, pizza_types, ingredients):
    #We add the ingredients of each pizza to the dictionary
    for key, value in pizzas_semana.items():
        for j in range (len(pizza_types)):
            if key == pizza_types['pizza_type_id'][j]:
                ingredients_pizza = pizza_types['ingredients'][j].split(', ')
                for k in range (len(ingredients_pizza)):
                    ingredients [ingredients_pizza [k]] += value
    return ingredients

def extract_data():
    #We extract the data from the csv files and make a report from them
    order_details = pd.read_csv('order_details.csv',sep=',')
    informe_calidad_datos(order_details, 'order_details.csv')
    pizzas = pd.read_csv('pizzas.csv',sep = ',')
    informe_calidad_datos(pizzas, 'pizzas.csv')
    pizza_types = pd.read_csv('pizza_types.csv', sep = ',', encoding='latin-1')
    informe_calidad_datos(pizza_types, 'pizza_types.csv')
    orders = pd.read_csv('orders.csv', sep = ',')
    informe_calidad_datos(orders, 'orders.csv')
    return order_details, pizzas, pizza_types, orders

def load_data(ingredients):
    #We print the recommendations for every week
    for i in range (len(ingredients)):
        print('Ingredientes recomendados para la semana', i + 1,':', ingredients[i])
        print('')
    
    #We write in a csv file the ingredients for each week
    with open('ingredients_per_week.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ingredientes'] + ['Semana ' + str(i + 1) for i in range (len(ingredients))])
        for key, value in ingredients[0].items():
            writer.writerow([key] + [ingredients [i][key] for i in range (len(ingredients))])
    print('Se ha creado el archivo ingredients_per_week.csv donde se hace la recomendacion de ingredientes por semana')
    print('Fin del programa')
        
    
if __name__ == '__main__':
    #We make an etl of the data to recommend the ingredients for each week
    order_details, pizzas, pizza_types, orders = extract_data()
    ingredients = cargar_datos(order_details, pizzas, pizza_types, orders)
    load_data(ingredients)
