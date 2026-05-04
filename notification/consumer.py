from database import redis
import time

group = "notification-group"
streams = ["order_completed", "refund_order"]

for stream in streams:
    try:
        redis.xgroup_create(stream, group, mkstream=True)
    except Exception:
        print(f"Group already exists for stream {stream}!")

while True:
    try:
        results = redis.xreadgroup(
            group,
            "notification-consumer",
            {stream: ">" for stream in streams},
            count=1,
            block=5000,
        )

        if results:
            for stream_name, messages in results:
                for message_id, data in messages:
                    if stream_name == "order_completed":
                        order_id = data.get("pk", data.get("id", "?"))
                        print(
                            f"Obavestenje: Porudzbina {order_id} je uspesno kreirana i placena"
                        )
                    elif stream_name == "refund_order":
                        order_id = data.get("pk", data.get("id", "?"))
                        print(
                            f"Obavestenje: Porudzbina {order_id} je refundirana"
                        )

                    redis.xack(stream_name, group, message_id)
    except Exception as e:
        print(f"Notification consumer error: {e}")
        time.sleep(1)
