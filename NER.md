---
title: |
    Extracción de identificadores personales de textos históricos en español
authors:
- Rafael Rodriguez-Charris
- Andrew Janco
date: 2018-04-09
reviewers:
layout: lesson
difficulty: advanced
topics: ''
abstract: ''  
---

Introducción
============

El procesamiento de lenguaje natural (*Natural Language Processing* por sus siglas en inglés) es un campo en las ciencias de la computación que busca entrenar a una computadora para que interactúe de la mejor manera con el lenguaje humano. De por sí, este campo tiene muchísima variedad y ofrece varias aplicaciones. Entre ellas:

- Síntesis del discurso
- Análisis del lenguaje
- Comprensión del lenguaje
- Reconocimiento del habla
- Síntesis de voz
- Traducción automática
- Extracción de información

En este tutorial, usted aprenderá a extraer información a partir de un corpus textual. La aplicación de extraer información es un concepto bastante amplio de por sí. Por lo tanto, esta lección se enfocará en extraer entidades nombradas (nombres propios en español) a partir de un corpus textual.  Usted podrá, sin importar cuán extenso sea su corpus, extraer con un alto porcentaje de precisión el nombre completo de personas que aparezcan referenciadas en su archivo textual.



## Requerimientos ##

**Python 3.0 o cualquier versión más reciente** 

**Editor de texto** - hay muchísimos editores de texto disponibles de forma gratuita. Puede usar NotePad, TextEdit, Sublime, entre muchos otros. Para este tutorial, usamos Sublime.

