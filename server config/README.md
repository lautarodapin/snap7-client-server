## Ficheros que se requieren

# 1. Areas del servidor
Se debe crear un archivo llamado "server areas.csv" con las siguientes columnas:
|----|------|------|----|
|area|numero|nombre|size|
|----|------|------|----|
    * area: nombre del area del servidor sacada del modulo de la librearia "snap7.snap7types". Valores: ,
        * "S7AreaPE"
        * "S7AreaPA"
        * "S7AreaMK"
        * "S7AreaDB"
        * "S7AreaCT"
        * "S7AreaTM"
    * numero: en el caso de entradas, marcas o salidas siempre es cero, en el caso de DBs es el numero del DB.
    * nombre: nombre de la variable, esta se utilizara para asignar valores de inicio en el otro fichero.
    * size: tamaño del area, en el caso de los DBs seria el offset maximo.

# 2. Valores
|------|-------|----|---|-----|
|nombre|funcion|byte|bit|valor|
|------|-------|----|---|-----|
    * nombre: nombre del area asignada en el fichero anterior
    * funcion: nombre de la funcion que se utilizara para asignar el valor. Esta funcion se saca del modulo "snap7.util". Funciones:
        * "set_bool"
        * "set_real"
        * "set_int"
        * "set_dword"
        * "set_string"
    * byte: offset de la variable, ej, DB1.DBD100, en este caso el offset es 100.
    * bit: bit de la variable, ej, DB1.DBX101.4 en este caso es 4.
    * valor: dependiendo del tipo de variable que se asigne, 1 es true, 0 es false, y se utiliza punto para decimales.




# TODO cambiar funciones por la funcion "set_value"