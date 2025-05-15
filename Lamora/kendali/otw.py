from telethon import events
from telethon.tl.custom import Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

REQUIRED_CHANNEL = "ceritalamora"  # Ganti tanpa @

def register(client):
    @client.on(events.NewMessage(pattern=r'/start'))
    async def start_handler(event):
        user = await event.get_sender()
        me = await client.get_me()

        # Cek apakah user sudah join channel
        try:
            await client(GetParticipantRequest(REQUIRED_CHANNEL, user.id))
        except UserNotParticipantError:
            await event.respond(
                "kaka harus gabung ke channel aku terlebih dahulu kalau mau pakai bot ini.",
                buttons=[
                    [Button.url("join channel", f"https://t.me/{REQUIRED_CHANNEL}")],
                    [Button.inline("cek dulu kak", data="refresh_start")]
                ]
            )
            return

        await event.delete()  # Hapus pesan /start jika sudah join

        await event.respond(
            "hai kak! aku bot mention grup yang dibuat oleh @wlamora.\ncek tombol di bawah untuk cara pakai ya.",
            buttons=[
                [Button.inline("ʜᴇʟᴘ", data="show_help")],
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/nothinglamora"),
                    Button.url("ᴏᴡɴᴇʀ", "https://t.me/wlamora")
                ],
                [Button.url("ᴛᴀᴍʙᴀʜ ᴋᴇ ɢʀᴜᴘ", f"https://t.me/{me.username}?startgroup=true")]
            ]
        )

    @client.on(events.CallbackQuery(data=b"refresh_start"))
    async def refresh_start_handler(event):
        user = await event.get_sender()
        me = await client.get_me()

        # Cek lagi apakah sudah join
        try:
            await client(GetParticipantRequest(REQUIRED_CHANNEL, user.id))
        except UserNotParticipantError:
            await event.answer("kaka belum join channel.", alert=True)
            return

        try:
            await event.delete()
        except:
            pass

        await event.respond(
            "hai kak! aku bot mention grup yang dibuat oleh @wlamora.\ncek tombol di bawah untuk cara pakai ya.",
            buttons=[
                [Button.inline("ʜᴇʟᴘ", data="show_help")],
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/nothinglamora"),
                    Button.url("ᴏᴡɴᴇʀ", "https://t.me/wlamora")
                ],
                [Button.url("ᴛᴀᴍʙᴀʜ ᴋᴇ ɢʀᴜᴘ", f"https://t.me/{me.username}?startgroup=true")]
            ]
        )

    @client.on(events.CallbackQuery(data=b"show_help"))
    async def help_button_handler(event):
        await event.answer()
        help_text = (
            "bantuan cara pakai\n\n"
            "bot ini membantu kaka buat memanggil semua member di grup kaka dengan cepat.\n\n"
            "Perintah:\n"
            "• /utag atau /all — Sebut semua member\n"
            "• /admin atau @admins — sebut semua admin\n"
            "• /cancel — berhenti tagall\n\n"
            "bot cuma bisa digunakan di grup."
        )
        await event.edit(
            help_text,
            buttons=[
                [Button.inline("ʙᴀᴄᴋ", data="back")],
                [Button.inline("ᴄʟᴏsᴇ", data="close")]
            ]
        )

    @client.on(events.CallbackQuery(data=b"back"))
    async def back_button_handler(event):
        me = await client.get_me()
        await event.answer()
        await event.edit(
            "hai kak! aku bot mention grup yang dibuat oleh @wlamora.\ncek tombol di bawah untuk cara pakai ya.",
            buttons=[
                [Button.inline("ʜᴇʟᴘ", data="show_help")],
                [
                    Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/nothinglamora"),
                    Button.url("ᴏᴡɴᴇʀ", "https://t.me/wlamora")
                ],
                [Button.url("ᴛᴀᴍʙᴀʜ ᴋᴇ ɢʀᴜᴘ", f"https://t.me/{me.username}?startgroup=true")]
            ]
        )

    @client.on(events.CallbackQuery(data=b"close"))
    async def close_button_handler(event):
        await event.answer()
        try:
            await event.delete()
        except:
            pass