from requests import get
from os import remove
from asyncio import sleep
from pyrogram.types import InputMediaPhoto
from main import bot, reg_handler, des_handler, par_handler


async def weather(message, args, origin_text):
    await message.edit("获取中 . . .")
    try:
        msg = message.text.split()[1]
    except ValueError:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    await bot.send_message('PagerMaid_Modify_bot', f'/weather_api {msg}')
    await sleep(5)
    await bot.read_history('PagerMaid_Modify_bot')
    async for msg in bot.iter_history('PagerMaid_Modify_bot', limit=1):
        weather_text = msg
    await message.edit(weather_text.caption)


async def pixiv(message, args, origin_text):
    await message.edit("获取中 . . .")
    try:
        msg = message.text.split()[1]
    except ValueError:
        await message.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    await bot.send_message('PagerMaid_Modify_bot', f'/pixiv_api {msg}')
    await sleep(5)
    await bot.read_history('PagerMaid_Modify_bot')
    async for msg in bot.iter_history('PagerMaid_Modify_bot', limit=1):
        pixiv_text = msg
    pixiv_list = pixiv_text.text.split('|||||')
    if len(pixiv_list) == 2:
        pixiv_albums = pixiv_list[1].split('|||')
        pixiv_album, pixiv_album_pyro = [], []
        await message.edit("下载图片中 . . .")
        for i in range(0, len(pixiv_albums)):
            r = get(pixiv_albums[i])
            with open("pixiv." + str(i) + ".jpg", "wb") as code:
                  code.write(r.content)
            photo_name = "pixiv." + str(i) + ".jpg"
            pixiv_album.extend([photo_name])
            pixiv_album_pyro.extend([InputMediaPhoto(photo_name, caption=pixiv_list[0])])
        await bot.send_media_group(message.chat.id, pixiv_album_pyro)
        await message.delete()
        for i in pixiv_album:
            try:
                remove(i)
            except:
                pass
    else:
        await message.edit(pixiv_text)


reg_handler('weather', weather)
reg_handler('pixiv', pixiv)
des_handler('weather', '使用彩云天气 api 查询国内实时天气。')
des_handler('pixiv', '查询插画信息。')
par_handler('weather', '<城市>')
par_handler('pixiv', '[<图片链接>]')
