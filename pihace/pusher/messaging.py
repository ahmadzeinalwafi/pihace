# -*- coding: utf-8 -*-
"""pihace.pusher.messaging: AMQP publisher to RabbitMQ for pushing health check results."""

import json
import pika
import traceback
from pihace.healthcheck import HealthCheck

class AMQPPusher:
    """
    Publishes health check results to a RabbitMQ queue using AMQP.

    Args:
        amqp_url (str): AMQP connection URL (e.g., 'amqp://user:pass@host:port/').
        queue_name (str): Name of the queue to publish messages to. Defaults to 'pihace.healthcheck'.

    Attributes:
        amqp_url (str): The AMQP connection URL.
        queue_name (str): The name of the target queue.
    """
    def __init__(self, amqp_url: str, healthcheck: HealthCheck, queue_name: str = "pihace.healthcheck"):
        """
        Initializes the AMQPPusher with the provided AMQP URL and queue name.
        """
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.healthcheck = healthcheck

        # Parse the AMQP URL
        parameters = pika.URLParameters(self.amqp_url)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Ensure the queue exists
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def push(self):
        """
        Sends a health check result payload to the configured RabbitMQ queue.

        Args:
            data (dict[str, Any]): The health check result dictionary, typically produced by `HealthCheck.check()`.

        Returns:
            bool: True if the message was successfully published.
            tuple[bool, str]: (False, error message) if an exception occurred.
        """
        try:
            result = self.healthcheck.check(output="dict")
            message = json.dumps(result)

            # Publish the message
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2  # make message persistent
                ),
            )

            self.connection.close()
            return True

        except Exception as e:
            return False, traceback.format_exc()
