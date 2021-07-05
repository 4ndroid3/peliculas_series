# BD de peliculas y series

### Datos técnicos.
La pagina funciona con un contenedor de Docker el cual levanta nuestros servicios.

Servicios:
- Django
- DB: Postgres
- Tareas Asincronas: Celery, Worker: RabbitMQ, Monitoreo: Flower
- Caché: Redis

### Funcion de la Página:
La funcion principal de la Pagina es registrar las Peliculas y Series vistas por un usuario.

Para ingresar a la pagina se debe realizar una autentificacion de usuario.
Para la misma se usó el sistema de autentificacion por defecto de Django.

Se obtienen los datos de las peliculas y series a traves de una API llamada IMDBpy (https://github.com/alberanid/imdbpy)
Se creo un buscador en la pagina principal en el cual vamos trayendo los datos; la logica principal se realiza al buscar
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
