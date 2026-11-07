import os
from anthropic import Anthropic

def recibir_respuesta(mensaje_usuario):
    client = Anthropic(
        api_key="",
    )

    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": mensaje_usuario,
            }
        ],
        model="claude-sonnet-5-5",
    )

    respuesta = ""
    for block in message.content:
        if block.type == "text":
            respuesta += block.text

    return respuesta