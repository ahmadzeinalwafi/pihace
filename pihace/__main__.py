import argparse
import asyncio
import threading
from pihace.loader import load_healthcheck_from_yaml

def run_in_thread(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread

def main():
    parser = argparse.ArgumentParser(description="Run PIHACE HealthCheck")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    args = parser.parse_args()

    result = load_healthcheck_from_yaml(args.config)
    hc = result["healthcheck"]
    providers = result.get("providers", [])
    pushers = result.get("pushers", [])
    storages = result.get("storages", [])
    config = result.get("config", {})

    # Start providers (e.g., web, prometheus)
    for provider in providers:
        if hasattr(provider, "serve"):
            run_in_thread(provider.serve)
        elif hasattr(provider, "start"):
            run_in_thread(provider.start)

    # Start pusher threads
    for push_cfg, pusher in zip(config.get("pushers", []), pushers):
        interval = push_cfg.get("push_config", {}).get("interval", 60)
        if hasattr(pusher, "push_forever_in_loop"):
            run_in_thread(pusher.push_forever_in_loop, interval=interval)

    # Start storage threads
    for store_cfg, storage in zip(config.get("storages", []), storages):
        interval = store_cfg.get("store_config", {}).get("interval", 60)
        if hasattr(storage, "run_forever_in_loop"):
            run_in_thread(storage.run_forever_in_loop, interval=interval)

    # Keep main thread alive
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
