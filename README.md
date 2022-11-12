# Libro Sueldos Digital

### Libro Sueldos Digital - Simple exportador desde txt F.931

El objetivo es simplificar el proceso para generar el txt exportador para LSD desde txt F.931 para quienes no cuenten con un sistema para este fin.
El código es abierto para todos.


## Puntos a considerar

### Exportación Básica

_Legajos predeterminado por orden, o sea 1, 2, 3, etc. No configurable por el momento_

_Lugar de Trabajo igual para toda la nómina de acuerdo a la configuración_

_Tratamiento de todas liquidaciones mensuales o quincenales como una única liquidación mensual_

_Retroactivos no tratados_

_Pendiente tratar análisis sobre el tope_

_Eventuales: Pendiente fecha de ingreso y de egreso_

### Exportación Avanzada

_No está alcanzado el pago por CBU_

---

### TODO List
#### Panel Control

* Resumen, cantidad de liquidaciones, empleados y total remuneración

#### Exportación avanzada

* Configurar 'M'=mes; 'Q'=quincena; 'S'=semanal
* Configurar días base
* Si borra liquidación recalcular totales
* Configurar forma de pago. No acreditación porque requiere CBU
* Ver cálculo de la Base Adicional OS.
* Borrar los txt temporales
* Al crear una presentación ver si hay una cerrada y preguntar si sobreescribir
* Permitir descargar archivos de presentaciones cerradas

---

### Future versions TODO List

#### Exportación avanzada
* Agregar parametrización de conceptos para no tener la necesidad de la columna Tipo
* Eventuales

#### Empleados
* Borrado masivo y ver si exportación conviene pisar

#### General
* Manejador de 404