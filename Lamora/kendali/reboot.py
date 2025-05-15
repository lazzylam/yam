import os
import sys
import asyncio
from telethon import events
from Lamora.config import DEVS, UPSTREAM_REPO, UPSTREAM_BRANCH, GIT_TOKEN

def register(client):
    @client.on(events.NewMessage(pattern="/reboot"))
    async def reboot_handler(event):
        if event.sender_id not in DEVS:
            return

        msg = await event.reply("Mengambil update dari GitHub...")

        if not GIT_TOKEN:
            await msg.edit("Gagal: Token GitHub tidak ditemukan.")
            return

        repo_url = UPSTREAM_REPO.replace("https://", f"https://{GIT_TOKEN}@")

        cmd = f"""
        rm -rf .git && \
        git init && \
        git config --global user.email "you@example.com" && \
        git config --global user.name "YourName" && \
        git remote add origin {repo_url} && \
        git fetch origin {UPSTREAM_BRANCH} && \
        git reset --hard origin/{UPSTREAM_BRANCH}
        """

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            await msg.edit(f"Gagal update:\n{stderr.decode()}")
            return

        # Simpan chat_id untuk notifikasi setelah reboot
        with open("rebooting.txt", "w") as f:
            f.write(str(event.chat_id))

        await msg.edit("✅ gitpull berhasil, mematikan bot...")
        await asyncio.sleep(2)
        os.execv(sys.executable, [sys.executable, "-m", "Lamora"])