# ¿Qué es GoLISMERO? #
GoLISMERO es un **spider web** capaz de **detectar vulnerabilidades** y **formatear los resultados** de forma muy útil cuando se afronta una auditoría web.

# ¿Para qué sirve? #
GoLISMERO está pensado para ser un primer paso cuando comenzamos una auditoría de seguridad web.

Cada vez que nos enfrentamos a una **nueva URL**, ¿no sería genial poder disponer **de forma sencilla** y rápida de **todos** los **enlaces, formularios** con sus **parámetros**, detectar posibles **URL vulnerables** y que además de que se presentasen de manera que nos permita hacernos una idea de la todos los puntos de entrada donde podríamos lanzar ataques? **GoLISMERO nos permite hacer todo esto.**

# Aprendiendo con ejemplos #

### **Recuerda: Para ejecutar correctamente GoLismero necesitas python 2.7.X or superior.** ###

A continuación se exponen diversos ejemplos y casos prácticos, que son la mejor forma de aprender a usar una herramienta de seguridad:

  1. Extraer todos los enlaces y formularios de una web, con todos sus parámetros, en formato extendido:

`GoLISMERO.py –t google.com`

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/x110911_1801_GoLISMEROSi12.png.pagespeed.ic.Xewovcm3yz.png' />

  1. Extraer todos los enlaces, en modo compacto y colorear la salida.

`GoLISMERO.py –c –m –t google.com`

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/x110911_1801_GoLISMEROSi22.png.pagespeed.ic.S5Cs2lcYJa.png' />

  1. Extraer solo los enlaces. Quitando css, javascript, imágenes y direcciones de correo.

`GoLISMERO.py --no-css--no-script --no-images --no-mail –c –A links –m –t google.com`

O, formato reducido:

`GoLISMERO.py –na –c –A links –m –t google.com`

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/golismero_google_3-1024x882.png.pagespeed.ce.Hoki-xr7Dd.png' />

  1. Extraer solamente los enlaces que tienen parámetros, seguir las redirecciones (HTTP 302) y exportar en HTML los resultados.

`GoLISMERO.py –c –A links --follow –F html –o results.html –m –t google.com`

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/x110911_1801_GoLISMEROSi43.png.pagespeed.ic.2lJh2Hy8jH.png' />

Y el HTML de resultados generado:

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/x110911_1801_GoLISMEROSi53.png.pagespeed.ic.wYdeAb8WuU.png' />

  1. Extraer todos los enlaces, buscar URL potencialmente vulnerables y utilizar un proxy intermedio para el análisis. Las URLs o parámetros vulnerables serán resaltados en rojo.

`GoLISMERO.py –c –A links --follow -na –x –m –t terra.com`

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/golismer_terra_1-1024x702.png' />

Comprobamos como ZAP Proxy captura la petición:

<img src='http://www.iniqua.com/wp-content/uploads/2011/11/x110911_1801_GoLISMEROSi71.png.pagespeed.ic.blW7vCO2YW.png' />