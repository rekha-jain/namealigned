#!/usr/bin/env python3
"""
Controlled mail-merge sender for NameAligned backlink outreach.

Safety defaults:
- Dry-run unless --send is passed.
- Sends only rows with approval_status=Approved and send_status=Not sent.
- Rate-limited with a delay between messages.
- Writes an append-only CSV log.
- Does not scrape or discover emails.
"""

import argparse
import csv
import os
import smtplib
import ssl
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "docs" / "backlinks" / "send-ready-outreach.csv"
DEFAULT_LOG = ROOT / "docs" / "backlinks" / "outreach-send-log.csv"


def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_rows(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_log(path, row):
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "timestamp_utc",
            "site",
            "to_email",
            "subject",
            "mode",
            "result",
            "message",
        ])
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def build_message(row, from_email, from_name, reply_to):
    msg = EmailMessage()
    msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
    msg["To"] = row["to_email"]
    msg["Subject"] = row["subject"]
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(row["body"].replace("\\n", "\n"))
    return msg


def send_message(msg, host, port, username, password, starttls):
    context = ssl.create_default_context()
    if starttls:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as server:
            server.login(username, password)
            server.send_message(msg)


def main():
    parser = argparse.ArgumentParser(description="Send approved backlink outreach emails.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="CSV input file")
    parser.add_argument("--log", default=str(DEFAULT_LOG), help="CSV send log")
    parser.add_argument("--send", action="store_true", help="Actually send email. Omit for dry-run.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum messages per run")
    parser.add_argument("--delay", type=int, default=90, help="Delay in seconds between sends")
    parser.add_argument("--from-name", default=os.environ.get("SMTP_FROM_NAME", "Rekha"), help="Sender display name")
    parser.add_argument("--reply-to", default=os.environ.get("SMTP_REPLY_TO", ""), help="Optional Reply-To")
    parser.add_argument("--starttls", action="store_true", help="Use STARTTLS instead of SMTP_SSL")
    parser.add_argument("--password-stdin", action="store_true", help="Read SMTP password from stdin instead of SMTP_PASSWORD")
    args = parser.parse_args()

    input_path = Path(args.input)
    log_path = Path(args.log)
    rows = load_rows(input_path)
    fieldnames = list(rows[0].keys()) if rows else []
    eligible = [
        row for row in rows
        if row.get("approval_status") == "Approved" and row.get("send_status") == "Not sent"
    ][:args.limit]

    if not eligible:
        print("No eligible rows. Mark approval_status=Approved and send_status=Not sent first.")
        return

    if args.send:
        host = require_env("SMTP_HOST")
        port = int(require_env("SMTP_PORT"))
        username = require_env("SMTP_USERNAME")
        if args.password_stdin:
            password = input("SMTP password: ").strip()
            if not password:
                raise SystemExit("No SMTP password provided on stdin")
        else:
            password = require_env("SMTP_PASSWORD")
        from_email = os.environ.get("SMTP_FROM_EMAIL", username)
    else:
        host = port = username = password = None
        from_email = os.environ.get("SMTP_FROM_EMAIL", "dry-run@example.com")

    mode = "send" if args.send else "dry-run"
    print(f"{mode}: {len(eligible)} eligible message(s)")

    for index, row in enumerate(eligible, start=1):
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        msg = build_message(row, from_email, args.from_name, args.reply_to)
        try:
            if args.send:
                send_message(msg, host, port, username, password, args.starttls)
                row["send_status"] = "Sent"
            print(f"[{index}/{len(eligible)}] {mode}: {row['site']} <{row['to_email']}>")
            append_log(log_path, {
                "timestamp_utc": timestamp,
                "site": row["site"],
                "to_email": row["to_email"],
                "subject": row["subject"],
                "mode": mode,
                "result": "ok",
                "message": "",
            })
        except Exception as exc:
            append_log(log_path, {
                "timestamp_utc": timestamp,
                "site": row.get("site", ""),
                "to_email": row.get("to_email", ""),
                "subject": row.get("subject", ""),
                "mode": mode,
                "result": "error",
                "message": str(exc),
            })
            raise

        if args.send and index < len(eligible):
            time.sleep(args.delay)

    if args.send:
        save_rows(input_path, rows, fieldnames)


if __name__ == "__main__":
    main()
