from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(280))
    category = db.Column(db.String(80), nullable=False)
    price_ars = db.Column(db.Integer, nullable=False)
    cover_class = db.Column(db.String(40), nullable=False, default="coral")
    accent = db.Column(db.String(20), nullable=False, default="#C9756B")
    featured = db.Column(db.Boolean, default=False)
    file_name = db.Column(db.String(255))
    cover_image = db.Column(db.String(255))
    cover_image_blob = db.Column(db.LargeBinary)
    product_type = db.Column(db.String(30), nullable=False, default="pdf")
    source_html_path = db.Column(db.String(255))
    ebook_file = db.Column(db.LargeBinary)
    file_name_epub = db.Column(db.String(255))
    ebook_file_epub = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    is_kit = db.Column(db.Boolean, default=False)
    kit_price_ars = db.Column(db.Integer)
    kit_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bonus_files = db.relationship(
        "ProductBonusFile", backref="product", lazy=True,
        cascade="all, delete-orphan", order_by="ProductBonusFile.id"
    )


class ProductBonusFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    name = db.Column(db.String(160), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(100), nullable=False)
    file_blob = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(120), nullable=False)
    buyer_email = db.Column(db.String(255), nullable=False)
    total_ars = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), default="pending")
    download_token = db.Column(db.String(120), unique=True)
    access_code = db.Column(db.String(8), unique=True)
    ebook_type = db.Column(db.String(30), nullable=False, default="pdf")
    personalized_file_path = db.Column(db.String(255))
    personalized_html_blob = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name = db.Column(db.String(160), nullable=False)
    unit_price_ars = db.Column(db.Integer, nullable=False)


class ProductClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name = db.Column(db.String(160), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_session_id = db.Column(db.String(120))
    referrer = db.Column(db.String(255))


class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_path = db.Column(db.String(255), nullable=False)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_session_id = db.Column(db.String(120))
    user_agent = db.Column(db.String(500))
    referrer = db.Column(db.String(255))


class DeviceSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    fingerprint = db.Column(db.String(255), nullable=False)
    user_agent = db.Column(db.String(500))
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
