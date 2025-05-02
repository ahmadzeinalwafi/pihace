import yaml
from pathlib import Path
from pihace.healthcheck import HealthCheck

from pihace.plugins.http import HTTP
from pihace.plugins.influxdb import InfluxDB
from pihace.plugins.mongodb import MongoDB
from pihace.plugins.mysql import MySQL
from pihace.plugins.elasticsearch import ElasticSearch
from pihace.providers.prometheus import PrometheusProvider
from pihace.providers.web import WebProvider
from pihace.pusher.elasticsearch import ElasticSearchPusher
from pihace.pusher.messaging import AMQPPusher
from pihace.storage.mongodb import MongoStorage
from pihace.system_info import get_system_info

CHECKER_MAP = {
    "http": HTTP,
    "influxdb": InfluxDB,
    "mongodb": MongoDB,
    "mysql": MySQL,
    "elasticsearch": ElasticSearch,
    "system": lambda: get_system_info(),
}

PROVIDER_MAP = {
    "prometheus_provider": PrometheusProvider,
    "web_provider": WebProvider,
}

PUSHER_MAP = {
    "elasticsearch_pusher": ElasticSearchPusher,
    "amqp_pusher": AMQPPusher,
}

STORAGE_MAP = {
    "mongodb_storage": MongoStorage,
}


def load_healthcheck_from_yaml(path: str | Path) -> dict:
    """
    Loads a HealthCheck instance and configured plugin instances from a YAML config file.

    Args:
        path (str | Path): Path to the config.yaml

    Returns:
        dict: {
            "healthcheck": HealthCheck,
            "providers": list,
            "pushers": list,
            "storages": list
        }
    """
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    component_name = config.get("instance", {}).get("name", "unknown")
    component_version = config.get("instance", {}).get("version", "0.0.1")
    with_system = config.get("instance", {}).get("with_system", False)
    providers = []
    pushers = []
    storages = []

    hc = HealthCheck(with_system=with_system, name=component_name, version=component_version)

    # --- Load health checks ---
    for entry in config.get("plugins", []):
        name = entry["name"].replace(" ", "_")
        type_ = entry["type"]
        checker_class = CHECKER_MAP.get(type_)

        if not checker_class:
            raise ValueError(f"Unknown checker type: {type_}")

        checker_config = entry.get("config", {})

        if callable(checker_class) and not isinstance(checker_class, type):
            hc.register(name, lambda: checker_class())
        else:
            hc.register(name, checker_class(**checker_config))

    # --- Load providers ---
    for entry in config.get("providers", []):
        type_ = entry["type"]
        config_ = entry.get("config", {})
        cls = PROVIDER_MAP.get(type_)
        if not cls:
            raise ValueError(f"Unknown provider type: {type_}")
        providers.append(cls(hc, **config_))

    # --- Load pushers ---
    for entry in config.get("pushers", []):
        type_ = entry["type"]
        config_ = entry.get("config", {})
        cls = PUSHER_MAP.get(type_)
        if not cls:
            raise ValueError(f"Unknown pusher type: {type_}")
        pushers.append(cls(hc, **config_))

    # --- Load storages ---
    for entry in config.get("storages", []):
        type_ = entry["type"]
        config_ = entry.get("config", {})
        cls = STORAGE_MAP.get(type_)
        if not cls:
            raise ValueError(f"Unknown storage type: {type_}")
        storages.append(cls(**config_))

    return {
        "healthcheck": hc,
        "providers": providers,
        "pushers": pushers,
        "storages": storages,
        "config": config,
    }
