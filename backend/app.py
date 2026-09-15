"""
Ebooksparalavida - Flask application for selling digital ebooks.
Handles product catalog, shopping cart, checkout, and payments.
"""
import secrets
import datetime
import re
from functools import wraps
from pathlib import Path

from flask import (
    Flask, abort, flash, redirect, render_template, request, session,
    url_for, send_from_directory
)
from werkzeug.utils import secure_filename

from backend.config import Config
from backend.models import (
    db, Product, Order, OrderItem, ProductClick, PageVisit
)
from backend.services import (
    MercadoPagoService, PayPalService, EmailService,
    generate_access_code, generate_personalized_html,
)


app = Flask(__name__, template_folder="templates",
            static_folder="../frontend/assets")
app.config.from_object(Config)
db.init_app(app)


SEED_PRODUCTS = [
    {
        "slug": "mente-en-calma",
        "name": "Mente en calma",
        "description": (
            "Herramientas amables para entender tu TDAH, bajar el ruido y "
            "recuperar foco."
        ),
        "category": "VIDA & BIENESTAR",
        "price_ars": 8900,
        "cover_class": "coral",
        "accent": "#C9756B",
        "featured": True,
    },
    {
        "slug": "casa-en-flujo",
        "name": "Casa en flujo",
        "description": (
            "Un sistema realista para ordenar tu hogar sin convertirlo en "
            "otro trabajo de tiempo completo."
        ),
        "category": "VIDA & BIENESTAR",
        "price_ars": 7900,
        "cover_class": "teal",
        "accent": "#3A5F5F",
        "featured": True,

    },
    {
        "slug": "semana-liviana",
        "name": "Semana liviana",
        "description": (
            "Planifica tus días con menos listas imposibles y más espacio "
            "para lo importante."
        ),
        "category": "TRABAJO & CARRERA",
        "price_ars": 6900,
        "cover_class": "sun",
        "accent": "#D98B7E",
        "featured": True,
    },
    {
        "slug": "rutinas-sin-culpa",
        "name": "Rutinas sin culpa",
        "description": (
            "Pequeños rituales que se adaptan a tu energía, tus tiempos y "
            "tu vida verdadera."
        ),
        "category": "APRENDER & DOMINAR",
        "price_ars": 6500,
        "cover_class": "lavender",
        "accent": "#7E8E8E",
        "featured": False,
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
        "description": (
            REAL_DESCRIPTION + "\n\nIncluye el ebook principal y los "
            "tres bonus: Modo Supervivencia, Mi Casa Funciona Así y "
            "Tarjetas Antibloqueo."
        ),
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
        "description": (
            CONVIVIR_DESCRIPTION + "\n\nIncluye el ebook oficial y "
            "todos los bonus del KIT."
        ),
        "short_description": (
            "El ebook completo con todos los bonus para construir una "
            "convivencia más previsible y calmada."
        ),
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
    """Seed Products."""
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

    demo_slugs = ["mente-en-calma", "casa-en-flujo",
                  "semana-liviana", "rutinas-sin-culpa"]
    Product.query.filter(Product.slug.in_(demo_slugs)
                         ).delete(synchronize_session=False)

    for data in REAL_PRODUCTS:
        product = Product.query.filter_by(slug=data["slug"]).first()
        if product is None:
            db.session.add(Product(**data))
        else:
            for key, value in data.items():
                setattr(product, key, value)
    romance = Product.query.filter_by(slug="Descubre tu identidad como lectora").first()
    if romance:
        romance.product_type = "html_interactive"
        romance.source_html_path = "interactive_ebooks/the-romance-reader-kit.html"
        romance.file_name = "the-romance-reader-kit.html"
    db.session.commit()


def migrate_product_columns():
    """Migrate Product Columns."""
    query = db.text("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'product' AND TABLE_SCHEMA = DATABASE()
    """)
    columns = {row[0] for row in db.session.execute(query)}
    if "short_description" not in columns:
        db.session.execute(
            db.text("ALTER TABLE product ADD COLUMN short_description VARCHAR(280)"))
        db.session.commit()
    if "cover_image" not in columns:
        db.session.execute(
            db.text("ALTER TABLE product ADD COLUMN cover_image VARCHAR(255)"))
        db.session.commit()
    for column, definition in {
        "product_type": "VARCHAR(30) NOT NULL DEFAULT 'pdf'",
        "source_html_path": "VARCHAR(255)",
        "is_kit": "BOOLEAN DEFAULT FALSE",
        "kit_bonus_ids": "VARCHAR(255)",
        "kit_price_ars": "INT",
        "kit_description": "TEXT",
    }.items():
        if column not in columns:
            db.session.execute(db.text(
                f"ALTER TABLE product ADD COLUMN {column} {definition}"
            ))
            db.session.commit()
    order_table = Order.__tablename__
    query = db.text(f"""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{order_table}' AND TABLE_SCHEMA = DATABASE()
    """)
    order_columns = {row[0] for row in db.session.execute(query)}
    for column, definition in {
        "access_code": "VARCHAR(8)",
        "ebook_type": "VARCHAR(30) NOT NULL DEFAULT 'pdf'",
        "personalized_file_path": "VARCHAR(255)",
    }.items():
        if column not in order_columns:
            db.session.execute(db.text(
                f"ALTER TABLE {order_table} ADD COLUMN {column} {definition}"
            ))
            db.session.commit()


def is_valid_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def cart_products():
    """Cart Products."""
    ids = session.get("cart", [])
    if not ids:
        return []
    products = Product.query.filter(Product.id.in_(ids)).all()
    product_map = {product.id: product for product in products}
    return [product_map[item_id] for item_id in ids if item_id in product_map]


def admin_required(view):
    """Admin Required."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        """Wrapped."""
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_globals():
    """Inject Globals."""
    def converted_price(price_ars, rate):
        """Converted Price."""
        return f"{price_ars / rate:,.2f}"

    return {
        "cart_count": len(session.get("cart", [])),
        "current_year": datetime.datetime.now().year,
        "price_usd": lambda price: converted_price(price, app.config["ARS_PER_USD"]),
        "price_eur": lambda price: converted_price(price, app.config["ARS_PER_EUR"]),
    }


@app.route("/")
def home():
    """Render home page with featured and recent products."""
    featured = Product.query.filter(Product.featured.is_(
        True), ~Product.slug.in_(KIT_SLUGS)).all()
    products = Product.query.filter(~Product.slug.in_(
        KIT_SLUGS)).order_by(Product.created_at.desc()).all()
    return render_template("home.html", featured=featured, products=products)


@app.route("/shop")
def shop():
    """Render shop page with filterable products."""
    category = request.args.get("category", "Todas")
    base_query = Product.query.filter(~Product.slug.in_(KIT_SLUGS))
    products = base_query.filter_by(category=category).all(
    ) if category != "Todas" else base_query.all()
    categories = CATEGORIES
    return render_template("shop.html", products=products, categories=categories, selected_category=category)


@app.route("/product/<slug>")
def product_detail(slug):
    """Product Detail."""
    product = Product.query.filter_by(slug=slug).first_or_404()
    kit = None

    if not slug.startswith("kit-"):
        kit_slug = f"kit-{slug}"
        kit_product = Product.query.filter_by(slug=kit_slug).first()
        if kit_product:
            kit = {
                "id": kit_product.id,
                "name": kit_product.name,
                "price_ars": kit_product.price_ars,
                "description": kit_product.short_description or kit_product.description[:100],
            }

    return render_template("product.html", product=product, kit=kit)


@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    """Add To Cart."""
    Product.query.get_or_404(product_id)
    cart_list = session.setdefault("cart", [])
    if product_id not in cart_list:
        cart_list.append(product_id)
        session.modified = True
        flash("Ebook agregado a tu carrito.", "success")
    next_url = request.form.get("next") or request.referrer or url_for("shop")
    return redirect(next_url)


@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    """Remove From Cart."""
    cart_list = session.get("cart", [])
    if product_id in cart_list:
        cart_list.remove(product_id)
        session.modified = True
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    """Cart."""
    products = cart_products()
    return render_template("cart.html", products=products, total=sum(item.price_ars for item in products))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Checkout."""
    products = cart_products()
    if not products:
        return redirect(url_for("shop"))
    total = sum(item.price_ars for item in products)
    if request.method == "POST":
        buyer_name = request.form.get("buyer_name", "").strip()
        buyer_email = request.form.get("buyer_email", "").strip().lower()
        payment_method = request.form.get("payment_method", "mercadopago")

        if not buyer_name:
            flash("El nombre es requerido.", "error")
            return render_template("checkout.html", products=products, total=total)

        if not is_valid_email(buyer_email):
            flash("Ingresá un email válido.", "error")
            return render_template("checkout.html", products=products, total=total)

        # Crear orden
        order = Order(
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            total_ars=total,
            payment_method=payment_method,
            status="pending",
            download_token=secrets.token_urlsafe(32),
            ebook_type=("html_interactive" if any(
                p.product_type == "html_interactive" for p in products
            ) else "pdf"),
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
        items = [{"id": p.id, "name": p.name, "price_ars": p.price_ars}
                 for p in products]

        # Crear preferencia de pago según método
        if payment_method == "mercadopago":
            session["cart"] = []
            return redirect(url_for("payment_simulator", order_id=order.id))

        # PayPal: crear orden y redirigir
        pp_service = PayPalService(
            app.config["PAYPAL_CLIENT_ID"], app.config["PAYPAL_CLIENT_SECRET"])
        payment_result = pp_service.create_order(
            order.id, buyer_email, total, items)

        if payment_result.get("success") and not payment_result.get("is_demo"):
            session["cart"] = []
            return redirect(payment_result.get("checkout_url"))

        # PayPal demo: marcar como pagado y procesar
        order.status = "paid_demo"
        db.session.commit()
        session["cart"] = []

        email_service = EmailService(app.config["SENDGRID_API_KEY"])
        interactive_product = next(
            (p for p in products if p.product_type == "html_interactive"), None
        )
        if interactive_product:
            access_code = generate_access_code()
            while Order.query.filter_by(access_code=access_code).first():
                access_code = generate_access_code()

            if not interactive_product.ebook_file:
                raise FileNotFoundError("No HTML content found for this product")

            try:
                html_content = interactive_product.ebook_file.decode('utf-8')
                if not html_content or not html_content.strip():
                    raise ValueError("El archivo HTML está vacío")

                personalized_html = generate_personalized_html(
                    buyer_email, None, access_code, None, html_content=html_content
                )
                if not personalized_html or not personalized_html.strip():
                    raise ValueError("El HTML personalizado resultó vacío")

                order.access_code = access_code
                order.personalized_html_blob = personalized_html.encode('utf-8')
                db.session.commit()
                email_service.send_interactive_ebook(
                    buyer_email, interactive_product.name, access_code, None
                )
            except (FileNotFoundError, OSError, ValueError, UnicodeDecodeError) as e:
                order.status = "paid_demo_no_file"
                db.session.commit()
                print(f"Error processing interactive product: {str(e)}")
                flash(f"Pago registrado pero no se pudo generar el archivo: {str(e)}", "warning")
                email_service.send_download_link(
                    buyer_email, [interactive_product.name], order.download_token)
                return redirect(url_for("success", order_id=order.id))
            except Exception as e:
                order.status = "paid_demo_no_file"
                db.session.commit()
                print(f"Unexpected error processing interactive product: {str(e)}")
                flash(f"Error inesperado al procesar el archivo: {str(e)}", "error")
                return redirect(url_for("success", order_id=order.id))
        else:
            email_service.send_download_link(
                buyer_email, [p.name for p in products], order.download_token)

        return redirect(url_for("success", order_id=order.id))

    return render_template("checkout.html", products=products, total=total)


@app.route("/success/<int:order_id>")
def success(order_id):
    """Success."""
    order = Order.query.get_or_404(order_id)
    if order.status not in {"paid_demo", "paid"}:
        abort(403)
    return render_template("success.html", order=order)


@app.route("/download/<token>")
def download(token):
    """Download."""
    from flask import make_response
    from io import BytesIO

    order = Order.query.filter_by(download_token=token).first_or_404()
    if order.status not in {"paid_demo", "paid"}:
        abort(403, description="Esta descarga no está disponible para esta orden.")

    if not order.items:
        abort(400, description="Esta orden no tiene items.")

    product = Product.query.filter_by(
        id=order.items[0].product_id).first_or_404()

    if product.ebook_file:
        extension = Path(product.file_name).suffix.lower() if product.file_name else ".pdf"
        mime_type = "application/pdf" if extension == ".pdf" else "application/epub+zip"

        response = make_response(product.ebook_file)
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = f'attachment; filename="{product.file_name or product.slug + extension}"'
        return response

    return render_template("download_placeholder.html", product=product, order=order)


@app.get("/leer/<access_code>")
def read_interactive_ebook(access_code):
    """Read interactive ebook with device protection (max 2 devices)."""
    order = Order.query.filter_by(access_code=access_code).first_or_404()
    if order.status not in {"paid_demo", "paid"}:
        abort(403, description="Esta orden no está pagada.")
    if not order.personalized_html_blob:
        print(f"ERROR: Order {order.id} has no personalized_html_blob")
        abort(404, description="El archivo personalizado no está disponible.")

    from backend.models import DeviceSession
    user_agent = request.headers.get("User-Agent", "unknown")
    fingerprint = f"{user_agent}:{request.remote_addr}"

    existing_session = DeviceSession.query.filter_by(
        order_id=order.id, fingerprint=fingerprint
    ).first()

    if not existing_session:
        device_count = DeviceSession.query.filter_by(order_id=order.id).count()
        if device_count >= 2:
            abort(403, description="Has alcanzado el límite máximo de 2 dispositivos autorizados para este Ebook Interactivo.")

        new_session = DeviceSession(
            order_id=order.id,
            fingerprint=fingerprint,
            user_agent=user_agent
        )
        db.session.add(new_session)
        db.session.commit()

    try:
        html_content = order.personalized_html_blob.decode('utf-8')
        if not html_content or not html_content.strip():
            print(f"ERROR: Order {order.id} has empty personalized_html_blob")
            abort(500, description="El contenido HTML está vacío")
        return html_content, 200, {"Content-Type": "text/html; charset=utf-8"}
    except UnicodeDecodeError as e:
        print(f"ERROR: Failed to decode personalized_html_blob for order {order.id}: {str(e)}")
        abort(500, description="Error al leer el archivo")


@app.get("/pay/mercadopago/<int:order_id>")
def payment_simulator(order_id):
    """Simulador de pago de Mercado Pago para localhost."""
    order = Order.query.get_or_404(order_id)
    if order.status != "pending":
        abort(403, description="Esta orden ya fue pagada.")
    return render_template("payment_simulator.html", order=order)


@app.post("/process-payment/<int:order_id>")
def process_payment(order_id):
    """Procesa el pago simulado de Mercado Pago."""
    try:
        order = Order.query.get_or_404(order_id)
        if order.status != "pending":
            abort(403, description="Esta orden ya fue pagada.")

        card_number = request.form.get("card_number", "").replace(" ", "")
        expiry = request.form.get("expiry", "")
        cvv = request.form.get("cvv", "")
        cardholder = request.form.get("cardholder", "").strip()

        if not all([card_number, expiry, cvv, cardholder]):
            flash("Completá todos los datos de la tarjeta.", "error")
            return redirect(url_for("payment_simulator", order_id=order_id))

        valid_test_cards = [
            "4111111111111111",  # Visa aprobada
            "5425233430109903",  # MasterCard aprobada
            "3782822463100005",  # Amex aprobada
        ]

        if card_number not in valid_test_cards:
            flash("Tarjeta rechazada. Usa tarjetas de prueba válidas.", "error")
            return redirect(url_for("payment_simulator", order_id=order_id))

        order.status = "paid"
        db.session.commit()

        email_service = EmailService(app.config.get("SENDGRID_API_KEY", ""))
        interactive_product = None
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product and product.product_type == "html_interactive":
                interactive_product = product
                break

        if interactive_product:
            try:
                access_code = generate_access_code()
                while Order.query.filter_by(access_code=access_code).first():
                    access_code = generate_access_code()
                if not interactive_product.ebook_file:
                    raise FileNotFoundError("No HTML content found for this product")

                html_content = interactive_product.ebook_file.decode('utf-8')
                personalized_html = generate_personalized_html(
                    order.buyer_email, None, access_code, None, html_content=html_content
                )
                order.access_code = access_code
                order.personalized_html_blob = personalized_html.encode('utf-8')
                db.session.commit()
                email_service.send_interactive_ebook(
                    order.buyer_email, interactive_product.name, access_code, None
                )
            except (FileNotFoundError, OSError) as e:
                print(f"Error generando ebook: {str(e)}")
                product_names = [item.product_name for item in order.items]
                email_service.send_download_link(
                    order.buyer_email,
                    product_names,
                    order.download_token
                )
        else:
            product_names = [item.product_name for item in order.items]
            email_service.send_download_link(
                order.buyer_email,
                product_names,
                order.download_token
            )

        flash("Pago aprobado exitosamente.", "success")
        return redirect(url_for("success", order_id=order_id))
    except Exception as e:
        print(f"Error en process_payment: {str(e)}")
        flash(f"Error procesando pago: {str(e)}", "error")
        return redirect(url_for("payment_simulator", order_id=order_id))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin Login."""
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        email_matches = secrets.compare_digest(
            email, app.config.get("ADMIN_EMAIL", "")
        )
        password_matches = secrets.compare_digest(
            password, app.config.get("ADMIN_PASSWORD", "")
        )

        if email_matches and password_matches:
            session["is_admin"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash("Credenciales incorrectas.", "error")
    return render_template("admin/login.html")


@app.get("/admin/logout")
def admin_logout():
    """Admin Logout."""
    session.pop("is_admin", None)
    return redirect(url_for("home"))


@app.get("/admin")
@admin_required
def admin_dashboard():
    """Admin Dashboard."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    revenue = sum(order.total_ars for order in orders if order.status in {
                  "paid", "paid_demo"})
    return render_template("admin/dashboard.html", orders=orders, revenue=revenue, products=Product.query.all(), categories=CATEGORIES)


@app.get("/admin/products/<int:product_id>/edit")
@admin_required
def edit_product_form(product_id):
    """Get product for editing."""
    product = Product.query.get(product_id)
    if not product:
        return {"error": "No encontrado"}, 404
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "price_ars": product.price_ars,
        "category": product.category,
        "is_kit": product.is_kit,
        "kit_bonus_ids": product.kit_bonus_ids,
    }


@app.post("/admin/products/<int:product_id>/kit")
@admin_required
def update_product_kit(product_id):
    """Update Product KIT configuration."""
    product = Product.query.get(product_id)
    if not product:
        return {"error": "No encontrado"}, 404
    product.is_kit = request.form.get("is_kit") == "True"
    if product.is_kit:
        bonus_ids = []
        idx = 0
        while True:
            key = f'bonus_file_{idx}'
            if key not in request.files:
                break
            for bonus_file in request.files.getlist(key):
                if bonus_file and bonus_file.filename:
                    bonus_ids.append(f"{product.slug}_bonus_{idx}")
            idx += 1
        product.kit_bonus_ids = ",".join(bonus_ids) if bonus_ids else ""
        kit_price = request.form.get("kit_price_ars")
        if kit_price:
            product.kit_price_ars = int(kit_price)
        kit_desc = request.form.get("kit_description", "").strip()
        if kit_desc:
            product.kit_description = kit_desc
    else:
        product.kit_price_ars = None
        product.kit_description = None
    db.session.commit()
    return {"message": "Configuración KIT guardada"}


@app.post("/admin/products/<int:product_id>/edit")
@admin_required
def update_product(product_id):
    """Update Product."""
    product = Product.query.get(product_id)
    if not product:
        return {"error": "No encontrado"}, 404
    product.name = request.form.get("name", product.name).strip()
    product.description = request.form.get("description", product.description).strip()
    product.price_ars = int(request.form.get("price_ars", product.price_ars))
    product.category = request.form.get("category", product.category).strip()
    product.is_kit = request.form.get("is_kit") == "on"
    product.kit_bonus_ids = request.form.get("kit_bonus_ids", "") if product.is_kit else None
    ebook_file = request.files.get("ebook_file")
    if ebook_file and ebook_file.filename:
        product.ebook_file = ebook_file.read()
    db.session.commit()
    return {"message": "Producto actualizado"}


@app.delete("/admin/products/<int:product_id>")
@admin_required
def delete_product(product_id):
    """Delete Product."""
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Producto no encontrado"}, 404
    db.session.delete(product)
    db.session.commit()
    return {"message": "Producto eliminado"}


@app.post("/admin/products/<int:product_id>/create-kit")
@admin_required
def create_kit_from_product(product_id):
    """Create KIT version from existing product."""
    product = Product.query.get_or_404(product_id)

    kit_slug = f"kit-{product.slug}"
    if Product.query.filter_by(slug=kit_slug).first():
        return {"error": f"KIT ya existe: {kit_slug}"}, 400

    kit_price = int(request.form.get("kit_price_ars", int(product.price_ars * 1.15)))
    kit_description = request.form.get("kit_description",
        f"{product.description}\n\nIncluye el ebook principal y 3 bonus exclusivos: Modo Supervivencia, Mi Casa Funciona Así, Tarjetas Antibloqueo.")

    kit = Product(
        slug=kit_slug,
        name=f"KIT: {product.name}",
        description=kit_description,
        short_description=f"KIT completo con 3 bonus",
        category=product.category,
        price_ars=kit_price,
        cover_class=product.cover_class,
        accent=product.accent,
        featured=product.featured,
        file_name=product.file_name,
        cover_image=product.cover_image,
        cover_image_blob=product.cover_image_blob,
        product_type=product.product_type,
        source_html_path=product.source_html_path,
        ebook_file=product.ebook_file,
        is_kit=True,
        kit_price_ars=kit_price,
        kit_description=kit_description,
    )
    db.session.add(kit)
    db.session.commit()

    return {"message": f"KIT '{kit_slug}' creado exitosamente", "kit_id": kit.id}


@app.post("/admin/products")
@admin_required
def admin_create_product():
    """Admin Create Product."""
    slug = request.form["slug"].strip()
    name = request.form["name"].strip()
    product_type = request.form.get("product_type", "pdf")
    is_kit = request.form.get("is_kit") == "on"
    kit_bonus_ids = request.form.get("kit_bonus_ids", "")

    ebook_file = request.files.get("ebook_file")
    file_name = None
    source_html_path = None
    ebook_binary = None
    extension = (Path(ebook_file.filename).suffix.lower()
                 if ebook_file and ebook_file.filename else "")

    if not ebook_file:
        flash("Debes subir un archivo ebook.", "error")
        return redirect(url_for("admin_dashboard"))

    if product_type == "html_interactive" and extension == ".html":
        file_name = secure_filename(f"{slug}.html")
        ebook_binary = ebook_file.read()
        source_html_path = None
    elif product_type in {"pdf", "epub"} and extension in {".pdf",
                                                             ".epub"}:
        file_name = secure_filename(f"{slug}{extension}")
        ebook_binary = ebook_file.read()
    else:
        flash(("El archivo no coincide con el tipo de producto "
               "elegido."), "error")
        return redirect(url_for("admin_dashboard"))

    cover_file = request.files.get("cover_image")
    cover_image = None
    cover_image_blob = None
    if cover_file and cover_file.filename:
        cover_image_blob = cover_file.read()
        cover_image = secure_filename(f"{slug}{Path(cover_file.filename).suffix}")

    try:
        price_ars = int(request.form["price_ars"])
    except (ValueError, KeyError):
        flash("El precio debe ser un número válido.", "error")
        return redirect(url_for("admin_dashboard"))

    if price_ars <= 0:
        flash("El precio debe ser mayor a 0.", "error")
        return redirect(url_for("admin_dashboard"))

    description = request.form.get("description", "").strip()
    if not description:
        flash("La descripción es requerida.", "error")
        return redirect(url_for("admin_dashboard"))

    category = request.form.get("category", "").strip()
    if not category:
        flash("La categoría es requerida.", "error")
        return redirect(url_for("admin_dashboard"))

    product = Product(
        slug=slug,
        name=name,
        description=description,
        category=category,
        price_ars=price_ars,
        cover_class=request.form.get("cover_class", "coral"),
        accent=request.form.get("accent", "#C9756B"),
        featured=request.form.get("featured") == "on",
        file_name=file_name,
        cover_image=cover_image,
        cover_image_blob=cover_image_blob,
        product_type=product_type,
        source_html_path=source_html_path,
        ebook_file=ebook_binary,
        is_kit=is_kit,
        kit_bonus_ids=kit_bonus_ids if is_kit else None,
    )
    db.session.add(product)
    db.session.commit()
    flash(f"✅ Producto '{name}' creado exitosamente.", "success")
    return redirect(url_for("admin_dashboard"))


@app.post("/api/track-click")
def track_product_click():
    """Track Product Click."""
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
    """Track Page Visit."""
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
    """Return analytics stats for admin dashboard."""
    # Órdenes y ingresos
    all_orders = Order.query.all()
    paid_orders = [o for o in all_orders if o.status in {"paid", "paid_demo"}]
    total_revenue = sum(o.total_ars for o in paid_orders)

    # Clientes únicos
    unique_customers = len(set(o.buyer_email for o in paid_orders))

    # Últimos 30 días
    thirty_days_ago = datetime.datetime.utcnow() - datetime.timedelta(
        days=30)
    recent_orders = [o for o in paid_orders if o.created_at >= thirty_days_ago]
    recent_revenue = sum(o.total_ars for o in recent_orders)

    # Productos más vendidos
    product_sales = {}
    for order in paid_orders:
        for item in order.items:
            product_sales[item.product_name] = product_sales.get(
                item.product_name, 0) + 1

    top_products = sorted(product_sales.items(),
                          key=lambda x: x[1], reverse=True)[:5]

    # Productos más clicleados
    clicks = ProductClick.query.all()
    product_clicks = {}
    for click in clicks:
        key = click.product_name
        product_clicks[key] = product_clicks.get(key, 0) + 1

    top_clicked = sorted(product_clicks.items(),
                         key=lambda x: x[1], reverse=True)[:5]

    # Visitas últimos 30 días
    recent_visits = PageVisit.query.filter(
        PageVisit.visited_at >= thirty_days_ago).all()
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
    """Get Admin Orders."""
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
    """Get Products Analytics."""
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

    return {"products": sorted(product_data.values(),
                               key=lambda x: x["clicks"],
                               reverse=True)}


@app.get("/api/admin/products-list")
@admin_required
def get_products_list():
    """Return list of products for kit bonus selection."""
    try:
        products = Product.query.all()
        return {
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price_ars": p.price_ars,
                    "category": p.category,
                }
                for p in products
            ]
        }
    except Exception as e:
        print(f"Error en get_products_list: {str(e)}")
        return {"error": str(e), "products": []}, 200


