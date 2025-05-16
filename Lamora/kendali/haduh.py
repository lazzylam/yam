import re
import asyncio
import random
from datetime import datetime
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from Lamora.config import MENTION_CHUNK_SIZE, DELAY_BETWEEN_MESSAGES
from Lamora.kangen.hum import chunk_list

active_tags = {}
current_tasks = {}

EMOJIS = ['🔥', '✨', '❤️', '⚡', '⭐', '💥', '🎉', '😎', '🥳', '🌀', '🌟', '☄️', '🍀', '🚀']

def register(client):

    # Fungsi untuk memeriksa apakah user adalah admin
    async def is_admin(client, chat_id, user_id):
        async for admin in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
            if admin.id == user_id:
                return True
        return False

    @client.on(events.NewMessage(pattern='/utag'))
    async def tag_all_handler(event):
        if event.is_private:
            await event.respond("Perintah hanya bisa digunakan di grup.")
            return

        chat_id = event.chat_id
        user_id = event.sender_id
        
        # Memeriksa apakah pengirim adalah admin
        if not await is_admin(client, chat_id, user_id):
            await event.respond("Maaf, hanya admin yang dapat menggunakan perintah ini.")
            return
            
        full_text = event.message.text.replace('/utag', '', 1).strip()
        link_match = re.findall(r'https:\/\/t\.me\/(?:\+)?[\w\d_]+', full_text)
        link_block = '\n'.join(link_match[:5]) if link_match else ''
        message = re.sub(r'https:\/\/t\.me\/(?:\+)?[\w\d_]+', '', full_text).strip() or "Hai semua!"

        active_tags[chat_id] = True
        status = await event.respond("Mengumpulkan anggota...")

        members = await get_all_members(client, chat_id)
        if not members:
            await status.edit("Tidak bisa mengambil anggota.")
            active_tags[chat_id] = False
            return

        # Gunakan emoji acak sebagai teks mention yang menyebut user
        mentions = [f"[{random.choice(EMOJIS)}](tg://user?id={m['id']})" for m in members]
        chunks = chunk_list(mentions, MENTION_CHUNK_SIZE)
        await status.edit(f"Mulai tag {len(members)} member tiap {DELAY_BETWEEN_MESSAGES} detik.\nGunakan /cancel untuk hentikan.")

        async def do_mention_loop():
            try:
                for chunk in chunks:
                    if not active_tags.get(chat_id):
                        break
                    content = f"{message}\n\n{link_block}\n\n{' '.join(chunk)}"
                    await client.send_message(chat_id, content, parse_mode='markdown')
                    await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
                if active_tags.get(chat_id):
                    await client.send_message(chat_id, "semua anggota telah disebut. Selesai.")
            except Exception as e:
                await client.send_message(chat_id, f"Gagal mengirim: {e}")
            finally:
                active_tags[chat_id] = False
                current_tasks.pop(chat_id, None)

        current_tasks[chat_id] = asyncio.create_task(do_mention_loop())

    @client.on(events.NewMessage(pattern='/cancel'))
    async def cancel_tag(event):
        if event.is_private:
            await event.respond("Perintah hanya bisa digunakan di grup.")
            return

        chat_id = event.chat_id
        user_id = event.sender_id
        
        # Memeriksa apakah pengirim adalah admin
        if not await is_admin(client, chat_id, user_id):
            await event.respond("Maaf, hanya admin yang dapat menggunakan perintah ini.")
            return
            
        if active_tags.get(chat_id):
            active_tags[chat_id] = False
            await event.respond("Tag dihentikan oleh admin.")
        else:
            await event.respond("Tidak ada sesi tag yang aktif.")

    @client.on(events.NewMessage(pattern=r'/all'))
    async def alias_all(event):
        if event.is_private:
            await event.respond("Perintah hanya bisa digunakan di grup.")
            return
            
        chat_id = event.chat_id
        user_id = event.sender_id
        
        # Memeriksa apakah pengirim adalah admin
        if not await is_admin(client, chat_id, user_id):
            await event.respond("Maaf, hanya admin yang dapat menggunakan perintah ini.")
            return
            
        event.message.text = event.message.text.replace('/all', '/utag', 1)
        await tag_all_handler(event)

    @client.on(events.NewMessage(pattern=r'^/(admins?|admin)$'))
    async def mention_admins(event):
        if event.is_private:
            await event.respond("Perintah hanya bisa digunakan di grup.")
            return

        chat_id = event.chat_id
        admins = []
        async for user in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
            if user.bot or user.deleted:
                continue
            admins.append(user)

        if not admins:
            await event.reply("Tidak dapat menemukan admin.")
            return

        mention_texts = [f"[{random.choice(EMOJIS)}](tg://user?id={u.id})" for u in admins]
        await event.respond("Admin grup:\n" + " ".join(mention_texts), parse_mode='markdown')

    @client.on(events.NewMessage(pattern=r'@admins'))
    async def mention_admins_alias(event):
        await mention_admins(event)

# Fungsi mengambil semua anggota grup
async def get_all_members(client, chat_id):
    members = []
    async for user in client.iter_participants(chat_id, search='', limit=None):
        if user.bot or user.deleted:
            continue
        members.append({
            'id': user.id,
            'first_name': user.first_name or '',
            'username': user.username
        })
    return members