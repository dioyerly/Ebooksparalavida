"""
Blueprint para la marca: EstrategIA
Rutas: /estrategia/*
"""
from flask import Blueprint, render_template

estrategia_bp = Blueprint(
    'estrategia',
    __name__,
    url_prefix='/estrategia',
    template_folder='../templates/estrategia'
)


@estrategia_bp.route('/')
def catalog():
    """Catálogo de EstrategIA (Herramientas e Interactivos)."""
    return render_template('catalog.html', brand='estrategia')


@estrategia_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Detalle de producto EstrategIA."""
    return render_template('product.html', brand='estrategia', product_id=product_id)
