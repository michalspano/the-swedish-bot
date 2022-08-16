from datetime import datetime as dt

def time_module() -> str:
    time_now = dt.now().strftime("%d. %m. (%A) - %H:%M:%S")
    return time_now


def logger(tweet_id: str) -> None:
    LOG_MSG: str = f"{time_module()} - https://twitter.com/anyuser/status/{tweet_id}\n"
    print(LOG_MSG, end='')
    with open('../info.log', 'a') as log:
        log.write(LOG_MSG)


def format_row_data(buff: list) -> dict:
    ''' Strcuture of the value list:
    [0] - url;  [1] - data;  [2] - tweet; 
    [3] - user; [4] - likes; [5] - retweets;
    [6] - lang '''
    return {
        "url": buff[0],
        "date": buff[1],
        "data": buff[2],
        "user": buff[3],
        "likes": buff[4],
        "retweets": buff[5],
        "lang": buff[-1]
    }
