#Importamos el modulo request para realizar la solicitud http en una pagina web.
import requests
#Importamos el modulo bs4 la libreria BeautifulSoup para analizar el html.
from bs4 import BeautifulSoup
#Importamos el modulo datetime para que nos proporcione clases para poder manipular fechas y horas.
from datetime import datetime
def tranformar_fecha(fecha_caracteres):
    fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]),
                     int(fecha_caracteres[6:8]))
    return fecha

#La función 'webscraping' tiene dos parámetros: 'url_scraping' y 'categoria_scraping' con un valor predeterminado de 'todas'.
def webscraping(url_scraping,categoria_scraping='todas'):
    # URL de de telemadrid
    url = url_scraping
       try:
        respuesta = requests.get(url)
        #Envíamos una solicitud GET a la URL (telemadrid) almacenada en la variable 'respuesta'.
        #print(respuesta)
        #print(respuesta.text)
        #La variable respuesta tendrá la información devuelta por el servidor, como el contenido html de la página web.

        #Agregamos una verificación para asegurarnos de que la url en este caso (telemadrid )sea válida.
        # Por medio de solicitud(respuesta.status_code).
        #Verificamos si la petición fue exitosa (código 200), para saber si podemos acceder a la información.
        #Si no es exitosa la respuesta colocamos la debida excepción.

        if respuesta.status_code == 200:
            # Si la petición es correcta (código 200) empezamos a analizar la pagina web.
            try:
                #Se intenta abrir el archivo 'noticias.csv' ubicado en directorio '../data en modo de escritura ('w').
                with open('../data/noticias.csv', 'w') as f:
                    # Si el archivo no existe, se creará.Se utiliza 'with' para garantizar que el archivo se cierre correctamente
                    # después de su uso.
                    f.write('titulo,url,categoria,fecha'+'\n')
                    #En el archivo csv que se crea se escribe la primera línea del encabezado.
                    #La línea del encabezado contiene los nombres de las columnas: 'titulo', 'url', 'categoria', 'fecha'.
            #Se coloca la excepción si no se pudo crear el archivo de noticias.csv
            except:
                print("ERROR: no se pudo crear el archivo noticias.csv")
            try:
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                #Con la libreria BS pasamos el texto de la página web y le decimos qué codigo analizar traduciendo la data
                # por medio de la variable soap a html.parser (lenguaje html).Y aquí se encuentra el texto definido: donde
                #se encuentran las clases, donde comienzan los li, cuales son las etiquetas que usan los programadores de
                #páginas web para introducir cajas, videos, botones, enlaces, textos alternativos etc.
                #print(soup)
                #Aquí empezamos a realizar operaciones de Web Scraping:
                #sacando las noticias del codigo html
                #Se intenta localizar por medio de find_all todos los elememtos que coinciden con los criterios:
                #'article' con la clase: card-news.
                try:
                    noticias = soup.find_all('article', class_='card-news')
                    if noticias:
                        #print(noticias)
                        lista_categorias = []
                        #Hacemos una variable general: lista de categorias que se inicializa en una lista vacía.Para que el
                        #usuario pueda acceder a un menú con las categorías únicas (sin duplicar)

                        for articulo in noticias:
                            #Iniciamos un bucle 'for' que itera sobre cada elemento en la lista 'noticias'.
                            #print(articulo)
                            try:#Buscamos la clase: oop-link, para localizar el título de los artículos.
                                #si falla la busqueda y no me puede sacar los títulos, buscamos otra clase en la excepción:lnk.
                                titulo = articulo.find('a', class_='oop-link').text.strip()
                                #Buscamos el elemento 'a' con la clase 'oop-link' dentro de cada 'articulo' y extraemos el texto del elemento.
                                url_noticia = articulo.find('a', class_='opp-link')['href']
                                #print(url_noticias), imprime el título y la url de cada articulo.
                                lista_url_noticia = url_noticia.split('/')
                                # A cada url, la dividimos en partes utilizando una barra '/' como delimitador (metodo split).
                                #Luego se almacena las partes en una lista: 'lista url noticia'
                                if lista_url_noticia[1] != '':
                                    #se verifica si el segundo componente de la URL (que está en la posición 2 de 'lista_url_noticia')
                                    # no es una cadena vacia.
                                    categoria = lista_url_noticia[1]
                                    #A la variable categoría le asigno 1 si es != vacío (1, accede al 2 elemento de la 'lista_url_noticia')
                                else:
                                    categoria = lista_url_noticia[3]
                                    #si el segundo componente de la URL (índice 1 en lista_url_noticia) es una cadena vacía,
                                    # el código asignará el valor del cuarto componente de la URL (índice 3 en lista_url_noticia)
                                    # a la variable categoria. .
                                lista_categorias.append(categoria)
                                #Agregamos el valor de la variable 'categoria' actual al final de la lista 'lista_categorias'.Lo que permite mantener
                                #un registro de todas las categorías.
                                lista_fecha = url_noticia.split('--')
                                #Descomponemos la cadena y extraemos la información de la fecha que se encuentra en la posición predefinida.
                                fecha_caracteres = lista_fecha[1].replace('.html', '')
                                #Quitamos la extension 'html' del segundo elemento de 'lista_fecha' y dejamos solo los caracteres de la
                                #fecha en la variable 'fecha_caracteres'
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
                                #Limpiamos el texto del titulo eliminando ciertos caracteres especiales para mejorar la
                                #generacion de archivos csv.
                                if categoria_scraping == 'todas':
                                    #Comprobar si la categoría a extraer es 'todas'
                                    try:
                                        with open('../data/noticias.csv', 'a') as f:
                                            f.write(titulo+','+url_noticia+','+categoria+','+str(fecha)+'\n')
                                            # Abrir el archivo 'noticias.csv' en modo de anexar ('a')
                                        # Analizar el contenido con BeautifulSoup
                                    except:
                                        print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                else:
                                    if categoria == categoria_scraping:
                                        #Si la categoria a extraer no es 'todas', comprobar si la categoria actual coincide
                                        #con la categoria deseada.
                                        try:
                                            with open('../data/noticias_'+categoria_scraping+'.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                            except:
                                try:# buscamos con la otra clase: lnk
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
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                    else:
                                        if categoria == categoria_scraping:
                                            try:
                                                with open('../data/noticias_' + categoria_scraping + '.csv', 'a') as f:
                                                    f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                        fecha) + '\n')
                                                # Analizar el contenido con BeautifulSoup
                                            except:
                                                print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                except:
                                    pass
                                    # si falla la conexión con oop-link y lnk no se hace nada
                        #print(lista_categorias)
                        conjunto_categorias = set(lista_categorias)
                        #print(conjunto_categorias)
                    else:
                        print(f"Error La pagina {url} no contiene noticias")
                        # si hay un error entonces se imprime ésta notificación.
                except:
                        print(f"ERROR: No se pudo encontrar articulos en el codigo html")
            except:
                print(f"ERROR: no se pudo convertir la pagina a codigo html")
                #Imprime error si no se pudo convertir los datos a codigo html-
        else:
            print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")
            #Imprime error si el codigo no es 200.
            # except:
        print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")
        #Imprime un error cuando no podemos abrir la web o existe algún error
    return 'conjunto_categorias'



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
