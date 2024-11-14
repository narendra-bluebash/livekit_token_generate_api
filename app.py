import os
import json
import random
import uvicorn
from livekit import api
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from dotenv import load_dotenv
load_dotenv()

LIVEKIT_API_KEY_LOCAL = os.getenv('LIVEKIT_API_KEY_LOCAL')
LIVEKIT_API_SECRET_LOCAL = os.getenv('LIVEKIT_API_SECRET_LOCAL')
LIVEKIT_WEBSCOKET_URL_LOCAL = os.getenv('LIVEKIT_WEBSCOKET_URL_LOCAL')


LIVEKIT_API_KEY_STAGE = os.getenv('LIVEKIT_API_KEY_STAGE')
LIVEKIT_API_SECRET_STAGE = os.getenv('LIVEKIT_API_SECRET_STAGE')
LIVEKIT_WEBSCOKET_URL_STAGE = os.getenv('LIVEKIT_WEBSCOKET_URL_STAGE')

app = FastAPI()

@app.get('/generate_token_local')
async def generate_token(request: Request):
    agent_token = request.query_params.get("agent_token")

    room_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=7))
    if not LIVEKIT_API_KEY_LOCAL or not LIVEKIT_API_SECRET_LOCAL:
        raise ValueError("LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set")
    metadata = json.dumps({
        "agent_token": agent_token,
        "web_uuid": "web_uuid_local"
    })
    identity = "human_local"
    name = "kickcall_local_name"
    at = api.AccessToken(LIVEKIT_API_KEY_LOCAL, LIVEKIT_API_SECRET_LOCAL).with_identity(identity).with_name(name).with_metadata(metadata)
    at.with_grants(api.VideoGrants(room=room_name, room_join=True, can_publish=True, 
                            can_publish_data=True, can_subscribe=True, can_update_own_metadata=True))

    access_token = at.to_jwt()
    return JSONResponse(content={
        "accessToken": access_token,
        "url": LIVEKIT_WEBSCOKET_URL_LOCAL,
    })


@app.get('/generate_token_stage')
async def generate_token(request: Request):
    agent_token = request.query_params.get("agent_token")

    room_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=7))
    if not LIVEKIT_API_KEY_STAGE or not LIVEKIT_API_SECRET_STAGE:
        raise ValueError("LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set")
    metadata = json.dumps({
        "agent_token": agent_token,
        "web_uuid": "web_uuid_local"
    })
    identity = "human_stage"
    name = "kickcall_stage_name"
    at = api.AccessToken(LIVEKIT_API_KEY_STAGE, LIVEKIT_API_SECRET_STAGE).with_identity(identity).with_name(name).with_metadata(metadata)
    at.with_grants(api.VideoGrants(room=room_name, room_join=True, can_publish=True, 
                            can_publish_data=True, can_subscribe=True, can_update_own_metadata=True))

    access_token = at.to_jwt()
    return JSONResponse(content={
        "accessToken": access_token,
        "url": LIVEKIT_WEBSCOKET_URL_STAGE,
    })


if __name__ == "__main__":
    print(r"""
  _  __ ___   ___  _  __  ___     _     _     _            _     ___
 | |/ /|_ _| / __|| |/ / / __|   / \   | |   | |          / \   |_ _|
 | ' /  | | | |   | ' / | |     / _ \  | |   | |    __   / _ \   | |
 | . \  | | | |__ | . \ | |__  / ___ \ | |__ | |__ |__| / ___ \  | |
 |_|\_\|___| \___||_|\_\ \___|/_/   \_\|__ _||____|    /_/   \_\|___|
    """, flush=True)
    uvicorn.run(app, host="0.0.0.0", port=5003)