from typing import Literal

PluginType = Literal["http", "influxdb", "mongodb", "mysql", "elasticsearch", "system"]
PusherType = Literal["elasticsearch_pusher", "amqp_pusher"]
StorageType = Literal["mongodb_storage"]
ProviderType = Literal["web_provider", "prometheus_provider"]