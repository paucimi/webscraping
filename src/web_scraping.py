#Importamos el modulo request para realizar la solicitud http en una pagina web.
import requests
#Importamos el modulo bs4 la libreria BeautifulSoup para analizar el html.
from bs4 import BeautifulSoup
#Importamos el modulo datetime para que nos proporcione clases para poder manipular fechas y horas.
from datetime import datetime
def tranformar_fecha(fecha_caracteres):
    fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]),
                     int(fecha_caracteres[6:8]))
    #La funcion toma una cadena de caracteres que representa una fecha en formato AAAAMMDD y la convierte en un objeto datetime.
    #La función utiliza el módulo datetime, que proporciona clases para trabajar con fechas y horas.
    return fecha
#La función 'webscraping' tiene dos parámetros: 'url_scraping' y 'categoria_scraping' con un valor predeterminado de 'todas'.
def webscraping(url_scraping,categoria_scraping='todas'):
    #URL de de telemadrid
    url = url_scraping
    #se asigna el valor de url_scraping a la variable url
    try:
        respuesta = requests.get(url)
        #Realizamos una solicitud GET a la URL (telemadrid) y la almacena en la variable respuesta.
        #print(respuesta)
        #print(respuesta.text)
        #La variable respuesta tendrá la información devuelta por el servidor, como el contenido html de la página web.

        #Agregamos una verificación para asegurarnos de que la url en este caso (telemadrid )sea válida.
        #Por medio de solicitud(respuesta.status_code) verificamos si la petición fue exitosa (código 200), para saber
        #si podemos acceder a la información.
        #Si no es exitosa la respuesta colocamos la debida excepción.

        if respuesta.status_code == 200:
            # Si la petición es correcta (código 200) empezamos a analizar la pagina web.
            try:

                with open('../data/noticias.csv', 'w') as f:
                    #Abrir el archivo 'noticias.csv' ubicado en directorio '../data en modo de escritura ('w') y lo asigna a
                    # la variable 'f'.
                    f.write('titulo,url,categoria,fecha'+'\n')
                    #En el archivo csv que se crea se escribe la primera línea del encabezado con las columnas:
                    # 'titulo', 'url', 'categoria', 'fecha'.
            #Si ocurre una excepcion, salta a la siguiente linea.
            except:
                print("ERROR: no se pudo crear el archivo noticias.csv")
            try:
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                #Utilizamos la biblioteca Beautifulsoup para extraer el contenido html de la respuesta http.
                #Por medio del html.parser podemos leer los distintos componentes de la pagina, en lugar de tratarla
                #como una cadena larga.

                #Aquí empezamos a realizar operaciones de Web Scraping:

                try:
                    noticias = soup.find_all('article', class_='card-news')
                    #Utilizamos la biblioteca soup para encontrar por medio de find_all todos los elememtos de la etiqueta
                    #'article' con el atributo de la clase: card-news.
                    if noticias:
                        #print(noticias)
                        lista_categorias = []
                        #Hacemos una variable general: con una lista vacía para que se puedan agregar elementos.
                        #Y el usuario pueda acceder a un menú con las categorías únicas (sin duplicar).

                        for articulo in noticias:
                            #Iniciamos un bucle 'for' que itera sobre cada elemento en la lista 'noticias'.
                            #print(articulo)
                            try:#Buscamos la clase: oop-link,dentro del elemento articulo actual.
                                #Si falla la busqueda y no me puede sacar los títulos, buscamos otra clase: lnk.
                                titulo = articulo.find('a', class_='oop-link').text.strip()
                                #Buscamos el primer elemento 'a' con la clase 'oop-link' dentro de cada 'articulo' y extraemos
                                #el texto del elemento.
                                #El método strip se utiliza para eliminar cualquier espacio en blanco al principio o al final del texto.
                                url_noticia = articulo.find('a', class_='opp-link')['href']
                                #print(url_noticias), imprime el título y la url de cada articulo.
                                lista_url_noticia = url_noticia.split('/')
                                # A cada url, la dividimos en partes utilizando una barra '/' como delimitador (metodo split).
                                #Luego se almacena las partes en una lista: 'lista url noticia'
                                if lista_url_noticia[1] != '':
                                    #se verifica si el segundo componente de la URL (que está en la posición 2 de 'lista_url_noticia')
                                    #no está vacio.
                                    categoria = lista_url_noticia[1]
                                    #A la variable categoría le asigno 1 si es != vacío (1, accede al 2 elemento de la 'lista_url_noticia')
                                else:
                                    categoria = lista_url_noticia[3]
                                    #si el segundo componente de la URL (índice 1 en lista_url_noticia) está vacio el código
                                    #asignará el valor del cuarto componente de la URL (índice 3 en lista_url_noticia)
                                    #a la variable categoria. .
                                lista_categorias.append(categoria)
                                #Agregamos el valor de la variable 'categoria' al final de la 'lista_categorias'.Lo que permite mantener
                                #un registro de todas las categorías de las noticias encontradas en el html analizado.
                                lista_fecha = url_noticia.split('--')
                                #Dividimos la URL de la noticia en partes utilizando -- y lo asigna a la variable lista_fecha.
                                #Y esta variable la utilizamos para obtener la fecha de la noticia.
                                fecha_caracteres = lista_fecha[1].replace('.html', '')
                                #Quitamos la extension 'html' del segundo elemento de 'lista_fecha' y reemplazamos con una cadena vacía.
                                #El resultado es una cadena de caracteres que representa la fecha en formato AAAAMMDD.
                                #La variable fecha_caracteres se utiliza para crear un objeto datetime que representa la fecha de la noticia.
                                # print(fecha_caracteres)
                                # print(fecha_caracteres[0:4])
                                # print(fecha_caracteres[4:6])
                                # print(fecha_caracteres[6:8])
                                # print(fecha_caracteres[8:10])
                                # print(fecha_caracteres[10:12])
                                # print(fecha_caracteres[12:14])
                                fecha = tranformar_fecha(fecha_caracteres)
                                #A partir de los componentes individuales del año, mes y dia que se extraen de
                                #'fecha_caracteres', modificamos los números a enteros para poder presentar una fecha
                                #estructurada.
                                fecha = fecha.strftime("%Y/%m/%d")
                                #Formateamos el objeto 'fecha' con el metodo ('string format time:  "AAAA/MM/DD")
                                titulo = titulo.replace('\'','').replace('"','').replace(',','')
                                #Con el metodo replace limpiamos el texto del titulo eliminando ciertos caracteres especiales
                                #como comillas,simples, dobles y comas.
                                #La variable titulo se utiliza para escribir una línea en un archivo CSV.
                                if categoria_scraping == 'todas':
                                    #Comprobar si la categoría a extraer es 'todas'
                                    try:
                                        with open('../data/noticias.csv', 'a') as f:
                                            f.write(titulo+','+url_noticia+','+categoria+','+str(fecha)+'\n')
                                            #Abrir el archivo 'noticias.csv' en modo de anexar ('a') y escribir una linea
                                            #en el archivo con los valores de titulo, url_noticia, categoria y fecha.
                                            #De esta forma en el archivo noticias.csv se almacena las noticias extraídas
                                            # de la pagina web de Telemadrid.

                                    except:
                                        print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                else:
                                    if categoria == categoria_scraping:
                                        #Si la categoria a extraer no es 'todas', comprobar si la categoria actual coincide
                                        #con la categoria deseada.Filtramos las noticias por categorias.
                                        try:
                                            with open('../data/noticias_'+categoria_scraping+'.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            #Se repite la misma informacion que antes
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                            except:
                                try:# buscamos con la otra clase: lnk y se repite todo el proceso anterior de la clase 'oop-link'.
                                    titulo = articulo.find('a', class_='lnk').text.strip()
                                    url_noticia = articulo.find('a', class_='lnk')['href']
                                    lista_url_noticia = url_noticia.split('/')
                                    if lista_url_noticia[1] != '':
                                        categoria = lista_url_noticia[1]
                                    else:
                                        categoria = lista_url_noticia[3]
                                    lista_categorias.append(categoria)
                                    lista_fecha = url_noticia.split('--')
                                    fecha_caracteres = lista_fecha[1].replace('.html', '')
                                    #print(fecha_caracteres)
                                    #print(fecha_caracteres[0:4])
                                    #print(fecha_caracteres[4:6])
                                    #print(fecha_caracteres[6:8])
                                    #print(fecha_caracteres[8:10])
                                    #print(fecha_caracteres[10:12])
                                    #print(fecha_caracteres[12:14])
                                    fecha = tranformar_fecha(fecha_caracteres)
                                    fecha = fecha.strftime("%Y/%m/%d")
                                    titulo = titulo.replace('\'', '').replace('"', '').replace(',', '')
                                    if categoria_scraping == 'todas':
                                        try:
                                            with open('../data/noticias.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')

                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                    else:
                                        if categoria == categoria_scraping:
                                            try:
                                                with open('../data/noticias_' + categoria_scraping + '.csv', 'a') as f:
                                                    f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                        fecha) + '\n')

                                            except:
                                                print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                except:
                                    pass
                                    #si falla la conexión con oop-link y lnk no se hace nada
                        #print(lista_categorias)
                        conjunto_categorias = set(lista_categorias)
                        #print(conjunto_categorias)
                    else:
                        print(f"Error La pagina {url} no contiene noticias")

                except:
                        print(f"ERROR: No se pudo encontrar articulos en el codigo html")
            except:
                print(f"ERROR: no se pudo convertir la pagina a codigo html")

        else:
            print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")

    except:
        print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")

    return 'conjunto_categorias'

