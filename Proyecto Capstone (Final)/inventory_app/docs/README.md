# Documentación del Sistema de Gestión de Inventario

Esta carpeta contiene toda la documentación técnica del proyecto.

## Índice de Documentos

### 1. [README_PROYECTO.md](README_PROYECTO.md)
Información general del sistema, cómo ejecutarlo y funcionalidades principales.
- Descripción del sistema
- Instrucciones de instalación y ejecución
- Lista completa de funcionalidades
- Estructura del proyecto
- Tecnologías utilizadas

### 2. [modelos_bd.md](modelos_bd.md)
Documentación detallada de la base de datos.
- Descripción de las tablas (suppliers y products)
- Columnas, tipos de datos y restricciones
- Relaciones entre tablas
- Diagrama de relación entidad
- Ejemplos de datos

### 3. [endpoints.md](endpoints.md)
Referencia completa de todas las rutas (endpoints) de la aplicación.
- Tabla de endpoints con métodos HTTP
- Descripción detallada de cada ruta
- Parámetros requeridos y opcionales
- Validaciones implementadas
- Códigos de respuesta HTTP

### 4. [arquitectura.md](arquitectura.md)
Explicación de la arquitectura del sistema.
- Diagrama de arquitectura general
- Flujo de datos entre componentes
- Explicación de cada capa (Navegador → Flask → SQLAlchemy → SQLite)
- Patrones de diseño utilizados (MVC)
- Consideraciones de seguridad

---

## Cómo Usar Esta Documentación

1. **Para empezar**: Lee [README_PROYECTO.md](README_PROYECTO.md) para entender qué hace el sistema y cómo ejecutarlo.

2. **Para entender la base de datos**: Consulta [modelos_bd.md](modelos_bd.md) para ver la estructura de las tablas.

3. **Para desarrollo/API**: Revisa [endpoints.md](endpoints.md) para conocer todas las rutas disponibles.

4. **Para comprender el diseño**: Lee [arquitectura.md](arquitectura.md) para entender cómo funciona el sistema internamente.

---

## Información Adicional

- **Proyecto**: Sistema de Gestión de Inventario
- **Framework**: Flask 3.x
- **Base de Datos**: SQLite
- **ORM**: SQLAlchemy
- **Lenguaje**: Python 3.x

---

## Capturas de Pantalla

Las capturas de pantalla del sistema se encuentran en la carpeta [screenshots/](screenshots/)
