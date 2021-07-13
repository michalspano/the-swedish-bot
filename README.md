# **The Swedish Twitter Bot**
***
![Icon](Assets/swedish_twitter_bot_final.jpg) <br>

## Introduction
***
Hej! I am the **Swedish Twitter Bot!**
I *retweet* hourly under #Sweden and #Sverige on **Twitter**! 🇸🇪 
I'm also a **Discord Bot** with multiple functions!

## Details
***
> [*Twitter Profile*](https://twitter.com/TheSwedishBot), [*Google Spreadsheet*](https://docs.google.com/spreadsheets/d/1Y8az4H5XGhBtKizaz6atYyhMCUeVif2c7-hUXNEtlhw/edit?usp=sharing), [*Add to your server*](https://discord.com/api/oauth2/authorize?client_id=860479686156353556&permissions=2148005952&scope=bot) <br>
> Created via `gspread`, `tweepy`, `discord.py`, `flask`.

## Bot commands
***
Use any of my *commands* by the *default bot prefix* (abbreviation **DBP**) `--` or just *mention me* `@The Swedish Twitter Bot`;
command prefix or command aliases (abbreviation **CP**).

```*NOTE*: different operators in a single command are stylized with a space```

### 📶 | **Status command**
> Invoke aliases: `Status`, `status` or `s`
> Syntax: `DBP CP`
> Reports current trends about the database and the latency (ping) status

### ⏬ | **Load command**
> Invoke aliases: `Load`, `load`, `l`
> Default syntax: `DBP CP operator n k`; `operator: str = None`, `n: int = 5`, `k: float = 5.0` [operator, n, k are *optional values*; their *type* and *default value* is specified]
> **Primitive load**: `CBP CD` - loads the latest submission in an embedded text message
> **Complex load**: Corresponding to *Default syntax*; `operator` prefix `recent` or `r`;
> `n` specifies the *number of retrieved tweets*; `k` specifies their *input interval* (i.e. delay)
> E.g., `--load recent 10 2` - loads 10 recent tweets and displays them with a 2 sec. delay

### ℹ️ | **Help command**
> Invoke aliases: `Help`, `help`, `h`
> Syntax: `DBP CP`
> Reports possible guidance and appropriate information

### 📩 | Socials
> [@TheSwedishBot](https://twitter.com/TheSwedishBot)
> [@michalspano](https://github.com/michalspano)
