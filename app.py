import os
import json
import random
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

LIVEKIT_API_KEY_PROD = os.getenv('LIVEKIT_API_KEY_PROD')
LIVEKIT_API_SECRET_PROD = os.getenv('LIVEKIT_API_SECRET_PROD')
LIVEKIT_WEBSCOKET_URL_PROD = os.getenv('LIVEKIT_WEBSCOKET_URL_PROD')

app = FastAPI()

@app.get('/generate_token_local')
async def generate_token(request: Request):
    agent_token = request.query_params.get("agent_token")

    room_name = 'local-'+''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
    if not LIVEKIT_API_KEY_LOCAL or not LIVEKIT_API_SECRET_LOCAL:
        raise ValueError("LIVEKIT_API_KEY_LOCAL and LIVEKIT_API_SECRET_LOCAL must be set")
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

    room_name = 'stage-'+''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=7))
    if not LIVEKIT_API_KEY_STAGE or not LIVEKIT_API_SECRET_STAGE:
        raise ValueError("LIVEKIT_API_KEY_STAGE and LIVEKIT_API_SECRET_STAGE must be set")
    metadata = json.dumps({
        "agent_token": agent_token,
        "web_uuid": "web_uuid_stage"
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


@app.get('/generate_token_prod')
async def generate_token(request: Request):
    agent_token = request.query_params.get("agent_token")

    room_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=7))
    if not LIVEKIT_API_KEY_PROD or not LIVEKIT_API_SECRET_PROD:
        raise ValueError("LIVEKIT_API_KEY_PROD and LIVEKIT_API_SECRET_PROD must be set")
    metadata = json.dumps({
        "agent_token": agent_token,
        "web_uuid": "web_uuid_prod"
    })
    identity = "human_prod"
    name = "kickcall_prod_name"
    at = api.AccessToken(LIVEKIT_API_KEY_PROD, LIVEKIT_API_SECRET_PROD).with_identity(identity).with_name(name).with_metadata(metadata)
    at.with_grants(api.VideoGrants(room=room_name, room_join=True, can_publish=True, 
                            can_publish_data=True, can_subscribe=True, can_update_own_metadata=True))

    access_token = at.to_jwt()
    return JSONResponse(content={
        "accessToken": access_token,
        "url": LIVEKIT_WEBSCOKET_URL_PROD,
    })