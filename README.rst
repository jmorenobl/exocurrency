=======================
ExoCurrency
=======================

---------
Requisitos
---------

* Docker (Para levantar la base de datos PostgreSQL)
* Python3
* Virtualenv o Pipenv (Opcional pero recomenddado)
* Make (para ejecutar los comandos)

--------
Arranque
--------

Clonar el proyecto con el siguiente comando:

.. code-block:: bash

    $ git clone ...
    $ cd exocurrency

Crear el entorno virtual (OPCIONAL):

.. code-block:: bash

    $ mkvirtualenv exocurrency


Instalar los requisitos via pip:

.. code-block:: bash

    (exocurrency)$ pip install -r requirements/local.txt

Init app:

.. code-block:: bash

    (exocurrency)$ mv example.env .env
    (exocurrency)$ make initapp


Este último comando iniciará el proceso de inicialización que consiste en los siguientes pasos:

1. Crear e inicializar el contenedor de PostgreSQL
2. Ejecutar las migraciones
3. Pedir datos por la consola para crear el superusuario.

---
Uso
---

Los endpoints disponibles son:

* /currency/rates/?fromDay=01-07-2018&toDay=15-07-2018 => Listado de ratios de divisas para un periodo de tiempo 
* /currency/exchange/EUR/GBP/10/ => Calcula una cantidad de una divida en otro 'BASE/TARGET/amount'
* /currency/time-weighted-rate/EUR/USD/1000/?fromDay=26-07-2018 => Devuelve el twrr para una cantidad invertida en una 
divisa desde el día especificado hasta hoy.