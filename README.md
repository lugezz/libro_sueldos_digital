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
### Paso a paso puesta en marcha

* Crear estos registros en TipoLiquidación

    1: Datos referenciales del envío (Liquidación de SyJ y datos para DJ F931)
    2: Datos referenciales de la Liquidación de SyJ del trabajador
    3: Detalle de los conceptos de sueldo liquidados al trabajador
    4: Datos del trabajador para el calculo de la DJ F931
    5: Datos del trabajador de la empresa de servicios eventuales - Dec 342/1992

* Acceder a exportadb-f931/

* Acceder a exportadb

* Vincular registros 4 con lo detallado en F.931

### TODO List

#### Exportación avanzada

* Configurar 'M'=mes; 'Q'=quincena; 'S'=semanal

---

### Future versions TODO List

#### Exportación avanzada
* Agregar parametrización de conceptos para no tener la necesidad de la columna Tipo
* Eventuales
* Ver cálculo de la Base Adicional OS.
* Configurar días base
* Configurar forma de pago. No acreditación porque requiere CBU


#### Empleados
* Borrado masivo y ver si exportación conviene pisar

#### General