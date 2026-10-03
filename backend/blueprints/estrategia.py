"""
Blueprint para la marca: EstrategIA
Rutas: /estrategia/*
"""
from flask import Blueprint, render_template, session
from backend.models import Product

estrategia_bp = Blueprint(
    'estrategia',
    __name__,
    url_prefix='/estrategia'
)


@estrategia_bp.before_request
def set_brand():
    """Establecer marca en sesión antes de cada request."""
    session['current_brand'] = 'estrategia'


@estrategia_bp.route('/')
def catalog():
    """Catálogo de EstrategIA (Herramientas e Interactivos)."""
    from sqlalchemy import func
    products = Product.query.filter(
        Product.universe == 'estrategia'
    ).order_by(
        func.coalesce(Product.sort_order, 999999).asc(),
        Product.id.asc()
    ).all()

    return render_template('estrategia/catalog.html', brand='estrategia', products=products)


@estrategia_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto EstrategIA."""
    return render_template('estrategia/product.html', brand='estrategia', product_id=product_id)
