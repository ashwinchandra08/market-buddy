# Notices & third-party content

## Pokémon
Pokémon and Pokémon character names are trademarks of Nintendo, Creatures Inc. and GAME FREAK inc.
This project is **unofficial and not affiliated with or endorsed by** any of them.
No Pokémon artwork is stored in this repository. At build time the workflow downloads artwork
from the community-run [PokeAPI sprites](https://github.com/PokeAPI/sprites) repository for **personal,
non-commercial** use. If you fork this project, keep it that way, or swap in your own mascots
(an original fallback mascot is built in: `src/mascot.py`).

## Market data
Quotes come from Yahoo Finance through the unofficial [`yfinance`](https://github.com/ranaroussi/yfinance)
library. Yahoo's terms apply; the data may be delayed or inaccurate. **Nothing here is investment advice.**

## Binaries you add yourself (not distributed in this repo)
| Tool | License | Source |
|---|---|---|
| FBInk (`fbink`, optional) | GPL-3.0 | https://github.com/NiLuJe/FBInk |
| static curl (`curl`) | curl license (MIT-like) | https://github.com/moparisthebest/static-curl |
| CA bundle (`cacert.pem`) | MPL-2.0 (Mozilla data) | https://curl.se/docs/caextract.html |

## Fonts
The workflow installs DejaVu Sans (free Bitstream Vera / public-domain-style license) on the build machine.
