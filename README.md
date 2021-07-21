# BD de peliculas y series

### Datos técnicos.
La pagina funciona con un contenedor de Docker el cual levanta los servicios utilizados.

Servicios:
- Django
- DB: Postgres
- Tareas Asincronas: Celery, Worker: RabbitMQ, Monitoreo: Flower
- Caché: Redis

### Funcion de la Página:
La funcion principal de la Pagina es registrar las Peliculas y Series vistas por un usuario.

Para ingresar a la pagina se debe realizar una autentificacion de usuario.
Para la misma se usó el sistema de autentificacion por defecto de Django.

Se obtienen los datos de las peliculas y series a traves de una API llamada [IMDBpy](https://github.com/alberanid/imdbpy "IMDBpy")
Se creó un buscador en la pagina principal en el cual vamos trayendo los datos; la logica principal se realiza al buscar
una pelicula y chekear si está en la DB en caso de que otro usuario ya haya agregado la misma. En caso de que ya este, solo
la agrega al perfil de Peliculas / Series vistas del usuario.

Los datos que se agregan al perfil del usuario son:
- Fecha en la que se vio la pelicula.
- Duración.
- Casting.
- Directores (en caso de que sea Pelicula)

Luego con estos datos se hacen informes mensuales con los que ir
comparando a traves del tiempo

# DB Design:
![drawSQL-export-2021-07-04_19_29](https://user-images.githubusercontent.com/35976464/124401131-28d84c80-dcfe-11eb-9563-f209b05c4f0f.png)

## Imagenes del proyecto

> El diseño del Front-End es representativo, se está desarrollando el mismo.
------------


Buscador en pagina principal
![PyS1](https://user-images.githubusercontent.com/35976464/126568729-29e466b2-733b-4cc8-8698-4f7ff7b9b288.png)

------------


Datos a agregar de Pelicula / Serie vista
![PyS2](https://user-images.githubusercontent.com/35976464/126568738-f8b3b560-f8d9-4539-9508-9d572516857e.png)

------------


Lista de las peliculas vistas
![PyS3](https://user-images.githubusercontent.com/35976464/126568741-69273bf9-e2ee-49cf-b334-511c84c175a6.png)
