import aiofiles
import json

class UtilMethods:

    # Contains methods that I will use to reduce redundancy

    @staticmethod
    def is_user(ctx) -> bool:
        id_list = [520741459478052886, 841851864429625404]
        return ctx.author.id in id_list

    @staticmethod
    def json_retriever(path: str):
        with aiofiles.open(path, encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
