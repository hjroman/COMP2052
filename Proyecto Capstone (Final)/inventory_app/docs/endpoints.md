# Endpoints de la API Web

## Descripción General

Este documento describe todas las rutas (endpoints) disponibles en el sistema de gestión de inventario. Cada ruta especifica el método HTTP permitido, la URL y una descripción de su funcionalidad.

---

## Tabla de Endpoints

### Ruta Principal

| Ruta | Método HTTP | Descripción |
|------|-------------|-------------|
| `/` | GET | Redirige automáticamente a la lista de productos (`/products`) |

---

### Endpoints de Proveedores (Suppliers)

| Ruta | Método HTTP | Descripción |
|------|-------------|-------------|
| `/suppliers` | GET | Lista todos los proveedores registrados con su información de contacto y cantidad de productos |
| `/suppliers/new` | GET | Muestra el formulario para crear un nuevo proveedor |
| `/suppliers/new` | POST | Procesa el formulario y crea un nuevo proveedor en la base de datos |
| `/suppliers/<int:supplier_id>/edit` | GET | Muestra el formulario para editar un proveedor existente |
| `/suppliers/<int:supplier_id>/edit` | POST | Procesa el formulario y actualiza la información del proveedor |
| `/suppliers/<int:supplier_id>/delete` | POST | Elimina un proveedor (solo si no tiene productos asociados) |

---

### Endpoints de Productos (Products)

| Ruta | Método HTTP | Descripción |
|------|-------------|-------------|
| `/products` | GET | Lista todos los productos del inventario. Permite filtrar por proveedor usando el parámetro `?supplier_id=X` |
| `/products/new` | GET | Muestra el formulario para crear un nuevo producto |
| `/products/new` | POST | Procesa el formulario y crea un nuevo producto en la base de datos |
| `/products/<int:product_id>/edit` | GET | Muestra el formulario para editar un producto existente |
| `/products/<int:product_id>/edit` | POST | Procesa el formulario y actualiza la información del producto |
| `/products/<int:product_id>/delete` | POST | Elimina un producto del inventario |

---

### Endpoints de Reportes

| Ruta | Método HTTP | Descripción |
|------|-------------|-------------|
| `/reports/low-stock` | GET | Muestra productos con stock bajo. Parámetro opcional: `?threshold=X` (por defecto: 5 unidades) |

---

## Detalles de Endpoints

### 1. Página Principal
**Endpoint**: `/`
**Método**: GET
**Descripción**: Redirige a la lista de productos
**Respuesta**: Redirección 302 a `/products`

---

### 2. Listar Proveedores
**Endpoint**: `/suppliers`
**Método**: GET
**Descripción**: Muestra una tabla con todos los proveedores registrados
**Parámetros**: Ninguno
**Respuesta**: Página HTML con tabla de proveedores
**Datos mostrados**:
- ID del proveedor
- Nombre
- Email de contacto
- Teléfono
- Cantidad de productos asociados
- Botones de acción (Editar, Eliminar)

---

### 3. Crear Proveedor (Formulario)
**Endpoint**: `/suppliers/new`
**Método**: GET
**Descripción**: Muestra el formulario para crear un nuevo proveedor
**Parámetros**: Ninguno
**Respuesta**: Página HTML con formulario vacío

---

### 4. Crear Proveedor (Procesar)
**Endpoint**: `/suppliers/new`
**Método**: POST
**Descripción**: Procesa los datos del formulario y crea un nuevo proveedor
**Parámetros del formulario**:
- `name` (obligatorio): Nombre del proveedor
- `contact_email` (opcional): Email de contacto
- `phone` (opcional): Número de teléfono

**Validaciones**:
- Nombre es obligatorio
- Email debe contener '@' si se proporciona

**Respuesta exitosa**: Redirección a `/suppliers` con mensaje de éxito
**Respuesta con errores**: Formulario con lista de errores

---

### 5. Editar Proveedor (Formulario)
**Endpoint**: `/suppliers/<int:supplier_id>/edit`
**Método**: GET
**Descripción**: Muestra el formulario para editar un proveedor existente
**Parámetros URL**: `supplier_id` (ID del proveedor)
**Respuesta**: Página HTML con formulario prellenado
**Error 404**: Si el proveedor no existe

---

### 6. Editar Proveedor (Procesar)
**Endpoint**: `/suppliers/<int:supplier_id>/edit`
**Método**: POST
**Descripción**: Actualiza la información de un proveedor existente
**Parámetros URL**: `supplier_id` (ID del proveedor)
**Parámetros del formulario**: Mismos que crear proveedor
**Validaciones**: Mismas que crear proveedor
**Respuesta exitosa**: Redirección a `/suppliers` con mensaje de éxito
**Respuesta con errores**: Formulario con lista de errores

---

### 7. Eliminar Proveedor
**Endpoint**: `/suppliers/<int:supplier_id>/delete`
**Método**: POST
**Descripción**: Elimina un proveedor del sistema
**Parámetros URL**: `supplier_id` (ID del proveedor)
**Restricción**: No permite eliminar si el proveedor tiene productos asociados
**Respuesta exitosa**: Redirección a `/suppliers` con mensaje de éxito
**Respuesta con error**: Redirección a `/suppliers` con mensaje de advertencia
**Error 404**: Si el proveedor no existe

