import secrets
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for, send_from_directory

from backend.config import Config
from backend.models import db, Product, Order, OrderItem


app = Flask(__name__, template_folder="templates", static_folder="../frontend/assets")
app.config.from_object(Config)
db.init_app(app)


SEED_PRODUCTS = [
    {
        "slug": "mente-en-calma", "name": "Mente en calma", "description": "Herramientas amables para entender tu TDAH, bajar el ruido y recuperar foco.",
        "category": "VIDA & BIENESTAR", "price_ars": 8900, "cover_class": "coral", "accent": "#C9756B", "featured": True,
    },
    {
        "slug": "casa-en-flujo", "name": "Casa en flujo", "description": "Un sistema realista para ordenar tu hogar sin convertirlo en otro trabajo de tiempo completo.",
        "category": "VIDA & BIENESTAR", "price_ars": 7900, "cover_class": "teal", "accent": "#3A5F5F", "featured": True,
    },
    {
        "slug": "semana-liviana", "name": "Semana liviana", "description": "Planifica tus días con menos listas imposibles y más espacio para lo importante.",
        "category": "TRABAJO & CARRERA", "price_ars": 6900, "cover_class": "sun", "accent": "#D98B7E", "featured": True,
    },
    {
        "slug": "rutinas-sin-culpa", "name": "Rutinas sin culpa", "description": "Pequeños rituales que se adaptan a tu energía, tus tiempos y tu vida verdadera.",
        "category": "APRENDER & DOMINAR", "price_ars": 6500, "cover_class": "lavender", "accent": "#7E8E8E", "featured": False,
    },
]

REAL_DESCRIPTION = """Primero tu mente, después tu hogar es una guía práctica de organización y gestión doméstica diseñada específicamente para personas con TDAH, autismo o AuDHD.

A diferencia de los métodos convencionales basados en la disciplina rígida y la fuerza de voluntad, este libro propone un cambio de paradigma: no esforzarte más, sino hacer que tu casa te pida menos. A través de sistemas de bajo esfuerzo, reducción de pasos y rutinas dinámicas divididas por niveles de energía (Rojo, Amarillo y Verde), aprenderás a desarmar la parálisis ejecutiva, eliminar la culpa por el desorden y mantener tu casa funcional y habitable, incluso en los días de menor capacidad."""

CONVIVIR_SHORT_DESCRIPTION = "Un método paso a paso para dejar de improvisar frente a cada conflicto diario, entender qué hay detrás de las conductas difíciles y construir una convivencia previsible con niños y adolescentes con TDAH o autismo."

CONVIVIR_DESCRIPTION = """Convivir sin apagar incendios es un mapa de ruta práctico y estructurado para padres, familiares y cuidadores que conviven a diario con niños y adolescentes con TDAH o autismo.

Cuando la rutina se convierte en una seguidilla de discusiones, negativas reiteradas, dificultades con las pantallas y crisis que parecen surgir de la nada, el agotamiento no proviene de las tareas cotidianas, sino de estar apagando fuegos todo el día. Este libro ofrece un enfoque claro para dejar atrás la improvisación: aprender a mirar qué ocurre antes de la conducta, anticipar los momentos de fricción, poner límites firmes sin necesidad de gritar y construir una convivencia previsible y calmada donde toda la familia comparta las mismas reglas."""

