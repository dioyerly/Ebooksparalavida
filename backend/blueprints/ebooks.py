"""
Blueprint para la marca: Ebooks para la vida
Rutas: /ebooks/*
"""
from flask import Blueprint, render_template, session

ebooks_bp = Blueprint(
    'ebooks',
    __name__,
    url_prefix='/ebooks',
    template_folder='../templates/ebooks'
)


@ebooks_bp.before_request
def set_brand():
    """Establecer marca en sesión antes de cada request."""
    session['current_brand'] = 'ebooks'


@ebooks_bp.route('/')
def catalog():
    """Catálogo de Ebooks para la vida."""
    return render_template('catalog.html', brand='ebooks')


@ebooks_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto Ebooks."""
    return render_template('product.html', brand='ebooks', product_id=product_id)
