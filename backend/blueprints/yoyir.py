"""
Blueprint para la marca: YOYI'R
Rutas: /yoyir/*
"""
from flask import Blueprint, render_template, session

yoyir_bp = Blueprint(
    'yoyir',
    __name__,
    url_prefix='/yoyir',
    template_folder='../templates/yoyir'
)


@yoyir_bp.before_request
def set_brand():
    """Establecer marca en sesión antes de cada request."""
    session['current_brand'] = 'yoyir'


@yoyir_bp.route('/')
def catalog():
    """Catálogo de YOYI'R (Agendas y Planners)."""
    return render_template('catalog.html', brand='yoyir')


@yoyir_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto YOYI'R."""
    return render_template('product.html', brand='yoyir', product_id=product_id)
