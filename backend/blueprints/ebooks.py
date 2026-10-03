"""
Blueprint para la marca: Ebooks para la vida
Rutas: /ebooks/*
"""
from flask import Blueprint, render_template, session
from backend.models import Product

ebooks_bp = Blueprint(
    'ebooks',
    __name__,
    url_prefix='/ebooks'
)


@ebooks_bp.before_request
def set_brand():
    """Establecer marca en sesión antes de cada request."""
    session['current_brand'] = 'ebooks'


@ebooks_bp.route('/')
def catalog():
    """Catálogo de Ebooks para la vida."""
    from sqlalchemy import func
    products = Product.query.filter(
        Product.universe == 'ebooks'
    ).order_by(
        func.coalesce(Product.sort_order, 999999).asc(),
        Product.id.asc()
    ).all()
    return render_template('ebooks/catalog.html', brand='ebooks', products=products)


@ebooks_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto Ebooks."""
    return render_template('ebooks/product.html', brand='ebooks', product_id=product_id)
