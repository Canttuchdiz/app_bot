import aiofiles
import json

class EasyJson:

    @staticmethod
    async def json_retriever(path : str):
        async with aiofiles.open(path, encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)

class UserCheck:

    @staticmethod
    def is_user(ctx) -> bool:
        return ctx.author.id == 1023094431349473310
