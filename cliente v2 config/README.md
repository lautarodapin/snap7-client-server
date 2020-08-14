## Ficheros que se requieren


# Valores
|----|----|------|----|---|
|area|tipo|numero|byte|bit|
|----|----|------|----|---|
* area: nombre del area del servidor sacada del modulo de la librearia "snap7.snap7types". Valores: ,
        * "S7AreaPE"
        * "S7AreaPA"
        * "S7AreaMK"
        * "S7AreaDB"
        * "S7AreaCT"
        * "S7AreaTM"
* tipo: nombre del tipo de variable que se debe leer, sacada del modulo "snap7.snap7types". Valores:
        * "S7WLBit"
        * "S7WLByte"
        * "S7WLWord"
        * "S7WLDWord"
        * "S7WLReal"
        * "S7WLCounter"
        * "S7WLTimer"
* numero: en el caso de que el area sea un DB, es el numero del DB. Si es una marca, salida o entrada es 0.
* byte: offset de la variable, ej, DB1.DBD100, en este caso el offset es 100.
* bit: bit de la variable, ej, DB1.DBX101.4 en este caso es 4. En caso de que no tenga se coloca 0.


# TODO cambiar funciones por la funcion "set_value"