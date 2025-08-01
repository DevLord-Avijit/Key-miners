import asyncio
import signal
import sys
import aiohttp
from core.github_scraper import run_full_scraper
from core.storage import save_results
from core.utils import log

fetched_matches = []
save_task = None  # reference to the background save coroutine


def handle_shutdown(signum, frame):
    log("🛑 Shutdown signal received. Saving progress...")
    if fetched_matches:
        save_results(fetched_matches)
        log(f"💾 Saved {len(fetched_matches)} results before exit.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


async def periodic_saver():
    """Saves fetched matches every 10 seconds."""
    while True:
        await asyncio.sleep(10)
        if fetched_matches:
            save_results(fetched_matches)
            log(f"💾 Auto-saved {len(fetched_matches)} results.")


async def main():
    global fetched_matches, save_task

    log("🚀 Starting API Miner...")

    # Start periodic save task
    save_task = asyncio.create_task(periodic_saver())

    try:
        fetched_matches = await run_full_scraper()

    except aiohttp.ClientConnectorError as e:
        log(f"🌐 Internet disconnected: {e}")
        save_results(fetched_matches)
        log(f"💾 Saved {len(fetched_matches)} results after net issue.")
        sys.exit(1)

    except Exception as e:
        log(f"❌ Unexpected error: {e}")
        save_results(fetched_matches)
        log(f"💾 Saved {len(fetched_matches)} results after error.")
        sys.exit(1)

    else:
        save_results(fetched_matches)
        log(f"✅ Mining completed. {len(fetched_matches)} secrets saved.")

    # Cancel the periodic save task after scraping completes
    save_task.cancel()
    try:
        await save_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        handle_shutdown(signal.SIGINT, None)
