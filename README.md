# Demucs
Este contener instalal Facebook Demucs y entrega una muy simple API para trabajar desde el navegador

## Como se usa
Hacer correr la aplicacion con `docker run -p 5000:5000 <nombre de la imagen>` luego entrar por medio del navegador
a http://localhost:5000. En esta pantalla se puede subir la cancion.

Existen 2 rutas mas `/uploads` que entrega una lista de todos los archivos disponibles, en caso de convertir varias canciones
aparecera la carpeta de cada cancion y `/uploads/<path a archivo>` donde se ingresa todo el path correspondiente con el nombre del archivo
para escucharlo o descargarlo

## Notas
Cuando se carga una cancion se comienza a hacer la separacion de tracks, esto se hace en otro hilo pero no vuelve bien.
Posiblemente ejecutar un thread.join() pueda ayudar. Aunque no regrese bien, separa los archivos de manera correcta.

Quizas sea posible mejorar esto pero aparentemente es necesario crear un entorno Celery que necesita una DB redis para 
entregar los mensajes, asi que por ahora queda asi