REAL_PRODUCTS = [
    {
        "slug": "primero-tu-mente-despues-tu-hogar",
        "name": "Primero tu mente, después tu hogar",
        "description": REAL_DESCRIPTION,
        "short_description": "Sistema de bajo esfuerzo para adultos con TDAH, Autismo o AuDHD.",
        "category": "VIDA & BIENESTAR",
        "price_ars": 6999,
        "cover_class": "teal",
        "accent": "#3A5F5F",
        "featured": True,
        "file_name": "primero-tu-mente-despues-tu-hogar.pdf",
        "cover_image": "primero-tu-mente-despues-tu-hogar.jpg",
    },
    {
        "slug": "kit-primero-tu-mente-despues-tu-hogar",
        "name": "KIT: Primero tu mente, después tu hogar",
        "description": REAL_DESCRIPTION + "\n\nIncluye el ebook principal y los tres bonus: Modo Supervivencia, Mi Casa Funciona Así y Tarjetas Antibloqueo.",
        "category": "VIDA & BIENESTAR",
        "price_ars": 7999,
        "cover_class": "coral",
        "accent": "#C9756B",
        "featured": True,
        "file_name": "kit-primero-tu-mente-despues-tu-hogar.zip",
        "cover_image": "primero-tu-mente-despues-tu-hogar.jpg",
    },
    {
        "slug": "convivir-sin-apagar-incendios",
        "name": "Convivir sin apagar incendios",
        "description": CONVIVIR_DESCRIPTION,
        "short_description": CONVIVIR_SHORT_DESCRIPTION,
        "category": "VIDA & BIENESTAR",
        "price_ars": 6999,
        "cover_class": "teal",
        "accent": "#3A5F5F",
        "featured": True,
        "file_name": "convivir-sin-apagar-incendios.pdf",
        "cover_image": "convivir-sin-apagar-incendios.jpg",
    },
    {
        "slug": "kit-convivir-sin-apagar-incendios",
        "name": "KIT: Convivir sin apagar incendios",
        "description": CONVIVIR_DESCRIPTION + "\n\nIncluye el ebook oficial y todos los bonus del KIT.",
        "short_description": "El ebook completo con todos los bonus para construir una convivencia más previsible y calmada.",
        "category": "VIDA & BIENESTAR",
        "price_ars": 7999,
        "cover_class": "coral",
        "accent": "#C9756B",
        "featured": True,
        "file_name": "kit-convivir-sin-apagar-incendios.pdf",
        "cover_image": "convivir-sin-apagar-incendios.jpg",
    },
]
KIT_SLUGS = {
    "kit-primero-tu-mente-despues-tu-hogar",
    "kit-convivir-sin-apagar-incendios",
}

CATEGORIES = [
    "VIDA & BIENESTAR",
    "APRENDER & DOMINAR",
    "DINERO INTELIGENTE",
    "TRABAJO & CARRERA",
    "CREATIVIDAD & PASIONES",
]


def seed_products():
    if Product.query.count() == 0:
        for data in SEED_PRODUCTS:
            db.session.add(Product(**data))
        db.session.commit()
    else:
        legacy_categories = {
            "TDAH": "VIDA & BIENESTAR",
            "Hogar": "VIDA & BIENESTAR",
            "Productividad": "TRABAJO & CARRERA",
        }
        changed = False
        for product in Product.query.all():
            if product.category in legacy_categories:
                product.category = legacy_categories[product.category]
                changed = True
        if changed:
            db.session.commit()

    demo_slugs = ["mente-en-calma", "casa-en-flujo", "semana-liviana", "rutinas-sin-culpa"]
    Product.query.filter(Product.slug.in_(demo_slugs)).delete(synchronize_session=False)

    for data in REAL_PRODUCTS:
        product = Product.query.filter_by(slug=data["slug"]).first()
        if product is None:
            db.session.add(Product(**data))
        else:
            for key, value in data.items():
                setattr(product, key, value)
    db.session.commit()


def migrate_product_columns():
    columns = {row[1] for row in db.session.execute(db.text("PRAGMA table_info(product)"))}
    if "short_description" not in columns:
        db.session.execute(db.text("ALTER TABLE product ADD COLUMN short_description VARCHAR(280)"))
        db.session.commit()
    if "cover_image" not in columns:
        db.session.execute(db.text("ALTER TABLE product ADD COLUMN cover_image VARCHAR(255)"))
        db.session.commit()


def cart_products():
    ids = session.get("cart", [])
    if not ids:
        return []
    products = Product.query.filter(Product.id.in_(ids)).all()
    product_map = {product.id: product for product in products}
    return [product_map[item_id] for item_id in ids if item_id in product_map]


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_globals():
    def converted_price(price_ars, rate):
        return f"{price_ars / rate:,.2f}"

    return {
        "cart_count": len(session.get("cart", [])),
        "current_year": datetime.now().year,
        "price_usd": lambda price: converted_price(price, app.config["ARS_PER_USD"]),
        "price_eur": lambda price: converted_price(price, app.config["ARS_PER_EUR"]),
    }


@app.route("/")
def home():
    featured = Product.query.filter(Product.featured.is_(True), ~Product.slug.in_(KIT_SLUGS)).all()
    products = Product.query.filter(~Product.slug.in_(KIT_SLUGS)).order_by(Product.created_at.desc()).all()
    return render_template("home.html", featured=featured, products=products)


