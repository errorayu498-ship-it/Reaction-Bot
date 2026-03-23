import aiohttp

class TokenManager:

    def __init__(self):
        self.file = "tokens.txt"

    def load_tokens(self):
        with open(self.file) as f:
            return [t.strip() for t in f.readlines() if t.strip()]

    def count_tokens(self):
        return len(self.load_tokens())

    def add_tokens(self, tokens):

        with open(self.file, "a") as f:
            for t in tokens:
                f.write(t+"\n")

        return len(tokens)

    async def check_tokens(self):

        tokens = self.load_tokens()

        results = []

        async with aiohttp.ClientSession() as session:

            for token in tokens:

                headers = {"Authorization": f"Bot {token}"}

                async with session.get(
                    "https://discord.com/api/v10/users/@me",
                    headers=headers
                ) as r:

                    results.append(r.status == 200)

        return results
