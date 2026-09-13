"""
Ebooksparalavida - Flask application for selling digital ebooks.
Handles product catalog, shopping cart, checkout, and payments.
"""
import secrets
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
    send_from_directory
)
from werkzeug.utils import secure_filename

from backend.config import Config
from backend.models import db, Product, Order, OrderItem, ProductClick, PageVisit
from backend.services import MercadoPagoService, PayPalService, EmailService


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

        # Crear orden
        order = Order(
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            total_ars=total,
            payment_method=payment_method,
            status="pending",
            download_token=secrets.token_urlsafe(32),
        )
        db.session.add(order)
        db.session.flush()

        for product in products:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                unit_price_ars=product.price_ars,
            ))
        db.session.commit()

        # Preparar items para pago
        items = [{"id": p.id, "name": p.name, "price_ars": p.price_ars} for p in products]

        # Crear preferencia de pago según método
        if payment_method == "mercadopago":
            mp_service = MercadoPagoService(app.config["MP_ACCESS_TOKEN"])
            payment_result = mp_service.create_preference(order.id, buyer_name, buyer_email, total, items)
        else:  # paypal
            pp_service = PayPalService(app.config["PAYPAL_CLIENT_ID"], app.config["PAYPAL_CLIENT_SECRET"])
            payment_result = pp_service.create_order(order.id, buyer_email, total, items)

        # En demo o si hay error, marcar como pagado y ir a success
        if payment_result.get("is_demo") or not payment_result.get("success"):
            order.status = "paid_demo"
            db.session.commit()
            session["cart"] = []

            # Enviar email de descarga (demo)
            email_service = EmailService(app.config["SENDGRID_API_KEY"])
            email_service.send_download_link(buyer_email, [p.name for p in products], order.download_token)

            return redirect(url_for("success", order_id=order.id))

        # Si es pago real, redirigir a plataforma de pago
        session["cart"] = []
        return redirect(payment_result.get("checkout_url"))

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
    slug = request.form["slug"].strip()
    name = request.form["name"].strip()

    # Guardar archivo PDF
    pdf_file = request.files.get("ebook_file")
    file_name = None
    if pdf_file and pdf_file.filename.endswith(".pdf"):
        ebooks_dir = Path(__file__).parent.parent / "storage" / "ebooks"
        ebooks_dir.mkdir(parents=True, exist_ok=True)
        filename = secure_filename(f"{slug}.pdf")
        pdf_file.save(str(ebooks_dir / filename))
        file_name = filename

    # Guardar imagen de portada
    cover_file = request.files.get("cover_image")
    cover_image = None
    if cover_file and cover_file.filename:
        images_dir = Path(__file__).parent.parent / "frontend" / "assets" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(cover_file.filename).suffix
        filename = secure_filename(f"{slug}{ext}")
        cover_file.save(str(images_dir / filename))
        cover_image = filename

    product = Product(
        slug=slug,
        name=name,
        description=request.form["description"].strip(),
        category=request.form["category"].strip(),
        price_ars=int(request.form["price_ars"]),
        cover_class=request.form.get("cover_class", "coral"),
        accent=request.form.get("accent", "#C9756B"),
        featured=request.form.get("featured") == "on",
        file_name=file_name,
        cover_image=cover_image,
    )
    db.session.add(product)
    db.session.commit()
    flash(f"✅ Producto '{name}' creado exitosamente.", "success")
    return redirect(url_for("admin_dashboard"))


@app.post("/api/track-click")
def track_product_click():
    data = request.get_json() or {}
    product_id = data.get("product_id")
    product_name = data.get("product_name", "Unknown")

    if product_id:
        session_id = session.get("session_id") or secrets.token_hex(16)
        session["session_id"] = session_id

        click = ProductClick(
            product_id=product_id,
            product_name=product_name,
            user_session_id=session_id,
            referrer=request.referrer
        )
        db.session.add(click)
        db.session.commit()

    return {"status": "ok"}