**Nombres.txt** - en este archivo de texto plano se encuentran 64,295 nombres y apellidos de personas en español y algunos otros idiomas. El trabajo de recopilación de estos datos es algo que se ha hecho previamente para el usuario, por lo tanto, usted solamente tiene que tenerlo disponible en su modelo para que sea usado en el tutorial. Refiérase a la sección de [Retos][#Retos] que se encuentra más adelante para que observe cómo se utiliza este archivo de texto plano y cuáles son algunos de los retos de usarlo.

Para aprender un poco la forma en cómo se generó esta extensa lista de nombres, visite la sección más adelante sobre [Fuentes libres usadas para construir la lista de nombres][#fuentes-libres-usadas-para-construir-la-lista-de-nombres]. 

**Archivo de muestra** - durante la creación de este taller, usamos como ejemplos los discursos políticos de presidentes colombianos (Álvaro Uribe Vélez y Juan Manuel Santos) para trabajar con el modelo de extracción. Si usted desea usarlos como referencia para observar como funciona el modelo, estos estarán disponibles en el repositorio digital. De otra manera, use su propio archivo de texto plano para realizar este tutorial.

**Google Colaboratory** (opcional) - una libreta (cuaderno) para programar con *Python* totalmente gratuita y creada por Google. La libreta (cuaderno) contiene todas las bibliotecas que usaremos para este tutorial y cada cambio se guarda automáticamente en su Google Drive. Por lo tanto, sería bueno que creara una cuenta de Gmail (si no la tiene ya) para así poder acceder a la libreta desde Google Drive. 

La opción para trabajar con esta libreta se presentará al final del tutorial, ya que es la más facil de las dos opciones que serán presentadas, pero no es la más sostenible ya que es dependiente de que Google mantenga este proyecto de *Google Colaboratory* disponible al público.



## Conocimiento previo ##

Este tutorial fue escrito en su totalidad usando el lenguaje de programación llamado *Python*. Aunque sería útil que supiese la forma en que trabaja este lenguaje de programación, este tutorial se ha escrito con el menor nivel de complejidad posible para el usuario. 

*Python* contiene varias bibliotecas que usaremos en este tutorial y de las cuales no se requiere tenga mayor pericia para utilizarlas:

- **Re** - esta biblioteca es una abreviatura para expresiones regulares (*regular expressions* en inglés). En este tutorial, no le explicaremos a fondo el uso de esta biblioteca que es más extenso y útil para muchísimos otros proyectos o investigaciones relacionados al análisis de texto. Si desea aprender más sobre su uso y utilidad, visite la sección [Fuentes libres usadas para construir la lista de nombres][#fuentes-libres-usadas-para-construir-la-lista-de-nombres] en donde brevemente se habla de su uso para obtener la lista de nombres con la que trabajaremos durante esta lección.

- **NLTK** - esta biblioteca es la más importante de todas las que usaremos en este tutorial. Kit de Herramientas del Lenguaje Natural (*Natural Language Tool Kit* en inglés) es una vasta biblioteca que permite limpiar y modificar el corpus textual antes de analizarlo para extracción. En la próxima sección entenderá más a fondo el porqué de su uso.

- **String** - esta biblioteca la usará brevemente en el tutorial, ya que ella contiene todos los signos de puntuación que se usan en el inglés. Lea en la sección de *Retos* de este tutorial un poco más sobre los obstáculos de esta biblioteca de *Python*.

- **Pandas** - esta biblioteca la usaremos con el propósito de poder visualizar la información procesada a medida que se analiza el contenido del corpus de texto.

  ​



## Retos

Durante la creación de este tutorial, enfrentamos varios retos que nos gustaría compartir con usted antes de que aplique alguna de las ideas de esta lección.

- **1) Longitud del nombre completo:** Analizar y extraer nombres completos en español es mucho más complicado que las estructuras de nombres en idiomas como el inglés, por ejemplo, porque una persona puede tener varios nombres en español (primer nombre, segundo nombre, entre otros) y, a la vez, se vuelve compleja la estructura de los apellidos (paterno y materno, aunque estos varían si la persona se casa, por ejemplo). Además, en el mundo hispanohablante, cada vez más se usan nombres que se originan de otros idiomas. Entendiendo entonces que este podía llegar a ser un gran reto para la precisión de este tutorial, tomamos algunas decisiones previas que debería tener en cuenta:

  - Pensando en la estructura más moderna de nombres en español, el código nada más reconocerá las siguientes formas de nombre:

    - **Primer nombre y apellido (usualmente el paterno)**
    - **Primer nombre, segundo nombre y apellido paterno**
    - **Primer nombre, segundo nombre, apellido paterno y apellido materno**

    Es decir, si una persona tiene más de dos nombres o si en una de las partes del nombre completo existe una abreviatura (tal y como Rafael **J.** Rodríguez), el segundo nombre en este caso será omitido y el modelo informático solamente imprimirá *Rafael Rodríguez*. 

    ​

- **2) Reconocimiento del nombre:** El código informático usado para esta lección básicamente compara el contenido del corpus textual con un archivo de texto plano previamente creado y recopilado, _nombres.txt_, que contiene una lista de 64,295 nombres y apellidos encontrados en db.pedia, CIDH y una hoja de cálculos que amablemente compartió con nosotros una organización sin ánimo de lucro en Guatemala llamada Grupo de Apoyo Mutuo. 

  Ya que comparamos la información del corpus con la de esta lista de nombres, tenga en cuenta que si un nombre o apellido no aparece en esta lista, algunos nombres serán omitidos por el código escrito. A largo plazo, la idea sería agregar más nombres a esta lista creada de nombres o que manualmente la persona incorpore estos nombres omitidos al finalizar el uso del modelo informático.

  ​

  **3) Omisión de ciertas puntuaciones únicas al español:** En la sección de Conocimiento previo, se explica que se usa una biblioteca de *Python* llamada *string*. *String* posee una función llamada *punctuation* que contiene todo tipo de puntuaciones usando el idioma inglés como base. Ya que en el español hay ciertos caracteres que son únicos en el idioma (tales como los signos de apertura de una exclamación, comilla o interrogación), el modelo infórmatico de este tutorial no los eliminará más adelante como lo hará con otros. Este no debería ser un problema de mayor trascendencia. No obstante, es importante resaltarlo. 

  ​


# Análisis y limpieza de texto #

Pensando en la mejor forma de estructurar esta lección, hemos decidido dividir la lección en dos partes: análisis y limpieza de texto y extracción de entidades nombradas. En esta primera parte, vamos a preparar el archivo de texto plano que tenemos de muestra [agregar enlace al archivo aquí] antes de poder realizar exitosamente la extracción de nombres de personas del corpus textual.



## Instalación de Python y pip ##

- ### Instalar Python 3

Este script usa un lenguaje de programación llamado Python. Muchas computadoras vienen con Python preinstalado. Para verificar si tiene Python versión 3 en su máquina, abra su interfaz de línea de comando (*Command Line Interface* en inglés). 

En una Mac, abra la terminal desde Launchpad. En Windows, haga clic en Inicio y seleccione Indicador de comando (*Command Prompt* en inglés). En el terminal, escriba `python3 --version`. Si obtiene el error de que "python3 no está definido", deberá instalar Python3.

Por lo tanto, continúe con el siguiente paso.

