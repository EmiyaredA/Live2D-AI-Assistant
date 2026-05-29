from __future__ import annotations

import re
import uuid
from typing import Any, Callable

from backend.core.audio_payload import prepare_audio_payload
from backend.core.service_context import ServiceContext

WebSocketSend = Callable[[dict[str, Any]], Any]

_SENTENCE_SPLIT = re.compile(r"(?<=[。！？!?\.])\s*")


async def process_single_conversation(
    context: ServiceContext,
    websocket_send: WebSocketSend,
    user_input: str,
    history_uid: str,
) -> str:
    context.history_uid = history_uid
    full_response = ""

    async for output in context.agent_engine.chat(user_input):
        if output.done:
            full_response = output.display_text
            break
        display_text = output.display_text
        actions_dict = None
        if context.live2d_model:
            display_text, actions = context.live2d_model.extract_emotion(display_text)
            actions_dict = actions.to_dict()
        await websocket_send(
            {"type": "display-text", "text": display_text, "actions": actions_dict}
        )

    if not full_response:
        return ""

    sentences = [s for s in _SENTENCE_SPLIT.split(full_response) if s.strip()]
    if not sentences:
        sentences = [full_response]

    for idx, sentence in enumerate(sentences):
        clean_sentence = sentence.strip()
        if not clean_sentence:
            continue

        actions_dict = None
        if context.live2d_model:
            clean_sentence, actions = context.live2d_model.extract_emotion(clean_sentence)
            actions_dict = actions.to_dict()

        file_id = f"{history_uid}_{uuid.uuid4().hex[:8]}_{idx}"
        try:
            audio_path = await context.tts_engine.async_generate_audio(
                clean_sentence, file_id
            )
            payload = prepare_audio_payload(
                audio_path,
                display_text=clean_sentence,
                actions=actions_dict,
            )
        except Exception:
            payload = prepare_audio_payload(
                None,
                display_text=clean_sentence,
                actions=actions_dict,
            )
        await websocket_send(payload)

    await websocket_send({"type": "turn-complete", "text": full_response})
    return full_response
