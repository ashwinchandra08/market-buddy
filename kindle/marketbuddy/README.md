# Kindle side – Market Buddy (Paperwhite 3, FW 5.16.2.1.1)

## What you must add yourself

Final layout on the Kindle (`/mnt/us` = the drive you see over USB):

```
(Kindle drive root)
├── documents/
├── koreader/                  ← untouched
└── extensions/
    └── marketbuddy/
        ├── config.xml         ← from this repo
        ├── menu.json          ← from this repo
        ├── config.sh          ← from this repo (EDIT URL_BASE)
        ├── cacert.pem         ← YOU ADD (required)
        └── bin/
            ├── common.sh  dash.sh  start.sh  stop.sh  test_once.sh  selfcheck.sh   ← from this repo
            ├── curl           ← YOU ADD (required)
            └── fbink          ← optional (see below)
```

| File | Required? | What it is | Where to get it |
|---|---|---|---|
| `bin/curl` | **Yes** | A static curl with modern TLS. The stock Kindle curl usually can't complete an HTTPS handshake with GitHub. | https://github.com/moparisthebest/static-curl/releases → download **`curl-armhf`** (current releases) and rename it to `curl`. Verified: static ARMv7-A hard-float ELF using VFPv3/NEON. If it dies with `Illegal instruction`, try `curl-armv7` from the older v8.11.0 release. Optionally check it against `sha256sum.txt` on the same page. |
| `cacert.pem` | **Yes** | Mozilla's list of trusted certificate authorities, so curl can verify GitHub's certificate. | https://curl.se/ca/cacert.pem – save the file as `cacert.pem`. |
| `bin/fbink` | No | A screen-drawing tool. Without it the scripts use the Kindle's built-in `eips -f -g` to show the PNG. | FBInk's GitHub page has **no release downloads**. Binaries are shared in NiLuJe's MobileRead thread (https://www.mobileread.com/forums/showthread.php?t=299620) and bundled in his packages; you may also find one inside your KOReader folder. Only bother if `eips` paints the image badly (wrong size, rotated, ghosting). |

These files are deliberately **not** in the repo (different licenses, device-specific); they are git-ignored.
You do **not** need SSH/USBNetwork, but it makes debugging much easier.

## Install steps
1. Connect the Kindle by USB. Copy `kindle/marketbuddy/` to `extensions/marketbuddy/` on the Kindle.
2. Add `bin/curl` and `cacert.pem` (and optionally `bin/fbink`).
3. Edit `config.sh`: set `URL_BASE="https://<your-github-username>.github.io/market-buddy"`.
4. Make sure the Kindle has your Wi-Fi saved. Eject, open **KUAL → Market Buddy**.
5. **1. Self-check** → then open `extensions/marketbuddy/marketbuddy.log` (via USB) and look for
   `GET .../meta.txt -> 200`, plus the curl version line. Fix anything marked MISSING.
6. **2. Test: paint once, then restore UI** – paints the dashboard for 20 s and brings the normal UI back.
7. **3. START dashboard** when you're happy.


## No KUAL? Use `;log runme` instead

If KUAL won't install, you can still run everything through the jailbreak hotfix's `;log runme` command
(forum reports show it launching KOReader on a PW3 this way). Differences from the KUAL flow:

1. Copy `kindle/RUNME.sh` to the **root** of the Kindle (next to `documents`).
2. Copy `kindle/marketbuddy/` to `extensions/marketbuddy/` (create `extensions` yourself if it doesn't exist).
3. The file `extensions/marketbuddy/ACTION` decides what `RUNME.sh` does. Put exactly one word in it:
   `selfcheck`, then `test`, then `start`. Edit it over USB between runs.
4. Eject, then type `;log runme` in the home-screen search bar and press Enter.
5. Read `extensions/marketbuddy/marketbuddy.log` over USB after each run.

Do **not** confuse this with the very old boot-time `RUNME.sh` trick for Kindle 4/Touch (it required a special
`data.tar.gz` and has bricked devices). This is only the on-demand `;log runme` command of the modern hotfix.

If the log says `/dev/fb0: NOT writable` or `framework stop` fails with *permission denied*, scripts started this way
are running without root. Search for a "RUNME.sh elevate framework user to root" script (mentioned by KOReader users with
"cannot open framebuffer" errors) and run it once first.

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
| `curl: Illegal instruction` / `not found` | wrong curl build – try `curl-armv7` from the v8.11.0 release |
| Image looks wrong with `eips` | add a matching `fbink` build and the scripts will use it automatically |
| Screen shows only "OFFLINE …" | 12 failed fetches in a row; check Wi-Fi/router |
