# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Supplier, Product

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Conectar SQLAlchemy con Flask
    db.init_app(app)

    # Crear las tablas en la base de datos (si no existen)
    with app.app_context():
        db.create_all()

    register_routes(app)
    return app

def register_routes(app):
    @app.route("/")
    def index():
        return redirect(url_for("list_products"))
    
    # ---------- SUPPLIERS ----------
    @app.route("/suppliers")
    def list_suppliers():
        suppliers = Supplier.query.order_by(Supplier.name).all()
        return render_template("suppliers_list.html", suppliers=suppliers)
    
    @app.route("/suppliers/new", methods=["GET", "POST"])
    def create_supplier():
        errors = []
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            contact_email = request.form.get("contact_email", "").strip()
            phone = request.form.get("phone", "").strip()

            # Validación sencilla
            if not name:
                errors.append("El nombre del proveedor es obligatorio.")
            if contact_email and "@" not in contact_email:
                errors.append("El email de contacto no es válido.")

            if not errors:
                supplier = Supplier(
                    name=name,
                    contact_email=contact_email or None,
                    phone=phone or None,
                )

                db.session.add(supplier)
                db.session.commit()
                flash("Proveedor creado exitosamente.", "success")
                return redirect(url_for("list_suppliers"))

        return render_template("supplier_form.html", errors=errors, supplier=None)

    @app.route("/suppliers/<int:supplier_id>/edit", methods=["GET", "POST"])
    def edit_supplier(supplier_id):
        supplier = Supplier.query.get_or_404(supplier_id)
        errors = []

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            contact_email = request.form.get("contact_email", "").strip()
            phone = request.form.get("phone", "").strip()

            # Validación sencilla
            if not name:
                errors.append("El nombre del proveedor es obligatorio.")
            if contact_email and "@" not in contact_email:
                errors.append("El email de contacto no es válido.")

            if not errors:
                supplier.name = name
                supplier.contact_email = contact_email or None
                supplier.phone = phone or None

                db.session.commit()
                flash("Proveedor actualizado correctamente.", "success")
                return redirect(url_for("list_suppliers"))

        return render_template("supplier_form.html", errors=errors, supplier=supplier)

    @app.route("/suppliers/<int:supplier_id>/delete", methods=["POST"])
    def delete_supplier(supplier_id):
        supplier = Supplier.query.get_or_404(supplier_id)
        # No permitir borrar si tiene productos
        if supplier.products:
            flash("No se puede eliminar un proveedor con productos asociados.", "danger")
            return redirect(url_for("list_suppliers"))
    
        db.session.delete(supplier)
        db.session.commit()
        flash("Proveedor eliminado.", "success")
        return redirect(url_for("list_suppliers"))
    # (aquí luego añadiremos las rutas de productos y reporte)

    # ---------- PRODUCTS ----------
    @app.route("/products")
    def list_products():
        supplier_id = request.args.get("supplier_id", type=int)

        suppliers = Supplier.query.order_by(Supplier.name).all()
        query = Product.query.order_by(Product.name)

        if supplier_id:
            query = query.filter(Product.supplier_id == supplier_id)

        products = query.all()
        return render_template(
            "products_list.html",
            products=products,
            suppliers=suppliers,
            selected_supplier_id=supplier_id,
        )
    
    @app.route("/products/new", methods=["GET", "POST"])
    def create_product():
        errors = []
        suppliers = Supplier.query.order_by(Supplier.name).all()

        if not suppliers:
            flash("Debe crear al menos un proveedor antes de crear productos.", "warning")
            return redirect(url_for("list_suppliers"))

        if request.method == "POST":
            supplier_id = request.form.get("supplier_id", type=int)
            name = request.form.get("name", "").strip()
            sku = request.form.get("sku", "").strip()
            stock_raw = request.form.get("stock", "0").strip()
            unit_price_raw = request.form.get("unit_price", "0").strip()

            if not supplier_id:
                errors.append("Debe seleccionar un proveedor.")

            if not name:
                errors.append("El nombre del producto es obligatorio.")

            if not sku:
                errors.append("El SKU es obligatorio.")

            if sku:
                existing = Product.query.filter_by(sku=sku).first()
                if existing:
                    errors.append("Ya existe un producto con ese SKU.")

            try:
                stock = int(stock_raw)
                if stock < 0:
                    errors.append("El stock no puede ser negativo.")
            except ValueError:
                errors.append("El stock debe ser un número entero.")

            try:
                unit_price = float(unit_price_raw)
                if unit_price < 0:
                    errors.append("El precio unitario no puede ser negativo.")
            except ValueError:
                errors.append("El precio unitario debe ser un número válido.")

            if not errors:
                product = Product(
                    supplier_id=supplier_id,
                    name=name,
                    sku=sku,
                    stock=stock,
                    unit_price=unit_price,
                )

                db.session.add(product)
                db.session.commit()
                flash("Producto creado exitosamente.", "success")
                return redirect(url_for("list_products"))

        return render_template(
            "product_form.html",
            errors=errors,
            product=None,
            suppliers=suppliers,
        )

    @app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        suppliers = Supplier.query.order_by(Supplier.name).all()
        errors = []

        if request.method == "POST":
            supplier_id = request.form.get("supplier_id", type=int)
            name = request.form.get("name", "").strip()
            sku = request.form.get("sku", "").strip()
            stock_raw = request.form.get("stock", "0").strip()
            unit_price_raw = request.form.get("unit_price", "0").strip()

            if not supplier_id:
                errors.append("Debe seleccionar un proveedor.")

            if not name:
                errors.append("El nombre del producto es obligatorio.")

            if not sku:
                errors.append("El SKU es obligatorio.")

            if sku:
                existing = Product.query.filter(
                    Product.sku == sku,
                    Product.id != product.id
                ).first()

                if existing:
                    errors.append("Ya existe otro producto con ese SKU.")

            try:
                stock = int(stock_raw)
                if stock < 0:
                    errors.append("El stock no puede ser negativo.")
            except ValueError:
                errors.append("El stock debe ser un número entero.")
            try:
                unit_price = float(unit_price_raw)
                if unit_price < 0:
                    errors.append("El precio unitario no puede ser negativo.")
            except ValueError:
                errors.append("El precio unitario debe ser un número válido.")
            if not errors:
                product.supplier_id = supplier_id
                product.name = name
                product.sku = sku
                product.stock = stock
                product.unit_price = unit_price

                db.session.commit()
                flash("Producto actualizado correctamente.", "success")
                return redirect(url_for("list_products"))

        return render_template(
            "product_form.html",
            errors=errors,
            product=product,
            suppliers=suppliers,
        )

    @app.route("/products/<int:product_id>/delete", methods=["POST"])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash("Producto eliminado.", "success")
        return redirect(url_for("list_products"))

    # ---------- LOW STOCK REPORT ----------
    @app.route("/reports/low-stock")
    def low_stock_report():
        threshold = request.args.get("threshold", default=5, type=int)
        products = Product.query.filter(Product.stock < threshold).order_by(Product.stock).all()
        return render_template(
            "low_stock_report.html",
            products=products,
            threshold=threshold,
        )
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)