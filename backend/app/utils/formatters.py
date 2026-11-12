from __future__ import annotations


def humanize_seconds(value: int | None) -> str:
    if value is None:
        return "0m"
    total_seconds = max(0, int(value))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def normalize_domain(domain: str) -> str:
    return domain.lower().replace("http://", "").replace("https://", "").split("/", 1)[0]
