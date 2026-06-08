# Sending Instructions

This workspace does not currently expose a Gmail connector, so outreach sending must use SMTP credentials or your own email tool.

## Approval Flow

1. Open `docs/backlinks/send-ready-outreach.csv`.
2. Change `approval_status` from `Needs approval` to `Approved` for only the rows you want to send.
3. Keep `send_status` as `Not sent`.
4. Run a dry-run first.

## Dry Run

```bash
python3 tools/send-backlink-outreach.py --limit 3
```

## Send With Gmail SMTP

Use a Gmail App Password, not your normal Gmail password.

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=465
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-gmail-app-password"
export SMTP_FROM_EMAIL="your-email@gmail.com"
export SMTP_FROM_NAME="Rekha"

python3 tools/send-backlink-outreach.py --send --limit 3 --delay 120
```

## Send With STARTTLS SMTP

```bash
export SMTP_HOST=smtp.example.com
export SMTP_PORT=587
export SMTP_USERNAME="your-login"
export SMTP_PASSWORD="your-password"
export SMTP_FROM_EMAIL="hello@namealigned.com"
export SMTP_FROM_NAME="Rekha"

python3 tools/send-backlink-outreach.py --send --starttls --limit 3 --delay 120
```

## Logs

Every dry-run or send is logged to:

`docs/backlinks/outreach-send-log.csv`

## Safety Rules

- Send 3-5 emails per day at first.
- Do not send rows marked `Do not send`, `Review first`, or `Needs manual verification`.
- Do not use paid dofollow link-insert sites for SEO.
- Do not follow up more than once unless they reply.
- Keep replies human and specific.
