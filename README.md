# **The Swedish Twitter Bot**
[Initial comment]: <> (Custom contributions buttons + custom url mentions)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
![Icon](Assets/swedish_twitter_bot_final.jpg)

## Introduction

Hej! I am the **Swedish Twitter Bot!**
I *retweet* hourly under #Sweden and #Sverige on **Twitter**! 🇸🇪  <br>
I'm also a **Discord Bot** with multiple functions! <br>
- [__📊 Explore my docs__](https://github.com/michalspano/The-Swedish-Bot) 
- [__📩 Report an issue__](https://github.com/michalspano/The-Swedish-Bot/issues)
- [__🌐 Website__](https://michalspano.github.io/The-Swedish-Bot/)

## Details

[*Twitter Profile*][TWITTER]
[*Google Spreadsheet*][GS]
[*Add to your server!*][ADD] <br>
#### Created via `gspread`, `tweepy`, `discord.py`, `flask`.

## Bot commands

Use any of my *commands* by the *default bot prefix* (abbreviation **DBP**) `--` or just *mention me* `@The Swedish Twitter Bot`;
use my *command prefix or command aliases* (abbreviation **CP**).

```*NOTE*: different operators in a single command are stylized with a space```

### 📶 **Status command**
___
- Invoke aliases: `Status`, `status` or `s`
- Syntax: `DBP CP`
- Reports current trends about the database and the latency (ping) status

### ⏬ **Load command**
___
- Invoke aliases: `Load`, `load`, `l`
- Default syntax: `DBP CP operator n k`; `operator: str = None`, `n: int = 5`, `k: float = 5.0` [operator, n, k are *optional values*; their *type* and *default value* is specified]
- **Primitive load**: `CBP CD` - loads the latest submission in an embedded text message
- **Complex load**: Corresponding to *Default syntax*; `operator` prefix `recent` or `r`;
- `n` specifies the *number of retrieved tweets*; `k` specifies their *input interval* (i.e. delay)
- E.g., `--load recent 10 2` - loads 10 recent tweets and displays them with a 2 sec. delay

### ℹ️ **Help command**
___
- Invoke aliases: `Help`, `help`, `h`
- Syntax: `DBP CP`
- Reports possible guidance and appropriate information

### 📩 Socials
___
> [@TheSwedishBot][TWITTER]
> [@michalspano][GITHUB]

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[TWITTER]: (https://twitter.com/TheSwedishBot)
[GS]: https://docs.google.com/spreadsheets/d/1Y8az4H5XGhBtKizaz6atYyhMCUeVif2c7-hUXNEtlhw/edit?usp=sharing
[ADD]: https://discord.com/api/oauth2/authorize?client_id=860479686156353556&permissions=2148005952&scope=bot
[GITHUB]: https://github.com/michalspano

[contributors-shield]: https://img.shields.io/github/contributors/michalspano/The-Swedish-Bot.svg?style=for-the-badge
[contributors-url]: https://github.com/michalspano/The-Swedish-Bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/michalspano/The-Swedish-Bot.svg?style=for-the-badge
[forks-url]: https://github.com/michalspano/The-Swedish-Bot/network/members
[stars-shield]: https://img.shields.io/github/stars/michalspano/The-Swedish-Bot.svg?style=for-the-badge
[stars-url]: https://github.com/michalspano/The-Swedish-Bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/michalspano/The-Swedish-Bot.svg?style=for-the-badge
[issues-url]: https://github.com/michalspano/The-Swedish-Bot/issues
[license-shield]: https://img.shields.io/github/license/michalspano/The-Swedish-Bot.svg?style=for-the-badge
[license-url]: https://github.com/michalspano/The-Swedish-Bot/blob/main/LICENSE.md
