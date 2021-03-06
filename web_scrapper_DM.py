# -*- coding: utf-8 -*-
"""
Autores:
    Alejandro Prieto Velasco. alex47@uoc.edu
    Oscar Ramírez González. oramirezgo@uoc.edu
    
No nos hacemos responsables del uso de este código ni de sus posibles consecuencias.

Esto es un ejercicio académico

Programa para hacer web scrapping con BeautifulSoup en la web de https://datosmacro.expansion.com/

Haremos web scrapping de las 22 web que hay bajo la URL https://datosmacro.expansion.com/demografia

No todos los indices que hay en cada página web muestran el mismo número de paises.html

210325_HHMM_main.py Oscar Ramirez y Alejandro Prieto: primer draft
210329_HHMM_main.py Alejandro Prieto: extraer información de cada indice
210331_2340_main.py Oscar Ramirez: ordeno las dos funciones para que estén al principio del fichero y añado el menu para
       seleccionar las web de las que se quiere hacer scrapping. Faltaba return(nombre_df) en la función de extracción
       de parametros. Crea un fichero csv por dataframe con codificación ISO-8859-1 para que salgan la ñ y los
       acentos. Quitar [+] detras de cada país, y añadir esta cabecera para llevar un control de versiones, un poco
       chapuza, pero bueno.......
210401_1625_main.py Alejandro Prieto: He cambiado el encoding de la última línea ( dataframe_temp.to_csv()) a
        "utf_8_sig" por que estaba dando un error en el enlace de mortalidad
210412_1747 Alejandro Prieto: Salida no direccionada a ninguna carpeta. Corrección de algunas faltas de ortografía.
210412_2052 Alejandro Prieto: Añadimos descargo de responsabilidad
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup



####################################
# COMIENZO DEFINICION DE FUNCIONES #
####################################

def seleccion_usuario():

    # Programa que devuelve la lista de opciones seleccionadas por el usuario, haciendo comprobación de valores no
    # existentes, campos vacios y, en caso de haber valores repetidos, dejando solo uno. Por ejemplo, si introducimos
    # 4,5,4,3,2, dejará 4,5,3,2.


    correcto = True
    while correcto == True:
        print("Bienvenido al programa de extracción de datos de la web https://datosmacro.expansion.com/demografia")
        print("Seleccione las web de las que quiere extraer los datos de la lista de debajo:")
        print("1.- Índice Global de la Brecha de Género")
        print("2.- Población")
        print("3.- Inmigrantes")
        print("4.- Remesas de migrantes")
        print("5.- Emigrantes totales")
        print("6.- Índice de Desarrollo Humano")
        print("7.- Índice de Progreso Social - SPI")
        print("8.- Índice de Paz Global")
        print("9.- Índice global de envejecimiento")
        print("10.- Natalidad")
        print("11.- Mortalidad")
        print("12.- Esperanza de vida al nacer")
        print("13.- Matrimonios")
        print("14.- Divorcios")
        print("15.- Suicidios")
        print("16.- Homicidios Intencionados")
        print("17.- Población reclusa")
        print("18.- Riesgo de pobreza")
        print("19.- Índice Mundial de la Felicidad")
        print("20.- Pirámide de población")
        print("21.- Tasa de alfabetización de adultos")
        print("22.- Religiones")

        print("\n\nPara terminar el programa pulsar ENTER.")
        val = input("\n\nIntroduzca selección indicando los número correspondientes, separados por comas y sin espacios en blanco "
                    "entre caracteres: ")

        lista_entrada = val.split(',')
        contador = 0
        for i in lista_entrada:
            if lista_entrada[contador] == "":
                exit("Programa Terminado")
            elif lista_entrada[contador] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'
                , '15', '16', '17', '18', '19', '20', '21', '22']:
                input("No has introducido valores correctos. Por favor, pulsa ENTER y prueba otra vez.")
                break
            else:
                if contador == len(lista_entrada)-1:
                    correcto = False
            contador = contador + 1
    lista_entrada_nueva = list(dict.fromkeys(lista_entrada))
    lista_ordenada = [int(p) for p in lista_entrada_nueva]
    lista_ordenada.sort()
    lista = lista_ordenada
    # print("Devuelve esta lista de opciones seleccionadas:", lista)
    return lista

# Funcion para extraer datos de cada web
def extraer(url):
    global nombre_df

    # Definimos la URL y los headers,.
    
    headers = {"User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                             "/47.0.2526.80 Safari/53asdfasdf7.36"}

    # Realizamos la petición a la página y creamos la sopa en formato lxml
    pagina = requests.get(url, headers=headers)
    statusCode = pagina.status_code

    if statusCode == 200:
        # print(statusCode)
        # print(url)

        sopa_demografia = BeautifulSoup(pagina.content, 'html.parser')

        # Sacamos los encabezados de la tabla
        tabla_encabezado = sopa_demografia.find_all('th')
        # Sacamos la información
        encabezado = [item.text for item in tabla_encabezado]

        # Elminamos un grafico de Barras que trae cada tabla y que no nos sirve de nada
        for td in sopa_demografia.find_all("td", {"class": "hbar"}):
            td.decompose()

        # Sacamos la información
        tabla = sopa_demografia.findAll('td')
        # Crea una lista de elementos a analizar
        info = [item.text for item in tabla]

        # Generamos nombre del dataframe
        # nombre_df ='df_' + url.rsplit('/', 1)[-1]

        # Creamos un dataframe
        nombre_df = pd.DataFrame()

        # Creamos el dataframe, el nombre de las columnas es el encabezado
        # que hemos descargado antes y le vamos indexando su correspondiente información
        # por columna
        for i in encabezado:
            nombre_df[i] = info[encabezado.index(i)::len(encabezado)]

        # Imprimimos el df para poder visualizarlo
        # print(nombre_df)
        return(nombre_df)

    else:
        texto = ("Esta web: " + url + " no existe")
        exit(texto)

###############################
# FIN DEFINICION DE FUNCIONES #
###############################


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)


# Definimos la URL y los headers, aunque los headers no se muy bien como funcionan.
url = 'https://datosmacro.expansion.com/demografia/'
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

# Realizamos la petición a la página y creamos la sopa en formato lxml
pagina = requests.get(url, headers=headers)
statusCode = pagina.status_code
if statusCode == 200:
    # print(statusCode)
    sopa_demografia = BeautifulSoup(pagina.content, 'html.parser')
else:
    texto=("Esta web: " + url + " no existe")
    exit(texto)

# Vemos el aspecto que tiene
# print(sopa_demografia.prettify())
'''
for link in sopa_demografia.find_all('a'):
    print(link.get('html'))
 '''

 
tabla = sopa_demografia.findAll(['h2', 'a'])

#print(tabla.attrs['href'])
#info_tabla = [item for item in tabla]
#info_tabla = info_tabla.attrs['href']
#print(info_tabla)


lista = []

for link in sopa_demografia.findAll('a'):
    if 'href' in link.attrs:
        lista.append(link.attrs['href'])

# Borro los primeros 62 elementos de la lista
lista = lista[62:]


# Cojo solo los que tienen la parte de la URL que nos interesa, sin nombre de país.
lista = lista[0::11]

# Borro los últimos 23 elementos de la lista
lista = lista[:-23]


# Dejamos solo el nombre final de la URL, por ejemplo "indice-brecha-genero-global"
parametro = []
for string in lista:
    lista_temp = string.replace("/demografia", "")
    parametro.append(lista_temp)
# print(parametro)

parametro_2 = []
for string in parametro:
    lista_temp = string.replace("/migracion", "")
    parametro_2.append(lista_temp)
# print(parametro_2)

parametro_3 = []
for string in parametro_2:
    lista_temp = string.replace("/mortalidad/causas-muerte", "")
    parametro_3.append(lista_temp)

# print(parametro_3)



# parametro es una lista con todos los nombres que hay depues del último / en cada URL
# Por ejemplo la última parte de https://datosmacro.expansion.com/demografia/indice-brecha-genero-global
# Lo podemos usar para crear varias carpetas en nuestro CSV y menter en cada una la info de cada web.
parametro = parametro_3
# print(parametro)

# Añado el path completo a cada URL
lista_nueva = []
for string in lista:
    lista_temp = string.replace("/demografia", "https://datosmacro.expansion.com/demografia")
    lista_nueva.append(lista_temp)

# Este es raro y lo asigno con esta igualdad
lista_nueva[5] = "https://datosmacro.expansion.com/idh"

# Lista contiene la lista de las 22 URLs
lista = lista_nueva

# Obtengo mi lista de 22 URL´s
# print(lista)

seleccion = seleccion_usuario()
# print(seleccion)
lista_temp = []
parametro_temp = []

for i in seleccion:
    indice = lista[i-1]

    lista_temp.append(indice)

    nombre_corto = parametro[i - 1]

    parametro_temp.append(nombre_corto)

lista = lista_temp
parametro = parametro_temp
# print(lista)
# print(parametro)

# df_datsomacro = DataFrame()

# extraer(https://datosmacro.expansion.com/demografia/spi)
j = 0
for i in lista:
    dataframe_temp = (extraer(i))
    dataframe_temp['Países'] = dataframe_temp['Países'].str.replace(' [+]', '', regex=False)
    # (dataframe_temp)
    nombre_fichero = (parametro[j])
    nombre_fichero = nombre_fichero.replace("/", "")
    nombre_fichero = ( str(seleccion[j]) + "_" + nombre_fichero + ".csv")
    # print(nombre_fichero)
    j = j + 1
    dataframe_temp.to_csv(nombre_fichero, encoding="utf_8_sig", index=False)



