import aiohttp

class ServerManager:

    def __init__(self, token_manager):
        self.tm = token_manager

    async def join_servers(self, invite):

        tokens = self.tm.load_tokens()

        joined = 0
        failed = 0

        async with aiohttp.ClientSession() as session:

            for token in tokens:

                headers = {"Authorization": f"Bot {token}"}

                url = f"https://discord.com/api/v10/invites/{invite}"

                async with session.post(url, headers=headers) as r:

                    if r.status == 200:
                        joined += 1
                    else:
                        failed += 1

        return {"joined": joined, "failed": failed}
