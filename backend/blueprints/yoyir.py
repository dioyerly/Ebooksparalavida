"""
Blueprint para la marca: YOYI'R
Rutas: /yoyir/*
"""
from flask import Blueprint, render_template, session
from backend.models import Product

yoyir_bp = Blueprint(
    'yoyir',
    __name__,
    url_prefix='/yoyir'
)


@yoyir_bp.before_request
def set_brand():
    """Establecer marca en sesión antes de cada request."""
    session['current_brand'] = 'yoyir'


@yoyir_bp.route('/')
def catalog():
    """Catálogo de YOYI'R (Agendas y Planners)."""
    from sqlalchemy import func
    products = Product.query.filter(
        Product.universe == 'yoyir'
    ).order_by(
        func.coalesce(Product.sort_order, 999999).asc(),
        Product.id.asc()
    ).all()

    return render_template('yoyir/catalog.html', brand='yoyir', products=products)


@yoyir_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto YOYI'R."""
    return render_template('yoyir/product.html', brand='yoyir', product_id=product_id)
