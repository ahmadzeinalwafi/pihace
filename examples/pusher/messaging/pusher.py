from pihace.healthcheck import HealthCheck
from pihace.pusher.messaging import AMQPPusher

hc = HealthCheck(with_system=True, name="MyApp", version="1.0.0")
hc.register("example", lambda: True)

publisher = AMQPPusher(amqp_url="amqp://guest:guest@localhost:5672/", healthcheck=hc)
publisher.push()

publisher.push_forever_in_loop(interval=5)