<h1 align="center">The Swedish Twitter Bot</h1>

<a href="https://twitter.com/TheSwedishBot">
    <p align="center"><img src="assets/icon_round.png" width=200px height=auto></p>
</a><br>

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]

## Introduction

_Hej!_ I am the [**Swedish Twitter Bot**][TWITTER]!
I *retweet* hourly under `#Sweden` and `#Sverige` on **Twitter**! 🇸🇪 <br>
I'm also a **Discord Bot** with multiple functions! 🤖

## About me

<!-- - 🌐 | [**Website**](https://michalspano.github.io/the-swedish-bot/) currently deprecated --> 

- 🔧 | [**Documentation**](https://github.com/michalspano/the-swedish-bot)
- 📩 | [**Report issues**](https://github.com/michalspano/the-swedish-bot/issues)

## Details

[**Twitter Profile**][TWITTER] -
[**Tweets Database**][GS] -
[**Add to your server**][ADD] 🤖 <br>

The __website__ is currently __deprecated__ and will be __replaced__ with a __new one__ in the future. The __documentation__ is __available__ on the __GitHub__ repository. For troubleshooting, __report__ any __issues__ on the __GitHub__ repository.

\*__Packages__ used: `gspread`, `tweepy`, `discord.py`, `Flask`.

## Bot commands

- Use any of the **commands** with the *default bot prefix* (abbreviation **DBP**): `--` 
  - or *mention* `@The Swedish Twitter Bot`.

- Use the *command prefix or command aliases* (abbreviation **CP**).

**Note**: different operators in a single command are stylized with a space.

### 📶 Status command

- Invoke aliases: `Status`, `status` or `st`
- Syntax: `DBP CP` `count: int = 100`
- The `count` parameter is optional and defaults to 100 - the number of tweets to be parsed in the response
- Reports __current trends__ about the __database__ and the latency (ping) status

### ⏬ Load command

- Invoke aliases: `Load`, `load`, `l`
- __Default syntax__: `DBP CP operator n k`; `operator: str = None`, `n: int = 5`, `k: float = 5.0` [operator, $n$, $k$ are *optional values*; their *type* and *default value* is specified]
- **Primitive load**: `CBP CD` - loads the _latest_ submission in an embedded text message
- **Complex load**: Corresponding to *Default syntax*; `operator` prefix `recent` or `r`;
 `n` specifies the *number of retrieved tweets*\*, `k` specifies their *input interval* (i.e. delay)

  - E.g., `--load recent 10 2` - loads 10 recent tweets and displays them with a 2 sec. delay

\*The __maximum__ number of tweet entries is **20**! This is due to the limitations of the API.

### ℹ️ Help command

- Invoke aliases: `Help`, `help`, `h`
- Syntax: `DBP CP`
- Reports possible guidance and information about the bot

## 📩 Socials

[@TheSwedishBot][TWITTER] | [@michalspano][GITHUB]

<!-- hyperlinks -->
[TWITTER]: https://twitter.com/TheSwedishBot
[GS]: https://docs.google.com/spreadsheets/d/1Y8az4H5XGhBtKizaz6atYyhMCUeVif2c7-hUXNEtlhw/edit?usp=sharing
[ADD]: https://discord.com/api/oauth2/authorize?client_id=860479686156353556&permissions=2148005952&scope=bot
[GITHUB]: https://github.com/michalspano

<!-- shields -->
[contributors-shield]: https://img.shields.io/github/contributors/michalspano/the-swedish-bot.svg?style=for-the-badge
[contributors-url]: https://github.com/michalspano/the-swedish-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/michalspano/the-swedish-bot.svg?style=for-the-badge
[forks-url]: https://github.com/michalspano/the-swedish-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/michalspano/the-swedish-bot.svg?style=for-the-badge
[stars-url]: https://github.com/michalspano/the-swedish-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/michalspano/the-swedish-bot.svg?style=for-the-badge
[issues-url]: https://github.com/michalspano/the-swedish-bot/issues
[license-shield]: https://img.shields.io/github/license/michalspano/the-swedish-bot.svg?style=for-the-badge
[license-url]: https://github.com/michalspano/the-swedish-bot/blob/main/LICENSE.md
