import aiofiles
import json

class UtilMethods:

    @staticmethod
    def is_user(ctx) -> bool:
        id_list = [520741459478052886, 841851864429625404]
        return ctx.author.id in id_list

    @staticmethod
    async def json_retriever(path: str):
        async with aiofiles.open(path, encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