@app.post("/api/track-visit")
def track_page_visit():
    data = request.get_json() or {}
    page_path = data.get("page_path", request.path)

    session_id = session.get("session_id") or secrets.token_hex(16)
    session["session_id"] = session_id

    visit = PageVisit(
        page_path=page_path,
        user_session_id=session_id,
        user_agent=request.headers.get("User-Agent", "Unknown"),
        referrer=request.referrer
    )
    db.session.add(visit)
    db.session.commit()

    return {"status": "ok"}


@app.get("/api/admin/stats")
@admin_required
def get_admin_stats():
    from datetime import datetime, timedelta

    # Órdenes y ingresos
    all_orders = Order.query.all()
    paid_orders = [o for o in all_orders if o.status in {"paid", "paid_demo"}]
    total_revenue = sum(o.total_ars for o in paid_orders)

    # Clientes únicos
    unique_customers = len(set(o.buyer_email for o in paid_orders))

    # Últimos 30 días
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_orders = [o for o in paid_orders if o.created_at >= thirty_days_ago]
    recent_revenue = sum(o.total_ars for o in recent_orders)

    # Productos más vendidos
    product_sales = {}
    for order in paid_orders:
        for item in order.items:
            product_sales[item.product_name] = product_sales.get(item.product_name, 0) + 1

    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]

    # Productos más clicleados
    clicks = ProductClick.query.all()
    product_clicks = {}
    for click in clicks:
        key = click.product_name
        product_clicks[key] = product_clicks.get(key, 0) + 1

    top_clicked = sorted(product_clicks.items(), key=lambda x: x[1], reverse=True)[:5]

    # Visitas últimos 30 días
    recent_visits = PageVisit.query.filter(PageVisit.visited_at >= thirty_days_ago).all()
    total_visits = len(recent_visits)
    unique_visits = len(set(v.user_session_id for v in recent_visits))

    # Ingresos por día (últimos 30)
    revenue_by_day = {}
    for order in recent_orders:
        day = order.created_at.strftime("%Y-%m-%d")
        revenue_by_day[day] = revenue_by_day.get(day, 0) + order.total_ars

    revenue_by_day = sorted(revenue_by_day.items())

    return {
        "total_orders": len(paid_orders),
        "total_revenue": total_revenue,
        "total_customers": unique_customers,
        "recent_orders": len(recent_orders),
        "recent_revenue": recent_revenue,
        "total_products": len(Product.query.all()),
        "total_clicks": len(clicks),
        "total_visits": total_visits,
        "unique_visits": unique_visits,
        "top_products": [{"name": name, "count": count} for name, count in top_products],
        "top_clicked": [{"name": name, "count": count} for name, count in top_clicked],
        "revenue_by_day": [{"date": date, "revenue": revenue} for date, revenue in revenue_by_day],
    }


@app.get("/api/admin/orders")
@admin_required
def get_admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return {
        "orders": [
            {
                "id": o.id,
                "buyer_name": o.buyer_name,
                "buyer_email": o.buyer_email,
                "total_ars": o.total_ars,
                "status": o.status,
                "payment_method": o.payment_method,
                "created_at": o.created_at.isoformat(),
                "items": [{"product_name": item.product_name, "unit_price_ars": item.unit_price_ars} for item in o.items]
            }
            for o in orders
        ]
    }


@app.get("/api/admin/products-analytics")
@admin_required
def get_products_analytics():
    products = Product.query.all()
    clicks = ProductClick.query.all()

    product_data = {}
    for product in products:
        product_data[product.id] = {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "category": product.category,
            "price_ars": product.price_ars,
            "clicks": 0,
            "sales": 0
        }

    # Contar clics por producto
    for click in clicks:
        if click.product_id in product_data:
            product_data[click.product_id]["clicks"] += 1

    # Contar ventas por producto
    items = OrderItem.query.all()
    for item in items:
        if item.product_id in product_data:
            product_data[item.product_id]["sales"] += 1

    return {"products": sorted(product_data.values(), key=lambda x: x["clicks"], reverse=True)}


with app.app_context():
    db.create_all()
    migrate_product_columns()
    seed_products()


if __name__ == "__main__":
    app.run(debug=True)
