"""Start this checkout as DadBotTest.

The live DadBot uses a different Discord application. This launcher reads
config.yaml and refuses to connect when that file is the live bot, so a
local run cannot kick the production session.
"""

import os
import re
import runpy
import sys
from pathlib import Path

LIVE_APPLICATION_ID = "483747956479229962"
TEST_APPLICATION_ID = "850471747358687242"


def application_id(path: Path) -> str:
    match = re.search(r'^application_id:\s*"([^"]+)"', path.read_text(encoding="utf-8"), re.M)
    if not match:
        sys.exit(f"{path.name} has no application_id.")
    return match.group(1)


def main() -> None:
    root = Path(__file__).resolve().parent
    config_path = root / "config.yaml"
    if not config_path.exists():
        sys.exit("config.yaml is missing. Copy config template.yaml and fill in the DadBotTest token.")

    app_id = application_id(config_path)
    if app_id == LIVE_APPLICATION_ID:
        sys.exit(
            "config.yaml is the live DadBot. Refusing to start it from this machine. "
            "Point config.yaml at DadBotTest first."
        )
    if app_id != TEST_APPLICATION_ID:
        sys.exit(
            f"config.yaml application_id {app_id} is not DadBotTest ({TEST_APPLICATION_ID})."
        )

    os.environ["DADBOT_TEST"] = "1"
    os.chdir(root)
    print("Starting DadBotTest. Use your testing server, then run /apod.")
    runpy.run_path(str(root / "bot.py"), run_name="__main__")


if __name__ == "__main__":
    main()
