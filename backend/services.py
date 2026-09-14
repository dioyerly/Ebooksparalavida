"""Servicios de pago e integración externa"""
import os
import re
import secrets
import string
import json
from pathlib import Path
from email.message import EmailMessage
import smtplib
import requests


def generate_access_code():
    """Generate a unique-looking eight-character access code."""
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(8))


def generate_personalized_html(
    customer_email, html_original_path, access_code=None, output_path=None
):
    """Create an offline HTML copy with the buyer credentials embedded."""
    original_path = Path(html_original_path)
    html = original_path.read_text(encoding="utf-8")
    escaped_email = customer_email.replace("\\", "\\\\").replace('"', '\\"')
    access_code = access_code or generate_access_code()
    escaped_code = access_code.replace("\\", "\\\\").replace('"', '\\"')

    # The supplied file already has the offline login; replace only its credentials.
    html = re.sub(
        r'(const emailCorrecto\s*=\s*)"[^"]*"',
        rf'\1"{escaped_email}"',
        html,
        count=1,
    )
    html = re.sub(
        r'(const codigoCorrecto\s*=\s*)"[^"]*"',
        rf'\1"{escaped_code}"',
        html,
        count=1,
    )
    html = re.sub(
        r'(data\.email\s*===\s*)"[^"]*"',
        rf'\1"{escaped_email}"',
        html,
        count=1,
    )
    html = re.sub(
        r'(<input[^>]+id=["\']login-email["\'][^>]+value=["\'])[^"\']*(["\'])',
        rf'\1{escaped_email}\2',
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    if "id=\"personalized-login-screen\"" not in html:
        email_json = json.dumps(customer_email)
        code_json = json.dumps(access_code)
        login_markup = f"""
<style id="personalized-login-style">
    #personalized-login-screen {{
        position: fixed; inset: 0; z-index: 2147483647; display: flex;
        align-items: center; justify-content: center; padding: 24px;
        background: linear-gradient(135deg, #D8A5A5 0%, #C8B8D8 100%);
        font-family: Arial, sans-serif;
    }}
    #personalized-login-screen .login-card {{
        width: min(100%, 420px); background: #fff; padding: 32px;
        border-radius: 12px; box-shadow: 0 16px 50px rgba(0,0,0,.18);
    }}
    #personalized-login-screen h2 {{ margin: 0 0 8px; color: #4A4A4A; }}
    #personalized-login-screen p {{ color: #666; }}
    #personalized-login-screen label {{ display:block; margin:14px 0 6px; color:#4A4A4A; font-weight:bold; }}
    #personalized-login-screen input {{ width:100%; padding:12px; border:2px solid #A8D5D5; border-radius:6px; box-sizing:border-box; }}
    #personalized-login-screen button {{ width:100%; margin-top:18px; padding:12px; border:0; border-radius:6px; background:#D8A5A5; color:#fff; font-weight:bold; cursor:pointer; }}
    #personalized-login-error {{ min-height:20px; color:#B44E4E!important; font-size:13px; }}
</style>
<div id="personalized-login-screen">
    <div class="login-card">
        <h2>The Romance Reader Kit</h2>
        <p>Ingresá el email de compra y tu código de acceso.</p>
        <label for="personalized-login-email">Email</label>
        <input id="personalized-login-email" type="email" autocomplete="email">
        <label for="personalized-login-code">Código</label>
        <input id="personalized-login-code" type="text" maxlength="8" autocomplete="off">
        <button type="button" onclick="validatePersonalizedLogin()">Ingresar</button>
        <p id="personalized-login-error"></p>
    </div>
</div>
<script>
(function() {{
    const emailExpected = {email_json};
    const codeExpected = {code_json};
    const storageKey = 'ebooks-para-la-vida-auth-' + codeExpected;
    window.validatePersonalizedLogin = function() {{
        const email = document.getElementById('personalized-login-email').value.trim();
        const code = document.getElementById('personalized-login-code').value.trim().toUpperCase();
        const error = document.getElementById('personalized-login-error');
        if (email === emailExpected && code === codeExpected) {{
            localStorage.setItem(storageKey, JSON.stringify({{ email: email, code: code, validado: true }}));
            document.getElementById('personalized-login-screen').remove();
        }} else {{
            error.textContent = 'Email o código incorrecto.';
        }}
    }};
    try {{
        const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
        if (saved && saved.validado && saved.email === emailExpected && saved.code === codeExpected) {{
            document.getElementById('personalized-login-screen').remove();
        }}
    }} catch (error) {{
        localStorage.removeItem(storageKey);
    }}
}})();
</script>
        """
        html = html.replace("</body>", login_markup + "</body>", 1)

    destination = Path(output_path or original_path.with_name(
        f"{original_path.stem}-{customer_email}.html"
    ))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")
    return str(destination)


class MercadoPagoService:
    """Integración con Mercado Pago para pagos en Argentina"""

    BASE_URL = "https://api.mercadopago.com"

    def __init__(self, access_token=None):
        self.access_token = access_token or os.getenv("MP_ACCESS_TOKEN", "")
        self.is_demo = not self.access_token or self.access_token == ""

    def create_preference(self, order_id, buyer_name, buyer_email, total_ars, items):
        """Crea una preferencia de pago en Mercado Pago"""
        if self.is_demo:
            return self._create_demo_preference(order_id, total_ars)

        base_url = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:5000")
        preference_data = {
            "items": [
                {
                    "id": str(item["id"]),
                    "title": item["name"][:256],
                    "quantity": 1,
                    "unit_price": float(item["price_ars"]),
                }
                for item in items
            ],
            "payer": {"email": buyer_email, "name": buyer_name},
            "external_reference": f"order_{order_id}",
            "back_urls": {
                "success": f"{base_url}/success/{order_id}",
                "failure": f"{base_url}/checkout",
                "pending": f"{base_url}/checkout",
            },
            "auto_return": "approved",
            "notification_url": f"{base_url}/webhook/mercadopago",
        }

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.post(
                f"{self.BASE_URL}/checkout/preferences",
                json=preference_data,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "success": True,
                "checkout_url": data.get("init_point"),
                "preference_id": data.get("id"),
            }
        except requests.exceptions.RequestException:
            return self._create_demo_preference(order_id, total_ars)

    def _create_demo_preference(self, order_id, total_ars):
        """URL de prueba - redirige a MP sandbox"""
        return {
            "success": True,
            "is_demo": True,
            "checkout_url": (
                f"https://www.mercadopago.com.ar/checkout/v1/redirect"
                f"?pref_id={order_id}_TEST"
            ),
        }

    def verify_payment(self, payment_id):
        """Verifica el estado de un pago"""
        if self.is_demo:
            return {"status": "paid_demo", "verified": True}

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.get(
                f"{self.BASE_URL}/v1/payments/{payment_id}",
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "status": data.get("status"),  # approved, pending, rejected, cancelled
                "verified": True,
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "verified": False}


class PayPalService:
    """Integración con PayPal para pagos internacionales"""

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or os.getenv("PAYPAL_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("PAYPAL_CLIENT_SECRET", "")
        self.is_demo = not self.client_id or self.client_id == ""
        self.sandbox = True  # Siempre usar sandbox en desarrollo

    def create_order(self, order_id, buyer_email, total_ars, items):
        """Crea una orden en PayPal"""
        if self.is_demo:
            return self._create_demo_order(order_id, total_ars)

        # Convertir ARS a USD (aproximado)
        ars_per_usd = float(os.getenv("ARS_PER_USD", "1450"))
        total_usd = round(total_ars / ars_per_usd, 2)

        base_url = (
            "https://api.sandbox.paypal.com"
            if self.sandbox
            else "https://api.paypal.com"
        )

        # Obtener token de acceso
        auth_response = requests.post(
            f"{base_url}/v1/oauth2/token",
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
            timeout=10,
        )

        if auth_response.status_code != 200:
            return {"success": False, "error": "Authentication failed"}

        access_token = auth_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(total_usd),
                        "breakdown": {
                            "item_total": {
                                "currency_code": "USD",
                                "value": str(total_usd),
                            }
                        },
                    },
                    "items": [
                        {
                            "name": item["name"],
                            "quantity": "1",
                            "unit_amount": {
                                "currency_code": "USD",
                                "value": str(
                                    round(item["price_ars"] / ars_per_usd, 2)
                                ),
                            },
                        }
                        for item in items
                    ],
                }
            ],
            "payer": {"email_address": buyer_email},
            "application_context": {
                "return_url": f"{os.getenv('PUBLIC_BASE_URL')}/success/{order_id}",
                "cancel_url": f"{os.getenv('PUBLIC_BASE_URL')}/checkout",
            },
        }

        try:
            response = requests.post(
                f"{base_url}/v1/checkout/orders",
                json=order_data,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "success": True,
                "order_id": data.get("id"),
                "checkout_url": next(
                    (link["href"] for link in data.get("links", []) if link["rel"] == "approve"),
                    None,
                ),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_demo_order(self, order_id, total_ars):
        """URL de prueba para PayPal en modo demo"""
        ars_per_usd = float(os.getenv("ARS_PER_USD", "1450"))
        total_usd = round(total_ars / ars_per_usd, 2)

        return {
            "success": True,
            "is_demo": True,
            "order_id": f"demo_{order_id}",
            "checkout_url": f"https://www.sandbox.paypal.com/checkoutnow?token=demo",
            "demo_message": f"MODO DEMO: Total ${total_usd:.2f} USD - Usa cuenta de prueba para completar",
        }


class EmailService:
    """Servicio de envío de emails"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SENDGRID_API_KEY", "")
        self.is_demo = not self.api_key or self.api_key == ""

    def send_download_link(self, buyer_email, product_names, download_token):
        """Envía el enlace de descarga al cliente"""
        if self.is_demo:
            return self._log_demo_email(buyer_email, product_names, download_token)

        # Implementar con SendGrid cuando esté disponible
        return {"success": False, "message": "SendGrid not configured"}

    def send_interactive_ebook(self, buyer_email, product_name, access_code, file_path):
        """Send notification with access code (no file attachment)."""
        subject = f"¡Tu compra de {product_name} está lista!"
        body = (
            f"Hola,\n\n"
            f"¡Gracias por tu compra de {product_name}!\n\n"
            f"Tu código de acceso es: {access_code}\n\n"
            f"Descargá tu ebook desde tu cuenta y usa este código para acceder.\n\n"
            f"Ebooks para la vida"
        )
        smtp_host = os.getenv("SMTP_HOST", "")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        sender = os.getenv("SMTP_FROM", smtp_user)
        smtp_configured = all([smtp_host, smtp_user, smtp_password, sender])

        if not smtp_configured:
            print(f"DEMO EMAIL TO: {buyer_email}\nSubject: {subject}\n\n{body}")
            return {"success": True, "is_demo": True, "message": "Interactive email logged"}

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = buyer_email
        message.set_content(body)
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(smtp_user, smtp_password)
            smtp.send_message(message)
        return {"success": True, "is_demo": False, "message": "Interactive email sent"}

    def _log_demo_email(self, buyer_email, product_names, download_token):
        """En modo demo, solo registra que se enviaría el email"""
        download_url = (
            f"{os.getenv('PUBLIC_BASE_URL', 'http://127.0.0.1:5000')}"
            f"/download/{download_token}"
        )

        email_content = f"""
        DEMO - EMAIL QUE SE ENVIARÍA A: {buyer_email}

        Asunto: ¡Tu ebook está listo para descargar!

        ---

        ¡Hola!

        Gracias por tu compra. Tus ebooks están listos:

        {chr(10).join(f"- {name}" for name in product_names)}

        Descargá aquí: {download_url}

        Este enlace es personal y no caduca.

        ---
        Ebooks para la vida
        """

        print(email_content)

        return {
            "success": True,
            "is_demo": True,
            "message": f"Demo: email sent to {buyer_email}",
            "download_url": download_url,
        }
