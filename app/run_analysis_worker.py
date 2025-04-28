from app.kafka.consumer import start_analysis_consumer
from app.kafka.producer import send_alert


def main():
    for prediction, record in start_analysis_consumer():
        send_alert(prediction, record)


if __name__ == "__main__":
    main()
