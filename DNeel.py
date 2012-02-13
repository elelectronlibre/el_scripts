# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 20:10:28 2012

@author: Daniel Rodríguez (elelectronlibre.wordpress.com)
Sencillo script para importar y analizar datos estadísticos de Libre Office Calc,
proveyendo el histograma,la distribución normal que más se ajusta a este,
la mediana, media y distribución estándar partiendo de un array de datos de 
1 dimensión .

El formato en el que deben estar los datos en la hoja de cálculo es:
      Fila 1  (.........)
      Fila 2  (Títulos)
           .
           .   (Datos)
           .
           .
Antes de ejecutar el script, hay que abrir LibreOffice con el siguiente comando:
$ libreoffice --calc [ubicación del archivo] --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
Sustituir [ubicación del archivo] por el archivo a analizar, por ejemplo:

$ libreoffice --calc ~/Documentos/estadisticas.ods --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
   
    
Uso :[python DNeel.py cabecero datos

En el primer comando se indica qué columna usar (por ejemplo "Enero") y en el
segundo el número de datos a analizar de esa columna, empezando por la siguiente
al título (por ejemplo 31)

ejemplo de llamada: python python DNeel.py Enero 31

licencia: GPL3

version: 0.1

Más información en: www.elelectronlibre.wordpress.com
"""



#!/usr/bin/env python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from oosheet import OOSheet as S
import re
import sys

datos = []
def parsestats(titulo,cantidad):
    for column in S('Dias.b2:k2').columns:
        if re.search(column.string, titulo):
            match = re.search(r'.(\w)(\d)',str(column))
            if match:
                columna = match.group(1)
                print columna
                fila = match.group(2)
                print fila
                break
            else: print 'No encontrado'
            
    
    for row in S('Dias.'+str(columna)+str(int(fila)+1)+':'+str(int(fila)+int(cantidad))).rows:
        datos.append(row.value)
        print row
        print row.value
    # the histogram of the data
    n, bins, patches = plt.hist(datos, max(datos)-min(datos), facecolor='orange', alpha=0.75)
    mediana = np.median(datos)
    mu = np.mean(datos)
    sigma = np.std(datos)
    # add a 'best fit' line
    y = max(datos)*mlab.normpdf( bins, mu, sigma)
    #dnmedia = max(datos)*mlab.normpdf( bins, media, sigma)
    plt.plot(bins, y, 'b--', linewidth=1)
    plt.axvline(mediana, linestyle = '--',color = 'red', linewidth=1)
    plt.axvline(mu, linestyle = '--',color = 'b', linewidth=1)
    
    plt.xlabel('Visitas diarias')
    plt.ylabel('Ocurrencia')
    plt.title('Datos de '+str(titulo))
    texto = '$\mu=%.2f$\n$\mathrm{mediana}=%.2f$\n$\sigma=%.2f$'%(mu, mediana, sigma)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*max(datos),0.95*max(n), texto, fontsize=14,
        verticalalignment='top', bbox=props)    
    plt.grid(True) 
    plt.show()


print sys.argv[1]
print sys.argv[2]
if sys.argv[1] == 'help':
    print 'Programa para analizar datos estadísticos, proveyendo el histograma,\
    la distribución normal que más se ajusta a este, la mediana, media y \
    distribución estándar. Uso :[python DNel.py titulo cantidad]'
else:
    print '\
    DNeel v = 0.1 \n \
    Autor: Daniel Rodríguez García \n \
    blog: elelectronlibre.wordpress.com \n \
    licencia: GPL 3 \n \
    fecha: 13/2/2012'
    parsestats(sys.argv[1],sys.argv[2])