#Este codigo utiliza la funcion webscraping para extraer noticias de la pagina de telemadrid y le permite al usuario
#seleccionar una categoria para extraer noticas.
listado_categorias = webscraping('https://www.telemadrid.es/','todas')
seleccion = 'x'
while seleccion != '0':
    print("Lista de categorias: ")
    i = 1
    for opcion in listado_categorias:
        print(f"{i}.- {opcion}")
        i = i + 1
    print("0.- Salir")
    seleccion = input("Por favor seleccione una opcion indicando un numero:")
    categorias_listas = list(listado_categorias)
    categoria_seleccionada = categorias_listas[int(seleccion)-1]
    webscraping('https://www.telemadrid.es/', categoria_seleccionada)

#Resumen del codigo anterior:
#La variable listado_categorias se inicializa llamando a la función webscraping con la URL 'https://www.telemadrid.es/'
#y la categoría 'todas'. A continuacion, el codigo entra en un bucle while que se ejecutara mientras el valor de seleccion
#no sea igual a '0'. Dentro del bucle, el codigo muestra una lista de categorias y solicita al usuario que seleccione una
#categoría ingresando un numero. La variable seleccion se utiliza para almacenar la seleccion del usuario. A continuacion,
#el codigo utiliza la variable seleccion para obtener la categoría seleccionada por el usuario y llama a la función
#webscraping con la URL.