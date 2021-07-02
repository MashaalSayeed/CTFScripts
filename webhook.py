import requests
from config import URL


class DiscordWebhook(dict):
	def __init__(self, url: str=URL, timeout: int=None, **kwargs):
		"""
		Initialises a webhook to a discord channel
		:param url: Webhook url (Defaults to one in config.py)
		:param timeout: Timeout in seconds
		:keyword content: The message content
        :keyword username: Webhook username
        :keyword avatar_url: Webhook avatar
        :keyword tts: TTS message (bool)
        :keyword file: File contents
        :keyword filename: File name
        :keyword embeds: List of discord embeds
        :keyword allowed_mentions: List of allowed mentions
		"""
		super().__init__()

		self.url = url
		self.timeout = timeout
		self.update(kwargs)

	def send(self):
		"""
		Sends a webhook message to a discord channel
		"""
		result = requests.post(self.url, timeout=self.timeout, json=self)
		if 200 <= result.status_code < 300:
			print(f"Webhook sent {result.status_code}")
		else:
			print(f"Webhook failed {result.status_code}\n{result.json()}")
		return result


if __name__ == "__main__":
	webhook = DiscordWebhook()
	webhook['content'] = 'This is a test! Alrighty'
	webhook.send()