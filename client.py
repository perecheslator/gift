import os
import asyncio

from typing import AsyncGenerator, Dict, Any

from pyrogram import Client
from pyrogram.types import ChatMember
from pyrogram.enums import ChatMemberStatus

from modules.config import API_HASH, API_ID, GIFT_IDS
from modules import db

from telethon.tl.functions.messages import ImportChatInviteRequest
from modules import config




async def get_client():
    session = [file for file in os.listdir('session') if file.split('.')[-1] == 'session']
    
    if not session:
        session = ['main']
    
    client = Client(
        name=f'session/{session[0].replace(".session", "")}',
        api_id=API_ID,
        api_hash=API_HASH,
        system_version="4.16.30-vxCUSTOM"
    )

    await client.start()
    return client

async def send_msg(username, client):
    await client.send_message(username, db.check_config_send_msg(None))



async def parse_members(chat: str) -> AsyncGenerator[Dict[str, Any], None]:
    client = await get_client()
    
    
    try:
        async for user in client.get_chat_members(chat):
            user: ChatMember
            if user.status == ChatMemberStatus.MEMBER:
                gifts = await get_user_gifts(client, user.user.id, user.user.username)

                if gifts:
                    await send_msg(user.user.username, client)
                    yield gifts

                    
                await asyncio.sleep(0.5)


    except Exception as e:
        print(e)
    
    if client:
        await client.stop()



b = 0

async def get_user_gifts(client: Client, user_id: int, username: str):
    global b

    result = []
    a = 1
    b += 1
    try:
        
        async for gift in client.get_user_gifts(user_id):
            
            #print(a, gift.can_upgrade, gift.is_limited, gift.id)
            
            if gift.id in config.GIFT_IDS:
            #f git:
                result.append({"gift": gift.id, "user_id": user_id, "username": username, "status": ')'})
        
        

        
    except Exception as e:
        print(f"Ошибка при получении пользователя: {e}")
        return []


    #print(f'{b} Смотрю: @{username}')


    return result



async def main():
    client = await get_client()


if __name__ == '__main__':
    asyncio.run(main())