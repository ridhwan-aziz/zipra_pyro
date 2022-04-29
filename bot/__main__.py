from .utils import init
from .utils.parser import Parser

client = init.client
pyrogram = init.pyrogram
logging = init.logging

if init.debug:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.getLogger().setLevel(logging.WARNING)


@client.on_message()
async def message_handler(_, msg: pyrogram.types.Message):
    text = msg.text or msg.caption or "None"
    parsed = Parser(init.me.username).parse(text)
    # if msg.from_user.id == 1923158017:
    #     await msg.reply(f"raw_cmd: {parsed.req.to_dict()}\ncmd: {parsed.req.cmd}\nargs: {parsed.args.args}\nraw_args: "
    #                     f"{parsed.args.to_dict()}", False)
    if parsed.req.cmd == "ping":
        return await msg.reply("PONG!")


logging.info(f"[Main] Client started with {client.workers} workers")
client.run()
logging.info("[Main] Client stopped")
