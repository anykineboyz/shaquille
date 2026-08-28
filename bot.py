from flask import Flask, request
import requests
import os
import re
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

BOT_ID = os.environ.get("BOT_ID")

# -----------------------------
# NIKO BANNED WORDS
# -----------------------------

NIKO_ONLY_BANNED_WORDS = [
    "eva",
    "rene",
    "brendon",
    "drill sergeant",
    "clanker",
    "shh",
    "hehe",
    "haha",
    "die",
    "kill",
    "stupid",
    "dumb",
    "mom",
    "dad",
    "shhh",
    "idiot",
    "ass",
    "shut",
    "uncle",
    "aunty",
    "what",
    "no",
    "stop",
    "fine"
]

# -----------------------------
# STORAGE
# -----------------------------

message_count = 0

# -----------------------------
# SHAQ-STYLE MESSAGES
# -----------------------------

shaq_messages = [

    "Niko, stop talking. You're making my head hurt.",

    "Niko, that's a terrible take. Delete the message.",

    "Big fella, you need to calm down.",

    "Niko, you talk more than you play.",

    "Niko, I've seen enough. Somebody get this man off the GroupMe.",

    "Niko, you're doing TOO much, man.",

    "Niko, that message was straight CHEEKS. 💀",

    "Niko, I'm not even gonna lie. That was ridiculous.",

    "Stop it, Niko. Just stop it.",

    "Niko, you ain't built for this GroupMe life.",

    "Niko, what are you even doing, big fella?",

    "Niko, please relax. You're doing too much.",

    "Niko, I've been watching this chat and I don't know what's going on with you.",

    "Big fella, take a seat and think about what you just sent.",

    "Niko, that was NOT it, man.",

    "Niko, you gotta do better than that.",

    "Niko, I'm disappointed in you, big fella.",

    "Niko, nobody told you to start cooking. You burned the whole kitchen.",

    "Niko, I'm looking at this message like... what are we doing here?",

    "Big fella, you've had enough screen time for today.",

    "Niko, that's enough. Go sit down somewhere.",

    "Niko, I'm trying to understand you, but you ain't making it easy.",

    "Niko, you are doing everything except being quiet.",

    "Big fella, the GroupMe does not need all that.",

    "Niko, I don't know who told you that was a good idea, but they lied.",

    "Niko, you got the whole chat confused right now.",

    "Man, Niko, what kind of message was THAT?",

    "Niko, I'm gonna need you to relax before this gets out of hand.",

    "Niko, you talkin' real confident for somebody sending messages like that.",

    "Big fella, please put the phone down.",

    "Niko, I'm not mad. I'm just disappointed.",

    "Niko, you had one job: be quiet.",

    "Niko, this is why we can't have nice things.",

    "Big fella, I think you've done enough damage for today.",

    "Niko, you need to sit this possession out. 😂",

    "Niko, that's a shot you should NOT have taken.",

    "Niko, you're shooting 0-for-10 from the GroupMe tonight.",

    "Niko, pass the phone to somebody else, man.",

    "Niko, the GroupMe is not your personal podcast.",

    "Big fella, please stop yapping."

]

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        response = requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

        print("GroupMe response:", response.status_code)

    except Exception as error:
        print("Error sending GroupMe message:", error)

# -----------------------------
# WEBHOOK
# -----------------------------

@app.route("/", methods=["POST"])
def webhook():

    global message_count

    data = request.json

    if not data:
        return "ok", 200

    # Ignore bot messages
    if data.get("sender_type") == "bot":
        return "ok", 200

    name = data.get(
        "name",
        "Unknown"
    )

    name_lower = name.lower()

    message = data.get(
        "text",
        ""
    ).strip()

    message_lower = message.lower()

    # -----------------------------
    # ONLY WATCH NIKO OR ITACHI
    # -----------------------------

    if "niko" not in name_lower and "itachi" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT MESSAGES
    # -----------------------------

    message_count += 1

    print(
        f"Tracked message #{message_count} from {name}"
    )

    # -----------------------------
    # BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                f"Big fella, take a seat and think about what you just sent."
            )

            break

    # -----------------------------
    # EVERY 3RD MESSAGE
    # -----------------------------

    if message_count % 3 == 0:

        send_message(
            random.choice(shaq_messages)
        )

    return "ok", 200


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
