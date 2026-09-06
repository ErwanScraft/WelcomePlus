import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class WebhookClient:
    def __init__(self, plugin) -> None:
        self.plugin = plugin

    def send(
        self,
        url: str,
        payload: dict,
        secret: str = "",
        timeout: float = 5.0,
    ) -> None:
        body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "WelcomePlus/0.1",
        }

        if secret:
            headers["Authorization"] = f"Bearer {secret}"

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