import re
import asyncio
import random
import time
from datetime import datetime, timedelta
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from Lamora.config import MENTION_CHUNK_SIZE, DELAY_BETWEEN_MESSAGES
from Lamora.kangen.hum import chunk_list

active_tags = {}
current_tasks = {}
tag_timers = {}

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
        
        # Extract time limit in minutes from the end of the message if present
        time_limit_minutes = None
        time_match = re.search(r'\s+(\d+)$', full_text)
        if time_match:
            time_limit_minutes = int(time_match.group(1))
            full_text = re.sub(r'\s+\d+$', '', full_text)
        
        link_match = re.findall(r'https:\/\/t\.me\/(?:\+)?[\w\d_]+', full_text)
        # Format links dengan '>' sebagai penunjuk dan pastikan tiap link di baris baru
        formatted_links = ""
        if link_match:
            formatted_links = "\n".join([f"> {link}" for link in link_match[:5]])
        message = re.sub(r'https:\/\/t\.me\/(?:\+)?[\w\d_]+', '', full_text).strip() or "Hai semua!"

        # Jika sudah ada tag yang berjalan di chat ini
        if chat_id in active_tags and active_tags[chat_id]:
            await event.respond("Ada tag yang sedang berjalan. Gunakan /cancel untuk menghentikannya terlebih dahulu.")
            return

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
        
        time_info = f" selama {time_limit_minutes} menit" if time_limit_minutes else ""
        await status.edit(f"Mulai tag {len(members)} member tiap {DELAY_BETWEEN_MESSAGES} detik{time_info}.\nGunakan /cancel untuk hentikan.")

        async def do_mention_loop():
            try:
                end_time = None
                if time_limit_minutes:
                    end_time = datetime.now() + timedelta(minutes=time_limit_minutes)
                
                tagged_count = 0
                for chunk in chunks:
                    if not active_tags.get(chat_id):
                        break
                    
                    # Check if time limit is reached
                    if end_time and datetime.now() >= end_time:
                        await client.send_message(chat_id, f"Batas waktu {time_limit_minutes} menit tercapai. Tag dihentikan setelah menyebut {tagged_count} anggota.")
                        break
                        
                    # Format links dengan '>' sebagai penunjuk dan pastikan tiap link di baris baru
                    formatted_links = ""
                    if link_match:
                        formatted_links = "\n".join([f"> {link}" for link in link_match[:5]])
                    
                    content = f"{message}\n\n{formatted_links}\n\n{' '.join(chunk)}"
                    await client.send_message(chat_id, content, parse_mode='markdown')
                    tagged_count += len(chunk)
                    await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
                
                if active_tags.get(chat_id) and (end_time is None or datetime.now() < end_time):
                    await client.send_message(chat_id, f"Semua {tagged_count} anggota telah disebut. Selesai.")
            except Exception as e:
                await client.send_message(chat_id, f"Gagal mengirim: {e}")
            finally:
                active_tags[chat_id] = False
                current_tasks.pop(chat_id, None)
                if chat_id in tag_timers:
                    del tag_timers[chat_id]

        current_tasks[chat_id] = asyncio.create_task(do_mention_loop())
        
        # Set timer if specified
        if time_limit_minutes:
            tag_timers[chat_id] = {
                'start_time': datetime.now(),
                'end_time': datetime.now() + timedelta(minutes=time_limit_minutes)
            }

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
            if chat_id in tag_timers:
                del tag_timers[chat_id]
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

    @client.on(events.NewMessage(pattern=r'/tagstatus'))
    async def tag_status(event):
        if event.is_private:
            await event.respond("Perintah hanya bisa digunakan di grup.")
            return

        chat_id = event.chat_id
        
        if chat_id in active_tags and active_tags[chat_id]:
            if chat_id in tag_timers:
                current_time = datetime.now()
                start_time = tag_timers[chat_id]['start_time']
                end_time = tag_timers[chat_id]['end_time']
                elapsed = current_time - start_time
                remaining = end_time - current_time if current_time < end_time else timedelta(0)
                
                elapsed_mins = int(elapsed.total_seconds() / 60)
                elapsed_secs = int(elapsed.total_seconds() % 60)
                remaining_mins = int(remaining.total_seconds() / 60)
                remaining_secs = int(remaining.total_seconds() % 60)
                
                status_msg = f"Tag sedang aktif dengan timer:\n"
                status_msg += f"⏱️ Berjalan: {elapsed_mins} menit {elapsed_secs} detik\n"
                status_msg += f"⏳ Sisa waktu: {remaining_mins} menit {remaining_secs} detik"
                await event.respond(status_msg)
            else:
                await event.respond("Tag sedang aktif tanpa batas waktu.")
        else:
            await event.respond("Tidak ada sesi tag yang aktif.")

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