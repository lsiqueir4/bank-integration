import uuid
from models import Webhook, WebhookStatus, WebhookType
from repositories import BaseRepository


class WebhookRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def create_webhook(
        self, webhook_data, webhook_type=None, failure_reason=None, external_id=None
    ):
        new_webhook = Webhook()
        new_webhook.webhook_key = str(uuid.uuid4())
        new_webhook.external_id = external_id
        new_webhook.webhook_type = webhook_type
        new_webhook.status = self.get_enumerator(WebhookStatus, "failed")
        new_webhook.payload = webhook_data
        new_webhook.failure_reason = failure_reason

        self.session.add(new_webhook)

        return new_webhook

    def update_webhook(self, webhook: Webhook, webhook_status, failure_reason=None):
        webhook.status = webhook_status
        webhook.failure_reason = failure_reason

        self.session.add(webhook)

    def get_webhook_by_key(self, webhook_key):
        return self.session.query(Webhook).filter_by(web=webhook_key).first()

    def get_webhook_type(self, webhook_type_enumerator):
        return self.get_enumerator(WebhookType, webhook_type_enumerator)

    def get_webhook_status(self, webhook_status_enumerator):
        return self.get_enumerator(WebhookStatus, webhook_status_enumerator)
