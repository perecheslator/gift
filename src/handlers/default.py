from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import CommandStart

from src.gifts import parse_members

from config import ADMINS
from src.gifts import db


router = Router()
IS_ACTIVE = False


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        text='<b>⚡️ Отправьте чаты списком и парсинг пользователей начнется автоматически</b>\n\n<i>Советуем скидывать до 4 чатов где меньше 5 тыс. подписчиков</i>\n<b>Парсинг отменить нельзя!</b>'
    )


@router.message(F.from_user.id.in_(ADMINS))
async def chats_handler(message: Message):
    global IS_ACTIVE 

    if IS_ACTIVE:
        return await message.answer('<b>❌ Дождитесь окончания предыдущего парсинга</b>')

    IS_ACTIVE = True
    
    chats = message.text.split('\n')
    for index, chat in enumerate(chats):
        chats[index] = chat.replace('https://', '').replace('t.me/', '').replace('@', '')

    result_message = await message.answer(f'<b>📑 Начали парсинг {len(chats)} чатов.</b>')

    for chat in chats:
        async for result_gift in parse_members(chat):
            result_text = f'<b>🌟 Чат: @{chat} | Юзер: @{result_gift[0]["username"]} [id: {result_gift[0]["user_id"]}]</b>\n\n'
            gifts_text = ""

            for index, item in enumerate(result_gift):
                gift_line = f'<b><i>{db.check_gift(int(item["gift"]))}</i> Gift: {item["gift"]}</b>\n'
                
                if len(result_text + gifts_text + gift_line) <= 4096: # max telegram message size 
                    gifts_text += gift_line
                else:
                    break 
                    
            await result_message.reply(result_text + gifts_text)

    await result_message.reply(f'<b>✅ Парсинг окончен</b>')
    IS_ACTIVE = False