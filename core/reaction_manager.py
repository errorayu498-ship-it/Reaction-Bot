import aiohttp
import asyncio

class ReactionManager:

    def __init__(self, token_manager):
        self.tm = token_manager
        self.running = False

    async def start(self, channel_id, message_id, emoji):

        self.running = True
        tokens = self.tm.load_tokens()

        async with aiohttp.ClientSession() as session:

            for token in tokens:

                if not self.running:
                    break

                url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"

                headers = {"Authorization": f"Bot {token}"}

                async with session.put(url, headers=headers):
                    pass

                await asyncio.sleep(1)

    def stop(self):
        self.running = False
