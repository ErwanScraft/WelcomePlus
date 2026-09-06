import threading
from datetime import datetime, timezone

from .client import WebhookClient


class WelcomePlusWebhook:
    def __init__(self, plugin, config) -> None:
        self.plugin = plugin
        self.config = config
        self.client = WebhookClient(plugin)

    def dispatch(self, event: str, data: dict) -> None:
        webhook = self.config.get_feature("webhook")

        if not webhook.get("enabled", False):
            return

        events = webhook.get("events", {})

        if not events.get(event, False):
            return

        url = str(webhook.get("url", "")).strip()

        if not url:
            self.plugin.logger.warning(
                "Webhook is enabled but no URL is configured."
            )
            return

        payload = {
            "version": 1,
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data,
        }

        secret = str(webhook.get("secret", "")).strip()

        timeout = webhook.get("timeout", 5)

        try:
            timeout = float(timeout)
        except (TypeError, ValueError):
            timeout = 5.0

        threading.Thread(
            target=self.client.send,
            args=(url, payload, secret, timeout),
            daemon=True,
            name="WelcomePlus-Webhook",
        ).start()