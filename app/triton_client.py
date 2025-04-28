import httpx
import json
import logging
from app.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def _post_json(url, payload):
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def infer(record: dict) -> dict:
    inputs = [
        {
            "name": "input",
            "shape": [1, len(record["features"])],
            "datatype": "FP32",
            "data": record["features"],
        }
    ]
    payload = {"inputs": inputs, "outputs": [{"name": "probabilities"}]}
    url = f"{settings.TRITON_URL}/v2/models/{settings.TRITON_MODEL}/versions/{settings.TRITON_MODEL_VER}/infer"

    try:
        logger.info(payload)
        r = httpx.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as exc:
        logger.error("Triton Server returned error!")
        logger.error(f"Status Code: {exc.response.status_code}")
        logger.error(f"Response Body: {exc.response.text}")
        raise  # re-raise to let your service handle it
