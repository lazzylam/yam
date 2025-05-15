import logging
from typing import List, Dict
from telethon.tl.types import Channel, Chat

from client import client

logger = logging.getLogger(__name__)

async def get_visible_members(chat_id: int, event) -> List[Dict]:
    members = []
    seen_ids = set()

    try:
        chat = await event.get_chat()

        try:
            admin_info = await client.get_participants(chat_id, filter="admins")
            admins = [admin.id for admin in admin_info]
        except Exception as e:
            logger.warning(f"Gagal ambil admin: {e}")
            admins = []

        try:
            participants = await client.get_participants(chat_id, limit=200)
            for p in participants:
                if not p.bot and not p.deleted and p.id not in seen_ids:
                    members.append({
                        'id': p.id,
                        'username': p.username,
                        'first_name': p.first_name or "User"
                    })
                    seen_ids.add(p.id)
        except Exception:
            async for msg in client.iter_messages(chat_id, limit=200):
                if msg.sender_id and msg.sender_id not in seen_ids:
                    try:
                        user = await client.get_entity(msg.sender_id)
                        if not user.bot and not user.deleted:
                            members.append({
                                'id': user.id,
                                'username': user.username,
                                'first_name': user.first_name or "User"
                            })
                            seen_ids.add(user.id)
                    except Exception:
                        continue

        for admin_id in admins:
            if admin_id not in seen_ids:
                try:
                    admin = await client.get_entity(admin_id)
                    if not admin.bot and not admin.deleted:
                        members.append({
                            'id': admin.id,
                            'username': admin.username,
                            'first_name': admin.first_name or "Admin"
                        })
                except Exception:
                    continue

        return members

    except Exception as e:
        logger.error(f"Error get member: {e}")
        return []
