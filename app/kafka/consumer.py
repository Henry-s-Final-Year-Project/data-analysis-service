import json
import logging
import signal, sys
from kafka import KafkaConsumer
from app.config import settings
from app.triton_client import infer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def start_analysis_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_PREPROCESSED_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=settings.KAFKA_GROUP_ID,
    )

    # clean shutdown
    def shutdown(sig, frame):
        logger.info("Shutting down analysis consumer…")
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("Analysis service listening on %s …", settings.KAFKA_PREPROCESSED_TOPIC)
    for msg in consumer:
        logger.info("Received message: %s", msg.value["features"])
        features = msg.value["features"]
        record = {"features": features}
        raw_transaction = msg.value["original_transaction"]
        try:
            result = infer(record)
            logger.info("Inference result: %s", result)
            yield result, record, raw_transaction
        except Exception as e:
            logger.error("Inference error: %s", e)
