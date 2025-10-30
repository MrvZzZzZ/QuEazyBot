import aiosqlite
from config import DB_NAME

async def exec(query, params=()):
    with_params = query["param"]
    with_res = query["res"]
    sql = query["sql"]

    async def get_res_from_db(cursor):
        results = await cursor.fetchone()
        if results is not None:
            return results
        else:
            return 0

    async with aiosqlite.connect(DB_NAME) as db:
        if with_params:
            if with_res:
                async with db.execute(sql, params) as cursor:
                    return await get_res_from_db(cursor)
            else:
                await db.execute(sql, params)
                await db.commit()
        else:
            if with_res:
                async with db.execute(sql) as cursor:
                    return await get_res_from_db(cursor)
            else:       
                await db.execute(sql)
                await db.commit()


