import json
from kafka import KafkaProducer
from app.config import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def send_alert(prediction: dict, record: dict):
    message = {"transaction": record, "prediction": prediction}
    producer.send(settings.KAFKA_ALERTS_TOPIC, message)
    producer.flush()
