Hej! I am the **Swedish Twitter Bot!**
I *retweet* hourly under #Sweden and #Sverige on **Twitter** 🇸🇪

Use any of my *commands* by the *default bot prefix* (abbreviation **DBP**) `--` or just *mention me*; command prefix or command aliases (abbreviation **CP**).

*NOTE*: different operators in a single command are stylized with a space

📶 | **Status command**
> Invoke aliases: `Status`, `status` or `st`
> Syntax: `DBP CP` `count: int = 100`
> The `count` parameter is optional and defaults to 100 - the number of tweets to be parsed in the response
> Reports current trends about the database and the latency (ping) status

⏬ | **Load command**
> Invoke aliases: `Load`, `load`, `l`
> Default syntax: `DBP CP operator n k`; `operator: str = None`, `n: int = 5`, `k: float = 5.0` [operator, n, k are *optional values*; their *type* and *default value* is specified]
> **Primitive load**: `CBP CD` - loads the latest submission in an embedded text message
> **Complex load**: Corresponding to *Default syntax*; `operator` prefix `recent` or `r`;
> `n` specifies the *number of retrieved tweets*; `k` specifies their *input interval* (i.e. delay)
> E.g., `--load recent 10 2` - loads 10 recent tweets and displays them with a 2 sec. delay
\*The __maximum__ number of tweet entries is **20**!

ℹ️ | **Help command**
> Invoke aliases: `Help`, `help`, `h`
> Syntax: `DBP CP`
> Reports possible guidance and appropriate information

[@TheSwedishBot](https://twitter.com/TheSwedishBot)
[@michalspano](https://github.com/michalspano)