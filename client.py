# client.py
import asyncio, ssl, sys, os
from rich.console import Console

IP = "45.38.139.91"
PORT = 5555
console = Console()

async def chat():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    try:
        reader, writer = await asyncio.open_connection(IP, PORT, ssl=ssl_ctx)
    except Exception as e:
        console.print(f"[bold red]❌ Connection failed: {e}[/bold red]")
        return

    # گرفتن اطلاعات ورودی بدون نمایش راهنما
    pw = input()
    writer.write((pw + "\n").encode())
    await writer.drain()

    nickname = input()
    writer.write((nickname + "\n").encode())
    await writer.drain()

    if nickname == "admin":
        admin_pw = input()
        writer.write((admin_pw + "\n").encode())
        await writer.drain()

    async def listen():
        while True:
            try:
                data = await reader.readline()
                if not data:
                    console.print("[bold red]⛔ Server disconnected.[/bold red]")
                    writer.close()
                    break

                decoded = data.decode().strip()
                if decoded == "\033c":
                    os.system("cls" if os.name == "nt" else "clear")
                else:
                    console.print(decoded, style="bold white")

            except Exception as e:
                console.print(f"[bold red]⚠️ Error: {e}[/bold red]")
                break

    asyncio.create_task(listen())

    try:
        while True:
            msg = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            msg = msg.strip()
            if msg == "/exit":
                writer.write((msg + "\n").encode())
                await writer.drain()
                writer.close()
                break
            writer.write((msg + "\n").encode())
            await writer.drain()
    except Exception as e:
        console.print(f"[bold red]⚠️ Client error: {e}[/bold red]")

asyncio.run(chat())