@app.get("/image/<int:product_id>")
def serve_cover_image(product_id):
    """Serve cover image from database (BLOB)."""
    product = Product.query.get_or_404(product_id)
    if not product.cover_image_blob:
        abort(404, description="Imagen no disponible")

    from flask import send_file
    from io import BytesIO
    return send_file(
        BytesIO(product.cover_image_blob),
        mimetype="image/jpeg",
        as_attachment=False
    )


@app.get("/ebook-file/<int:product_id>")
@admin_required
def serve_ebook_file(product_id):
    """Serve ebook file from database (BLOB) - ADMIN ONLY."""
    product = Product.query.get_or_404(product_id)
    if not product.ebook_file:
        abort(404, description="Archivo no disponible")

    from flask import send_file
    from io import BytesIO

    mime_type = "application/pdf" if product.product_type == "pdf" else "text/html"
    filename = product.file_name or f"{product.slug}.{product.product_type}"

    return send_file(
        BytesIO(product.ebook_file),
        mimetype=mime_type,
        as_attachment=True,
        download_name=filename
    )


@app.post("/webhook/mercadopago")
def webhook_mercadopago():
    """Handle Mercado Pago payment notifications."""
    try:
        data = request.get_json() or {}
        topic = data.get("type") or data.get("topic")
        resource_id = data.get("data", {}).get("id") or data.get("id")

        if not topic or not resource_id:
            return {"status": "ok"}, 200

        if topic in {"payment", "merchant_order"}:
            mp_service = MercadoPagoService(app.config.get("MP_ACCESS_TOKEN"))
            payment_info = mp_service.verify_payment(resource_id)

            if payment_info.get("status") in {"approved", "paid", "paid_demo"}:
                external_ref = data.get("data", {}).get("external_reference", "")
                if external_ref and external_ref.startswith("order_"):
                    order_id = int(external_ref.split("_")[1])
                    order = Order.query.get(order_id)

                    if order and order.status == "pending":
                        order.status = "paid"
                        db.session.commit()

                        email_service = EmailService(app.config.get("SENDGRID_API_KEY"))

                        # Check if order contains interactive products
                        interactive_product = None
                        for item in order.items:
                            product = Product.query.get(item.product_id)
                            if product and product.product_type == "html_interactive":
                                interactive_product = product
                                break

                        if interactive_product:
                            access_code = generate_access_code()
                            while Order.query.filter_by(access_code=access_code).first():
                                access_code = generate_access_code()

                            if interactive_product.ebook_file:
                                try:
                                    html_content = interactive_product.ebook_file.decode('utf-8')
                                    if not html_content or not html_content.strip():
                                        raise ValueError("El archivo HTML está vacío")

                                    personalized_html = generate_personalized_html(
                                        order.buyer_email, None, access_code, None, html_content=html_content
                                    )
                                    if not personalized_html or not personalized_html.strip():
                                        raise ValueError("El HTML personalizado resultó vacío")

                                    order.access_code = access_code
                                    order.personalized_html_blob = personalized_html.encode('utf-8')
                                    db.session.commit()
                                    email_service.send_interactive_ebook(
                                        order.buyer_email, interactive_product.name, access_code, None
                                    )
                                except (UnicodeDecodeError, ValueError) as e:
                                    print(f"Error processing interactive product in webhook: {str(e)}")
                                except Exception as e:
                                    print(f"Unexpected error in webhook: {str(e)}")
                        else:
                            # Regular PDF download
                            product_names = [item.product_name for item in order.items]
                            email_service.send_download_link(
                                order.buyer_email,
                                product_names,
                                order.download_token
                            )

        return {"status": "ok"}, 200
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return {"status": "error", "message": str(e)}, 500


with app.app_context():
    db.create_all()
    migrate_product_columns()


if __name__ == "__main__":
    app.run(debug=True)
