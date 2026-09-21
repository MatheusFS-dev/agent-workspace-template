#!/usr/bin/env python3
"""Render shared Claude Code and Antigravity CLI statusline telemetry."""

import json
import os
import sys


def _value(payload, *keys):
    """Return a nested mapping value, or None when any key is unavailable."""
    value = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _percentage(value):
    """Format a non-negative numeric percentage without a fractional part."""
    try:
        return "{0}%".format(int(float(value) + 0.5))
    except (TypeError, ValueError):
        return "—"


def _quota_percentage(bucket):
    """Return used quota from a CLI rate-limit or remaining-quota bucket."""
    used_percentage = _value(bucket, "used_percentage")
    if used_percentage is not None:
        return _percentage(used_percentage)
    remaining_fraction = _value(bucket, "remaining_fraction")
    try:
        return _percentage((1 - float(remaining_fraction)) * 100)
    except (TypeError, ValueError):
        return "—"


def _agy_quota(payload, period):
    """Return AGY quota usage for the requested five-hour or weekly period."""
    quota = _value(payload, "quota")
    if not isinstance(quota, dict):
        return "—"

    period_markers = {
        "five_hour": ("five", "5h", "hour"),
        "seven_day": ("week", "seven", "7d"),
    }
    for name, bucket in quota.items():
        if any(marker in str(name).lower() for marker in period_markers[period]):
            return _quota_percentage(bucket)

    buckets = []
    for bucket in quota.values():
        try:
            reset_seconds = float(_value(bucket, "reset_in_seconds"))
        except (TypeError, ValueError):
            continue
        buckets.append((reset_seconds, bucket))
    if period == "five_hour":
        candidates = [bucket for seconds, bucket in buckets if seconds <= 8 * 60 * 60]
        return _quota_percentage(candidates[0]) if candidates else "—"
    candidates = [bucket for seconds, bucket in buckets if seconds > 8 * 60 * 60]
    return _quota_percentage(max(candidates, key=lambda item: _value(item, "reset_in_seconds"))) if candidates else "—"


def format_statusline(payload):
    """Format model, effort, folder, context, and rate-limit telemetry.

    Args:
        payload: Statusline JSON emitted by Claude Code or Antigravity CLI.

    Returns:
        str: One compact, human-readable statusline.
    """
    model = _value(payload, "model", "display_name") or _value(payload, "model", "id") or "—"
    effort = _value(payload, "effort", "level")
    if effort:
        model = "{0} ({1})".format(model, effort)

    directory = _value(payload, "workspace", "current_dir") or _value(payload, "cwd")
    folder = os.path.basename(directory.rstrip(os.sep)) if directory else "—"
    context = _percentage(_value(payload, "context_window", "used_percentage"))

    five_hour = _quota_percentage(_value(payload, "rate_limits", "five_hour"))
    weekly = _quota_percentage(_value(payload, "rate_limits", "seven_day"))
    if five_hour == "—":
        five_hour = _agy_quota(payload, "five_hour")
    if weekly == "—":
        weekly = _agy_quota(payload, "seven_day")

    return "{0} · {1} · ctx {2} · 5H {3} · week {4}".format(
        model, folder, context, five_hour, weekly
    )


def main():
    """Read one JSON payload from standard input and print its statusline."""
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        payload = {}
    sys.stdout.write(format_statusline(payload) + "\n")


if __name__ == "__main__":
    main()
