from telethon import events

def register(client):

    @client.on(events.NewMessage(pattern=r'/help'))
    async def help_handler(event):
        await event.respond("""
Perintah:
- `/utag` atau `/all` - Mention semua anggota grup
- `/cancel` - Batalkan proses mention
- `/help` - Bantuan
        """, parse_mode='markdown')
