# Kindle side – Market Buddy (Paperwhite 3, FW 5.16.2.1.1)

## What you must add yourself (3 files)

Final layout on the Kindle (`/mnt/us` = the drive you see over USB):

```
extensions/
└── marketbuddy/
    ├── config.xml        ← from this repo
    ├── menu.json         ← from this repo
    ├── config.sh         ← from this repo (EDIT URL_BASE)
    ├── cacert.pem        ← YOU ADD (1)
    └── bin/
        ├── common.sh  dash.sh  start.sh  stop.sh  test_once.sh  selfcheck.sh   ← from this repo
        ├── curl          ← YOU ADD (2)
        └── fbink         ← YOU ADD (3)
```

| File | What it is | Why it's needed | Where to get it |
|---|---|---|---|
| `bin/fbink` | FBInk – tiny tool that draws images/text straight to the e-ink screen | Once the Kindle UI is stopped, nothing else can paint the PNG | https://github.com/NiLuJe/FBInk/releases – download the archive for **Kindle** devices and take the `fbink` binary. For a PW3 on 5.16.2.x I believe the non-"hf" (soft-float, "PW2 and later") Kindle build is the right one; "kindlehf" is for newer firmware. If one prints `not found` or `Illegal instruction`, try the other. If you have KOReader installed, check `koreader/` – it usually bundles a working `fbink` you can copy. |
| `bin/curl` | A **static** curl with modern TLS | The stock Kindle curl is old and usually can't complete an HTTPS handshake with GitHub Pages | https://github.com/moparisthebest/static-curl/releases – the `curl-armv7` asset (rename to `curl`). Static builds don't depend on the Kindle's libraries, so the float-ABI question doesn't apply. |
| `cacert.pem` | Mozilla's list of trusted certificate authorities | curl needs it to verify GitHub's certificate | https://curl.se/ca/cacert.pem (save as `cacert.pem`) |

Release asset names change over time – the above is the intent, not a promise about exact filenames.
These three files are deliberately **not** in the repo (different licenses, device-specific). They are git-ignored.

You do **not** need SSH/USBNetwork for the basics, but it makes debugging far easier.

## Install steps
1. Connect the Kindle by USB. Copy `kindle/marketbuddy/` to `extensions/marketbuddy/` on the Kindle.
2. Add the three files above.
3. Edit `config.sh`: set `URL_BASE="https://<your-github-username>.github.io/market-buddy"`.
4. Make sure the Kindle has your Wi-Fi saved. Eject, open **KUAL → Market Buddy**.
5. **1. Self-check** → then open `extensions/marketbuddy/marketbuddy.log` (via USB) and look for
   `GET .../meta.txt -> 200`, plus curl/fbink version lines. Fix anything marked MISSING.
6. **2. Test: paint once, then restore UI** – paints the dashboard for 20 s and brings the normal UI back.
7. **3. START dashboard** when you're happy.

## How to exit and go back to normal Kindle use
While the dashboard runs, the Kindle UI (and KUAL) is **stopped on purpose** so nothing overwrites the picture.

1. **Always works – reboot:** press and **hold the power button ~40 seconds** (until the screen flashes and the
   Kindle restarts). Your books, Wi-Fi and KUAL are untouched. The dashboard does **not** auto-start after a reboot.
2. **Over SSH (if you installed USBNetwork):** `touch /mnt/us/extensions/marketbuddy/STOP`.
   Within ~5 seconds the script restarts the Kindle UI by itself. (`bin/stop.sh` does the same thing.)
3. To bring the dashboard back later: KUAL → Market Buddy → **3. START**.

Tip: while testing, always use **2. Test** first – it restores the UI automatically.

## Troubleshooting
| Symptom | Likely cause |
|---|---|
| Self-check: `curl: (60)` / SSL error | `cacert.pem` missing, or the Kindle's clock is wrong |
| `GET ... -> 000` | Wi-Fi off/not saved, or wrong `URL_BASE` |
| `404` | GitHub Pages not enabled yet, or the workflow hasn't run successfully |
| Image paints rotated or offset | try `fbink` rotation flags (`--rota`) in `common.sh` `paint()` |
| `fbink: not found` / `Illegal instruction` | wrong FBInk build for this firmware – try the other Kindle build |
| Screen shows only "OFFLINE …" | 12 failed fetches in a row; check Wi-Fi/router |