@app.route("/shop")
def shop():
    category = request.args.get("category", "Todas")
    base_query = Product.query.filter(~Product.slug.in_(KIT_SLUGS))
    products = base_query.filter_by(category=category).all() if category != "Todas" else base_query.all()
    categories = CATEGORIES
    return render_template("shop.html", products=products, categories=categories, selected_category=category)


@app.route("/product/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    kit_slug = f"kit-{slug}" if not slug.startswith("kit-") else None
    kit = Product.query.filter_by(slug=kit_slug).first() if kit_slug else None
    return render_template("product.html", product=product, kit=kit)


@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    Product.query.get_or_404(product_id)
    cart = session.setdefault("cart", [])
    if product_id not in cart:
        cart.append(product_id)
        session.modified = True
        flash("Ebook agregado a tu carrito.", "success")
    return redirect(request.form.get("next") or request.referrer or url_for("shop"))


@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    if product_id in cart:
        cart.remove(product_id)
        session.modified = True
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    products = cart_products()
    return render_template("cart.html", products=products, total=sum(item.price_ars for item in products))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    products = cart_products()
    if not products:
        return redirect(url_for("shop"))
    total = sum(item.price_ars for item in products)
    if request.method == "POST":
        buyer_name = request.form.get("buyer_name", "").strip()
        buyer_email = request.form.get("buyer_email", "").strip().lower()
        payment_method = request.form.get("payment_method", "mercadopago")
        if not buyer_name or "@" not in buyer_email:
            flash("Completá tu nombre y un email válido.", "error")
            return render_template("checkout.html", products=products, total=total)
        order = Order(
            buyer_name=buyer_name, buyer_email=buyer_email, total_ars=total,
            payment_method=payment_method, status="paid_demo",
            download_token=secrets.token_urlsafe(32),
        )
        db.session.add(order)
        db.session.flush()
        for product in products:
            db.session.add(OrderItem(order_id=order.id, product_id=product.id, product_name=product.name, unit_price_ars=product.price_ars))
        db.session.commit()
        session["cart"] = []
        return redirect(url_for("success", order_id=order.id))
    return render_template("checkout.html", products=products, total=total)


@app.route("/success/<int:order_id>")
def success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status not in {"paid_demo", "paid"}:
        abort(403)
    return render_template("success.html", order=order)


@app.route("/download/<token>")
def download(token):
    order = Order.query.filter_by(download_token=token).first_or_404()
    if order.status not in {"paid_demo", "paid"}:
        abort(403, description="Esta descarga no está disponible para esta orden.")
    product = Product.query.filter_by(id=order.items[0].product_id).first_or_404()
    downloads_dir = Path(app.root_path).parent / "storage" / "ebooks"
    if product.file_name and (downloads_dir / product.file_name).exists():
        return send_from_directory(downloads_dir, product.file_name, as_attachment=True)
    return render_template("download_placeholder.html", product=product, order=order)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("email") == app.config["ADMIN_EMAIL"] and request.form.get("password") == app.config["ADMIN_PASSWORD"]:
            session["is_admin"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash("Credenciales incorrectas.", "error")
    return render_template("admin/login.html")


@app.get("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("home"))


@app.get("/admin")
@admin_required
def admin_dashboard():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    revenue = sum(order.total_ars for order in orders if order.status in {"paid", "paid_demo"})
    return render_template("admin/dashboard.html", orders=orders, revenue=revenue, products=Product.query.all(), categories=CATEGORIES)


@app.post("/admin/products")
@admin_required
def admin_create_product():
    product = Product(
        slug=request.form["slug"].strip(), name=request.form["name"].strip(), description=request.form["description"].strip(),
        category=request.form["category"].strip(), price_ars=int(request.form["price_ars"]), cover_class=request.form.get("cover_class", "coral"),
        accent=request.form.get("accent", "#C9756B"), featured=request.form.get("featured") == "on",
    )
    db.session.add(product)
    db.session.commit()
    flash("Producto creado.", "success")
    return redirect(url_for("admin_dashboard"))


with app.app_context():
    db.create_all()
    migrate_product_columns()
    seed_products()


if __name__ == "__main__":
    app.run(debug=True)
