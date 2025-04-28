import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    KAFKA_PREPROCESSED_TOPIC = os.getenv("KAFKA_PREPROCESSED_TOPIC")
    KAFKA_ALERTS_TOPIC = os.getenv("KAFKA_ALERTS_TOPIC")
    KAFKA_GROUP_ID = os.getenv("KAFKA_ANALYSIS_GROUP_ID")
    TRITON_URL = os.getenv("TRITON_URL")
    TRITON_MODEL = os.getenv("TRITON_MODEL_NAME")
    TRITON_MODEL_VER = os.getenv("TRITON_MODEL_VERSION")


settings = Settings()