Con Mac, Windows o máquina Linux, descargue Python3 desde este [enlace](https://www.python.org/downloads/).

Se pueden encontrar más instrucciones en inglés [aquí](https://docs.python.org/3.7/using/index.html).

- ### Instalar pip

Para usar la secuencia de comandos de Python en su computadora local, primero deberá instalar el lenguaje natural
Tool Kit y una biblioteca llamada Pandas. Esto se puede hacer de manera muy simple utilizando pip, que es una herramienta estándar para instalar paquetes de Python. Para comprobar si tiene pip instalado, puede simplemente escribir `pip -h` en su
interfaz de línea de comando (Terminal en Max y símbolo del sistema en Windows). Si obtiene un error que "'pip' no es reconocido", escriba lo siguiente
en la linea de comando

Mac o Linux:
`python3 -m pip install --user virtualenv`
Windows:
`py -m pip install --user virtualenv`

Más detalles sobre pip se pueden encontrar en el tutorial,
[Instalar módulos de Python con pip](https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip).



## Crear un entorno virtual

Primero, instalaremos un paquete llamado virtualenv. Esto nos permite crear el ambiente
donde se ejecutará tu script En una Mac, abre la Terminal desde Launchpad. En Windows, haz clic en Comenzar
y seleccione Símbolo del sistema.

Con macOS o tipo de Windows:
`pip install virtualenv`

En Linux:
`sudo pip install virtualenv`

Cuando ejecutamos virtualenv, creará un directorio que contiene los archivos para el entorno.
Navegue a un directorio donde desea almacenar el proyecto. Si no estás seguro del camino,
puede arrastrar la carpeta al terminal y aparecerá la ruta a ese directorio.
Una vez que esté en el directorio deseado, escriba `virtualenv --python = python3 nombres`
Esto creará un nuevo entorno virtual ejecutando Python3 llamado 'nombres'.

Para activar el entorno, escriba `source. / Nombres / bin / activate`
Ahora debería ver `(nombres)` en el lado izquierdo de la terminal.



## Descargando el archivo de *Python* 

Una vez haya creado el ambiente virtual en el cual guardará todos los archivos con los que ha de trabajar - el archivo de *Python*, el archivo de texto plano con la lista de nombres (nombres.txt) y el archivo de texto plano para extraer los nombres (en este caso, los discursos políticos de Álvaro Uribe Vélez) -, proceda a descargar el archivo de *Python* que ejecutará el modelo informático


### Instalación de paquetes y bibliotecas de *Python*

Ahora que ha descargado archivo de *Python* el cual contiene toda la información de su modelo, está listo para comenzar a comprender lo que hace el modelo informático. Es en este momento cuando necesitará abrir su editor de texto que le permita hacer cambios a su *script* de *Python*. [Explicar cómo se abre el archivo de Python en el editor de texto]

Este primer paso importará todos los paquetes o bibliotecas de *Python* que necesitará a través de la lección. Las bibliotecas más relevantes para esta lección han sido brevemente explicadas en la sección de [Conocimiento previo][#Conocimiento-previo]. Para las otras que están incluidas en este tutorial, no se requiere que sepa mucho de ellas. Queda a discreción de usted como usuario el indagar más al respecto.


```python
import os
import nltk
import string
import re
from nltk.corpus import stopwords
import pandas as pd
from pandas.compat import StringIO
import urllib.request
import shutil
import tempfile
import subprocess
import platform
from tkinter.filedialog import askopenfilename
```


Además de importar estas bibliotecas de Python, también necesitará descargar ciertas aplicaciones de dos bibliotecas: *nltk* y *stopwords*. *Stopwords* es una biblioteca dentro de NLTK que contiene todas las palabras vacías del idioma español. Si no sabe que es esto de palabras vacías o *stopwords*, no se preocupe. Cuando lleguemos a usarlas más adelante en el tutorial, explicaremos porque son indispensables dentro de este modelo informático.

```python
nltk.download("stopwords")
#nltk.download('wordnet')
stopwords.words('spanish')
```



### Subiendo los archivos a trabajar al script de *Python*

Luego de haber instalado los paquetes y bibliotecas necesarios para trabajar con el modelo, es necesario que suba los archivos a trabajar a su *script* de *Python*. Recuerde que hay dos tipos de archivos con los que trabajaremos durante todo el tutorial: **nombres.txt** y el archivo de muestra (que usted puede cambiar o utilizar uno diferente), **alvaro_uribe_speeches_2007_2010.txt**.



Este fragmento de código abre una venta para que usted pueda importar el archivo de muestra. Una vez esta ventana se abra, diríjase al directorio (carpeta) dentro de su computador que le permita subir el archivo de muestra, **alvaro_uribe_speeches_2007_2010.txt**. 

```python
filename = askopenfilename()
```



Luego de subir el archivo de muestra al archivo de *Python*, tendrá que subir el archivo **nombres.txt** al mismo. Ya que nombres.txt contiene la lista de nombres con la cual compararemos el archivo de muestra, este documento no variará y podemos obtenerlo desde el enlace URL que aparece en el siguiente fragmento de código.

```python
if 'nombres.txt' not in os.listdir('./assets'):
  urllib.request.urlretrieve('https://raw.githubusercontent.com/rrodrigue2498/NER-with-NLTK/master/assets/nombres.txt','./assets/nombres.txt')
```


Si usted desea crear su propia lista de nombres, refiérase a la sección [Fuentes libres usadas para construir la lista de nombres][#fuentes-libres-usadas-para-construir-la-lista-de-nombres]. Aquí se explica cómo se obtuvo esta lista y se da algunas instrucciones de cómo poder generar su propia lista de nombres basado en su proyecto o investigación.



### Preparación del texto

Ahora que se entiende cómo se importaron todas las bibliotecas, paquetes y archivos necesarios para el tutorial, puede comenzar a trabajar en la primera parte más importante del modelo: preparación o limpieza del texto. Aquí limpiaremos un poco el texto para que se facilite el trabajo en la próxima parte de este tutorial - extracción de entidades nombradas (nombres propios).




# Extracción de entidades nombradas #



## Recopilación de nombres propios a partir de base de datos libres ##

La lista de nombres se creó a partir de una variedad de fuentes libres en la Internet. Esta lista que ha sido previamente gestionada para ser usada en este tutorial, también puede ser utilizada para la creación de listas personalizadas para su proyecto en español o en otros idiomas. Como estrategia general para extraer nombres propios en español, sugerimos construir una lista notoriamente extensa de nombres generales (como los que encontramos disponibles libremente en la Internet), así como también incluir datos específicos de su proyecto o conjunto particular de documentos. Esta combinación de datos generales y específicos tienden a producir mejores resultados.

El modelo informático de *Python* verifica cada token generado con esta extensa lista de nombres, apellidos y posibles apodos de una persona. Si el token se encuentra en esta lista, podemos estar relativamente seguros de que ha identificado la parte de un nombre. La lista que proporcionamos para este tutorial contiene 64,295 nombres únicos. De ese número, 17,297 son nombres y 48,923 son apellidos. La lista también incluye 270 diminutivos comunes.

A continuación, describiremos cómo se logró recopilar y procesar esta gran variedad de nombres y apellidos y las fuentes libres de donde se pudo conseguir esta información. Note que esta parte simplemente busca dar una explicación concisa de cómo se obtuvieron los nombres y cómo fueron procesados. Aunque se dan indicaciones de cómo hacerlo, el enfoque de este tutorial no es el de explicar a fondo como lograr este objetivo. En la siguiente sección, se dan consejos y se dirige a ciertos tutoriales del Programming Historian que pueden ser de mayor utilidad si este es su interés.

### Fuentes libres usadas para construir la lista de nombres ###

- #### DBpedia, base de datos de Wikipedia ####

La mayor cantidad de nombres en nuestra lista proviene de DBpedia. Usando datos enlazados, es posible encontrar todos los nombres en Wikipedia y guardarlos en un archivo CSV. Lo hicimos usando el lenguaje de consulta SPARQL (http://es.dbpedia.org/sparql). Para más información sobre datos enlazados y SPARQL, consulte el siguiente tutorial encontrado en el Programming Historian:

[Uso de SPARQL para acceder a los datos abiertos enlazados](https://programminghistorian.org/es/lecciones/sparql-datos-abiertos-enlazados) por Matthew Lincoln. 

DBpedia solo arroja 10,000 resultados a la vez. Dada esta limitación, creamos consultas de nombre para cada letra en el alfabeto. En la mayoría de los casos, había menos de 10,000 nombres únicos, pero en otros, solo incluímos los 10,000 nombres como resultado. No obstante, se puede generar un conjunto más grande de nombres con consultas más específicas. Tenga en cuenta que usamos expresiones regulares (mencionadas previamente en la sección de *Conocimiento previo*) para seleccionar nombres por letra.

Ejemplo de como se obtiene nombres desde DBpedia que usando SPARQL:

En la línea FILTER REGEX (filtro de expresión regular) de la nota de consulta "^Ñ", la zanahoria (^) selecciona los nombres al comienzo de la cadena con la letra Ñ. 

```sparql
SELECT DISTINCT ?given 
WHERE {
?person foaf:givenName ?given .
FILTER REGEX(STR(?given), "^Ñ") .
}
```

Esta línea FILTER REGEX (filtro de expresión regular) de la nota de consulta "^Z" identifica todos los apellidos comenzados por Z. La zanahoria (^) selecciona los apellidos al comienzo de la cadena con la letra Z. 

```sparql
SELECT DISTINCT ?sur  
WHERE {
?person foaf:surname ?sur .
FILTER REGEX(STR(?sur), "^Z") .
} 
```

Más información sobre expresiones regulares está disponible en:

 ["Comprensión de expresiones regulares" por Doug Knox](https://programminghistorian.org/en/lessons/understanding-regular-expressions).

También se usó el lenguaje Amigo de un amigo (*Friend of a Friend* en inglés) para identificar nombres en las entradas de DBpedia. El FOAF [givenName](http://xmlns.com/foaf/spec/#term_givenName) es el término más general que podríamos encontrar para identificar nombres. [Apellido](http://xmlns.com/foaf/spec/#term_surname) se seleccionó sobre [nombre de familia](http://xmlns.com/foaf/spec/#term_familyName) dado el número relativamente mayor de resultados en español. La lista final debe entenderse como el mejor esfuerzo para obtener tantos nombres únicos de DBpedia como fuera posible. Por favor, siéntase libre de descargar [nuestra lista](https://github.com/programminghistorian/jekyll/tree/gh-pages/assets/.../nombres.txt) y modificarla de acuerdo a su proyecto o investigación.

Para ejecutar las consultas usted mismo, simplemente vaya a [es.dbpedia.org/sparql](http://es.dbpedia.org/sparql). A continuación, puede copiar y pegar las consultas anteriores en la interfaz de búsqueda. *Endpoints* similares están disponibles en [inglés](https://dbpedia.org/sparql), [holandés](http://nl.dbpedia.org/sparql), [griego](http://el.dbpedia.org/sparql), [polaco](http://pl.dbpedia.org/sparql).

- #### Conjuntos de datos publicados en la web ####

Algunos de los nombres en nuestra lista provienen de una búsqueda web simple para encontrar conjuntos de datos existentes. En el sitio data.world, Alexander Cruz ha publicado [listas](https://data.world/axtscz/spanish-first-name) de nombres masculinos y femeninos en español. Si bien la mayoría de ellos repiten nombres encontrados en los datos de DBpedia, aun así vale la pena ver qué datos están disponibles gratuitamente. 

 -  #### Datos del Centro Internacional para Investigaciones en Derechos Humanos (CIIDH) - Diccionario ####

Dado que este tutorial se creó con el fin de apoyar un proyecto actual relacionado con una organización en Guatemala, usamos la base de datos del Centro Internacional para Investigaciones en Derechos Humanos (CIIDH) de dicho país. El conjunto de datos del CIIDH incluye varios datos sobre violaciones de derechos humanos en Guatemala durante el período 1960-1996. La lista es particularmente útil dado el gran número de nombres indígenas de la región en la base de datos. Los datos del CIIDH están disponibles gratuitamente como un archivo CSV en este [enlace](https://hrdag.org/wp-content/uploads/2014/01/atv201.csv.zip).
Dichos datos del CIIDH contienen 13,838 nombres, 13,594 nombres paternos familiares y 8,505 apellidos maternos.

-  #### Base de datos del Grupo de Apoyo Mutuo

Como parte de un proyecto para digitalizar los registros de la organización de derechos humanos más antigua de Guatemala, incluimos nombres de los registros específicos que planeamos consultar con dicha organización. A medida que el archivo se cataloga, se agrega el nombre completo de las personas referenciadas en cada archivo o folio. 



## #

## Cuaderno (libreta) de *Google Colaboratory* ##

Para hacer las cosas lo más simples posible, hemos creado un cuaderno donde puede ejecutar el script
sin tener que hacer ningún cambio en su computadora. No requiere más que una conexión a Internet y un navegador. Para acceder a nuestra computadora portátil, haga clic en el siguiente enlace.

[Enlace a la versión del guión de Colab Notebook.](Https://colab.research.google.com/drive/1HlAjZDW4OF68-PMtgWj-pDviGch71jZp#scrollTo=S-f7YGEJHvWw)

A continuación, proporcionamos instrucciones sobre cómo descargar el script y ejecutarlo localmente en su computadora, si lo prefiere.















[#Retos]: #Retos
[#fuentes-libres-usadas-para-construir-la-lista-de-nombres]: #fuentes-libres-usadas-para-construir-la-lista-de-nombres
[#Conocimiento-previo]: #Conocimiento-previo