---

### 8. Listar Productos
**Endpoint**: `/products`
**Método**: GET
**Descripción**: Muestra todos los productos del inventario
**Parámetros query string** (opcionales):
- `supplier_id`: Filtra productos por proveedor específico

**Ejemplos**:
- `/products` - Muestra todos los productos
- `/products?supplier_id=1` - Muestra solo productos del proveedor 1

**Respuesta**: Página HTML con tabla de productos
**Datos mostrados**:
- ID del producto
- Nombre del proveedor
- Nombre del producto
- SKU
- Stock actual
- Precio unitario
- Botones de acción (Editar, Eliminar)

---

### 9. Crear Producto (Formulario)
**Endpoint**: `/products/new`
**Método**: GET
**Descripción**: Muestra el formulario para crear un nuevo producto
**Verificación previa**: Verifica que exista al menos un proveedor
**Respuesta**: Página HTML con formulario
**Redirección**: Si no hay proveedores, redirige a `/suppliers` con mensaje de advertencia

---

### 10. Crear Producto (Procesar)
**Endpoint**: `/products/new`
**Método**: POST
**Descripción**: Procesa los datos y crea un nuevo producto
**Parámetros del formulario**:
- `supplier_id` (obligatorio): ID del proveedor
- `name` (obligatorio): Nombre del producto
- `sku` (obligatorio): Código SKU único
- `stock` (obligatorio): Cantidad en stock (número entero, e 0)
- `unit_price` (obligatorio): Precio unitario (número decimal, e 0)

**Validaciones**:
- Todos los campos son obligatorios
- SKU debe ser único (no puede existir otro producto con el mismo SKU)
- Stock debe ser entero no negativo
- Precio debe ser número no negativo

**Respuesta exitosa**: Redirección a `/products` con mensaje de éxito
**Respuesta con errores**: Formulario con lista de errores

---

### 11. Editar Producto (Formulario)
**Endpoint**: `/products/<int:product_id>/edit`
**Método**: GET
**Descripción**: Muestra el formulario para editar un producto existente
**Parámetros URL**: `product_id` (ID del producto)
**Respuesta**: Página HTML con formulario prellenado
**Error 404**: Si el producto no existe

---

### 12. Editar Producto (Procesar)
**Endpoint**: `/products/<int:product_id>/edit`
**Método**: POST
**Descripción**: Actualiza la información de un producto existente
**Parámetros URL**: `product_id` (ID del producto)
**Parámetros del formulario**: Mismos que crear producto
**Validaciones**:
- Mismas que crear producto
- SKU debe ser único excepto para el producto actual

**Respuesta exitosa**: Redirección a `/products` con mensaje de éxito
**Respuesta con errores**: Formulario con lista de errores

---

### 13. Eliminar Producto
**Endpoint**: `/products/<int:product_id>/delete`
**Método**: POST
**Descripción**: Elimina un producto del inventario
**Parámetros URL**: `product_id` (ID del producto)
**Respuesta exitosa**: Redirección a `/products` con mensaje de éxito
**Error 404**: Si el producto no existe

---

### 14. Reporte de Stock Bajo
**Endpoint**: `/reports/low-stock`
**Método**: GET
**Descripción**: Muestra productos cuyo stock está por debajo de un umbral configurable
**Parámetros query string** (opcionales):
- `threshold`: Umbral de stock (por defecto: 5)

**Ejemplos**:
- `/reports/low-stock` - Muestra productos con stock < 5
- `/reports/low-stock?threshold=10` - Muestra productos con stock < 10

**Respuesta**: Página HTML con tabla de productos con stock bajo
**Orden**: Productos ordenados por stock ascendente (menor stock primero)

---

## Códigos de Respuesta HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 OK | Solicitud exitosa | Al mostrar páginas, listas, formularios |
| 302 Found | Redirección temporal | Después de crear/editar/eliminar registros |
| 404 Not Found | Recurso no encontrado | Cuando un proveedor o producto no existe |
| 500 Internal Server Error | Error del servidor | Errores no controlados en el servidor |

---

## Mensajes Flash

El sistema utiliza mensajes flash para informar al usuario sobre el resultado de las operaciones:

| Categoría | Tipo de Mensaje | Ejemplo |
|-----------|-----------------|---------|
| `success` | Operación exitosa | "Proveedor creado exitosamente." |
| `danger` | Error o prohibición | "No se puede eliminar un proveedor con productos asociados." |
| `warning` | Advertencia | "Debe crear al menos un proveedor antes de crear productos." |

---

## Notas de Seguridad

1. **Protección CSRF**: Se recomienda implementar tokens CSRF en producción
2. **Validación del lado del servidor**: Todas las validaciones se realizan en el servidor
3. **Confirmaciones JavaScript**: Operaciones destructivas (eliminar) requieren confirmación del usuario
4. **SQL Injection**: Protegido automáticamente por SQLAlchemy ORM
