from user_agents import parse
from typing import Dict


def parse_user_agent(user_agent: str) -> Dict:
    """
    Parse user agent string and extract device information.
    """
    ua = parse(user_agent)
    return {
        "device_type": get_device_type(ua),
        "browser": ua.browser.family,
        "os": ua.os.family,
        "is_bot": ua.is_bot,
    }


def get_device_type(ua) -> str:
    """
    Determine device type from user agent.
    """
    if ua.is_mobile:
        return "mobile"
    elif ua.is_tablet:
        return "tablet"
    elif ua.is_pc:
        return "desktop"
    return "other"
