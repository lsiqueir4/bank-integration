from flask_smorest import Blueprint
from controllers import BaseController
from errors import APIError
from repositories import WebhookRepository
from services import InvoiceService
from schemas import ResponseWebhookSchema
from flask import request

blp = Blueprint("Webhook", __name__, url_prefix="/webhook")


class WebhookController(BaseController):
    def __init__(self):
        super().__init__()
        self.webhook_bp = blp
        self.webhook_bp.add_url_rule(
            "", view_func=self.proccess_webhook, methods=["POST"]
        )
        self.webhook_bp.add_url_rule(
            "/webhook_key/<webhook_key>",
            view_func=self.get_webhook_by_key,
            methods=["GET"],
        )
        self.webhook_repository = WebhookRepository(self.db.session)

    @blp.response(201, ResponseWebhookSchema)
    def proccess_webhook(self):
        webhook_event = request.get_json().get("event")
        failure_reason = ""
        if not webhook_event:
            failure_reason = "Invalid webhook data format"

        webhook_subscription = webhook_event.get("subscription")
        webhook_type_enumerator = (
            f"{webhook_subscription}_{webhook_event.get('log', {}).get('type')}"
        )
        webhook_type = self.webhook_repository.get_webhook_type(webhook_type_enumerator)
        if not webhook_type:
            failure_reason = f"Unknown webhook type: {webhook_type_enumerator}"

        webhook = self.webhook_repository.get_webhook_by_external_id(
            external_id=webhook_event.get("id")
        )

        if webhook and webhook.status.enumerator == "processed":
            return
        if not webhook:
            webhook = self.webhook_repository.create_webhook(
                webhook_data=webhook_event,
                webhook_type=webhook_type,
                external_id=webhook_event.get("id"),
            )

        if failure_reason:
            self.webhook_repository.session.commit()

        else:
            service_handler = {
                "invoice": InvoiceService(db_session=self.db.session),
            }.get(webhook_subscription)

            failure_reason = service_handler.process(webhook_event)

            webhook_status = self.webhook_repository.get_webhook_status(
                "failed" if failure_reason else "processed"
            )

            self.webhook_repository.update_webhook(
                webhook, webhook_status, failure_reason
            )

            self.webhook_repository.session.commit()

        return webhook

    @blp.response(200, ResponseWebhookSchema)
    def get_webhook_by_key(self, webhook_key: str):
        webhook = self.webhook_repository.get_webhook_by_key(webhook_key)
        if not webhook:
            raise APIError(message="Webhook not found.", status_code=404)
        return webhook
