"""Servicios de pago e integración externa"""
import os
import requests


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

    def _log_demo_email(self, buyer_email, product_names, download_token):
        """En modo demo, solo registra que se enviaría el email"""
        download_url = (
            f"{os.getenv('PUBLIC_BASE_URL', 'http://127.0.0.1:5000')}"
            f"/download/{download_token}"
        )

        email_content = f"""
        ✅ DEMO - EMAIL QUE SE ENVIARÍA A: {buyer_email}

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
