import json
import threading
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class WelcomePlusWebhook:
    def __init__(self, plugin, config) -> None:
        self.plugin = plugin
        self.config = config

    def send_player_join(self, player) -> None:
        webhook = self.config.get_feature("webhook")

        if not webhook.get("enabled", False):
            return

        events = webhook.get("events", {})

        if not events.get("player_join", False):
            return

        url = str(webhook.get("url", "")).strip()

        if not url:
            self.plugin.logger.warning(
                "Webhook is enabled but no URL is configured."
            )
            return

        payload = self._build_player_join_payload(player)

        threading.Thread(
            target=self._send,
            args=(url, payload, webhook),
            daemon=True,
            name="WelcomePlus-Webhook",
        ).start()

    def _build_player_join_payload(self, player) -> dict:
        return {
            "event": "player_join",
            "player": {
                "name": player.name,
                "uuid": str(player.unique_id),
            },
        }

    def _send(
        self,
        url: str,
        payload: dict,
        webhook: dict,
    ) -> None:
        body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "WelcomePlus/0.1",
        }

        secret = str(webhook.get("secret", "")).strip()

        if secret:
            headers["Authorization"] = f"Bearer {secret}"

        timeout = webhook.get("timeout", 5)

        try:
            timeout = float(timeout)
        except (TypeError, ValueError):
            timeout = 5.0

        try:
            request = Request(
                url,
                data=body,
                headers=headers,
                method="POST",
            )

            with urlopen(request, timeout=timeout) as response:
                status = response.status

            if 200 <= status < 300:
                self.plugin.logger.debug(
                    f"Webhook sent successfully: {payload['event']}"
                )
            else:
                self.plugin.logger.warning(
                    f"Webhook returned HTTP {status}."
                )

        except HTTPError as error:
            self.plugin.logger.warning(
                f"Webhook request failed with HTTP {error.code}: "
                f"{error.reason}"
            )

        except URLError as error:
            self.plugin.logger.warning(
                f"Webhook connection failed: {error.reason}"
            )

        except Exception as error:
            self.plugin.logger.error(
                f"Unexpected webhook error: {error}"
            )