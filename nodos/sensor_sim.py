
import json
import os
import random
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("BROKER", "localhost")
PUERTO = 1883

PARCELA = os.getenv("PARCELA", "p01")
NODO = os.getenv("NODO", "n01")
INTERVALO = int(os.getenv("INTERVALO", "30"))

TOPICO = f"agrismart/{PARCELA}/{NODO}/telemetria"

cliente = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"sim-{PARCELA}-{NODO}"
)

cliente.connect(BROKER, PUERTO, 60)
cliente.loop_start()

humedad = 38.0

print("Sensor conectado al broker MQTT")
print("Tópico:", TOPICO)

try:
    while True:
        humedad = max(
            10,
            min(70, humedad + random.uniform(-1.5, 1.0))
        )

        lectura = {
            "ts": int(time.time()),
            "ph": round(random.gauss(6.4, 0.1), 2),
            "humedad": round(humedad, 1),
            "temperatura": round(random.gauss(14, 2), 1),
            "n": random.randint(30, 45),
            "p": random.randint(12, 20),
            "k": random.randint(110, 150)
        }

        resultado = cliente.publish(
            TOPICO,
            json.dumps(lectura),
            qos=1
        )

        resultado.wait_for_publish()

        print(TOPICO, lectura, flush=True)

        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print("Sensor detenido")

finally:
    cliente.loop_stop()
    cliente.disconnect()
