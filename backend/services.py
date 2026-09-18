"""Servicios de pago e integración externa"""
import html as html_lib
import os
import re
import secrets
import ssl
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
    customer_email, html_original_path, access_code=None, output_path=None,
    html_content=None, product_name=None
):
    """Create an offline HTML copy with the buyer credentials embedded.

    Can accept either:
    - html_original_path: path to HTML file (for backward compatibility)
    - html_content: raw HTML string (preferred for database-backed storage)
    """
    try:
        if html_content:
            html = html_content
        else:
            original_path = Path(html_original_path)
            if not original_path.exists():
                raise FileNotFoundError(f"HTML file not found: {html_original_path}")
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
    except (OSError, IOError) as e:
        print(f"Error reading HTML file {html_original_path}: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error processing HTML: {str(e)}")
        raise

    if "id=\"personalized-login-screen\"" not in html:
        email_json = json.dumps(customer_email)
        code_json = json.dumps(access_code)
        login_title = html_lib.escape(product_name) if product_name else "Tu ebook interactivo"
        login_markup = f"""
<style id="personalized-login-style">
    #personalized-login-screen {{
        position: fixed; inset: 0; z-index: 2147483647; display: flex;
        align-items: center; justify-content: center; padding: 24px;
        background: linear-gradient(135deg, #31595a 0%, #24403f 100%);
        font-family: 'DM Sans', Arial, sans-serif;
    }}
    #personalized-login-screen .login-card {{
        width: min(100%, 420px); background: #fff; padding: 32px;
        border-radius: 12px; box-shadow: 0 16px 50px rgba(0,0,0,.18);
    }}
    #personalized-login-screen h2 {{ margin: 0 0 8px; color: #31595a; }}
    #personalized-login-screen p {{ color: #7d827d; }}
    #personalized-login-screen label {{ display:block; margin:14px 0 6px; color:#31595a; font-weight:bold; }}
    #personalized-login-screen input {{ width:100%; padding:12px; border:2px solid #d6cabb; border-radius:6px; box-sizing:border-box; }}
    #personalized-login-screen button {{ width:100%; margin-top:18px; padding:12px; border:0; border-radius:6px; background:#c9756b; color:#fff; font-weight:bold; cursor:pointer; }}
    #personalized-login-error {{ min-height:20px; color:#B44E4E!important; font-size:13px; }}
</style>
<div id="personalized-login-screen">
    <div class="login-card">
        <h2>{login_title}</h2>
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
        # Intentar inyectar antes de </body> (case-insensitive)
        if "</body>" in html.lower():
            body_close_idx = html.lower().rfind("</body>")
            html = html[:body_close_idx] + login_markup + html[body_close_idx:]
        else:
            # Si no tiene </body>, inyectar al final
            html = html + login_markup

    if output_path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding="utf-8")
        return str(destination)
    else:
        return html


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
                "external_reference": data.get("external_reference", ""),
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
        self.sandbox = os.getenv("PAYPAL_MODE", "live").lower() == "sandbox"

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
            print(f"PayPal auth failed for order {order_id}: "
                  f"{auth_response.status_code} {auth_response.text}")
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
        except requests.exceptions.HTTPError as e:
            print(f"PayPal create_order failed for order {order_id}: "
                  f"{response.status_code} {response.text}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            print(f"PayPal create_order error for order {order_id}: {str(e)}")
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

    def _smtp_config(self):
        """Smtp Config."""
        smtp_host = os.getenv("SMTP_HOST", "")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        sender = os.getenv("SMTP_FROM", smtp_user)
        configured = all([smtp_host, smtp_user, smtp_password, sender])
        return smtp_host, smtp_port, smtp_user, smtp_password, sender, configured

    def _send_via_sendgrid_api(self, buyer_email, subject, body):
        """Send via SendGrid's HTTPS API (works even when the host blocks
        outbound SMTP ports, like Render does)."""
        from_email = os.getenv("SMTP_FROM") or os.getenv("SENDGRID_FROM_EMAIL", "")
        if not from_email:
            return {"success": False, "error": "SENDGRID_FROM_EMAIL/SMTP_FROM not configured",
                     "message": "Falta configurar el email remitente para SendGrid"}
        try:
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": buyer_email}]}],
                    "from": {"email": from_email},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": body}],
                },
                timeout=15,
            )
            if response.status_code in (200, 202):
                print(f"Email sent via SendGrid to {buyer_email}: {subject}")
                return {"success": True, "is_demo": False, "message": "Email sent"}
            print(f"SendGrid API error sending to {buyer_email}: {response.status_code} {response.text}")
            return {"success": False, "error": "Email delivery failed", "message": response.text}
        except requests.RequestException as e:
            print(f"SendGrid API request failed sending to {buyer_email}: {str(e)}")
            return {"success": False, "error": "Email delivery failed", "message": str(e)}

    def _send(self, buyer_email, subject, body):
        """Send an email: SendGrid API first (HTTPS, not blocked by hosts
        that restrict outbound SMTP), SMTP as a fallback, demo log if
        neither is configured."""
        if self.api_key:
            return self._send_via_sendgrid_api(buyer_email, subject, body)

        smtp_host, smtp_port, smtp_user, smtp_password, sender, smtp_configured = self._smtp_config()

        if not smtp_configured:
            print(f"DEMO EMAIL TO: {buyer_email}\nSubject: {subject}\n\n{body}")
            return {"success": True, "is_demo": True, "message": "Email logged (no email provider configured)"}

        try:
            message = EmailMessage()
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = buyer_email
            message.set_content(body)

            # Use certifi's CA bundle explicitly - some minimal container
            # images lack a complete system CA store, which makes the
            # default SSL context reject even valid certificates.
            try:
                import certifi
                ssl_context = ssl.create_default_context(cafile=certifi.where())
            except ImportError:
                ssl_context = ssl.create_default_context()

            # Port 465 expects implicit SSL from the first byte; STARTTLS
            # (used on 587/25) fails or hangs if used against it.
            if smtp_port == 465:
                smtp = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15, context=ssl_context)
            else:
                smtp = smtplib.SMTP(smtp_host, smtp_port, timeout=15)

            with smtp:
                if smtp_port != 465:
                    smtp.starttls(context=ssl_context)
                smtp.login(smtp_user, smtp_password)
                smtp.send_message(message)
            print(f"Email sent to {buyer_email}: {subject}")
            return {"success": True, "is_demo": False, "message": "Email sent"}
        except (smtplib.SMTPException, OSError) as e:
            print(f"SMTP Error sending to {buyer_email} via {smtp_host}:{smtp_port}: {str(e)}")
            return {"success": False, "error": "Email delivery failed", "message": str(e)}

    def send_download_link(self, buyer_email, product_names, download_token):
        """Envía el enlace de descarga al cliente (compra de ebook normal)."""
        base_url = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:5000")
        download_url = f"{base_url}/download/{download_token}"
        subject = "¡Tu compra está lista!"
        body = (
            f"Hola,\n\n"
            f"¡Gracias por tu compra! Tus ebooks están listos:\n\n"
            + "\n".join(f"- {name}" for name in product_names)
            + f"\n\nDescargalos acá (vas a poder elegir PDF o EPUB si están disponibles): {download_url}\n\n"
            f"Este enlace es personal y no caduca, podés usarlo cuando quieras.\n\n"
            f"Ebooks para la vida"
        )
        return self._send(buyer_email, subject, body)

    def send_interactive_ebook(self, buyer_email, product_name, access_code, file_path):
        """Send notification with access code and read-online link."""
        base_url = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:5000")
        read_url = f"{base_url}/leer/{access_code}"
        subject = f"¡Tu compra de {product_name} está lista!"
        body = (
            f"Hola,\n\n"
            f"¡Gracias por tu compra de {product_name}!\n\n"
            f"Tu código de acceso es: {access_code}\n\n"
            f"Entrá acá cuando quieras leerlo: {read_url}\n\n"
            f"Guardá este email: el enlace y el código son personales, no caducan, "
            f"y los vas a necesitar para volver a entrar.\n\n"
            f"Ebooks para la vida"
        )
        return self._send(buyer_email, subject, body)
