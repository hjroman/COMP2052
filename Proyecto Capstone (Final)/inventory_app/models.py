# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Supplier(db.Model):
    __tablename__ = "suppliers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact_email = db.Column(db.String(120))
    phone = db.Column(db.String(50))

    # Un proveedor tiene muchos productos
    products = db.relationship("Product", backref="supplier", lazy=True)
    def __repr__(self):
        return f"<Supplier {self.id} - {self.name}>"
    
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(80), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<Product {self.id} - {self.name} ({self.sku})>"