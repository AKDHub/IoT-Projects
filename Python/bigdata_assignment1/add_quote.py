import redis
import main
import get_quote


def add_quote(redis_connection: redis.Redis):
    """
    Asks user for quote and adds it to 'quotes' key in redis database.
    :param redis_connection: Redis instance connection.
    """
    quote = input("Write your quote:\n")
    author = input("Who's the author of the quote?:\n")

    if redis_connection.ping():
        try:
            quotes_exists = redis_connection.json().get('quotes')
        except redis.exceptions.ResponseError as e:
            quotes_exists = False

        if quotes_exists:
            quotes_len = redis_connection.json().arrlen('quotes', '$')[0]
            redis_connection.json().arrappend('quotes', '$', {"id": quotes_len+1, "quote": quote, "author": author})
        else:
            redis_connection.json().set('quotes', '$', [{"id": 1, "quote": quote, "author": author}])
        print("Successfully added quote: ")
        get_quote.print_quote(author=author, quote=quote)
        print("--------------\nto database!")
    else:
        print("Couldn't connect to DB.")


if __name__ == '__main__':
    add_quote(main.redis_connection)


