import redis
import main
import random
import textwrap
import init_db


def print_rand_quote(author: str, quote: str):
    wrapped_quote = textwrap.fill(quote, width=80)
    print(f"""
Random Quote! 
--------------
'{wrapped_quote}'
                            - {author}
""")


def print_quote(author: str, quote: str):
    wrapped_quote = textwrap.fill(quote, width=80)
    print(
f"""--------------
'{wrapped_quote}'
                            - {author}
""")


def get_author_quote(redis_connection: redis.Redis, author_name: str) -> dict:
    """
    Search for an authors quotes and print them.
    :param redis_connection: Redis instans connection
    :param author_name: Authors name to search for in database
    """
    quotes = redis_connection.json().get('quotes', f'$.[?(@.author=~"{author_name}")]')
    print(f"These are all quotes that matches '{author_name}':")
    for quote in quotes:
        print_quote(quote["author"], quote["quote"])
    print("--------------")


def get_rand_quote(redis_connection: redis.Redis):
    """
    Gets a random quote from the 'quotes' key in Redis database, and prints it to terminal.
    If key doesn't exist in database, user is asked to import quotes.
    :param redis_connection: Redis instans connection.
    """

    quotes_key = redis_connection.json().get('quotes', '$')
    if not quotes_key:
        print("Error: No quotes found in database!")
        choice = input("Import quotes to database [y]: ")
        choice = choice.strip().lower()
        if choice == "y":
            init_db.init_redis(redis_connection)
        else:
            print("If you don't import or add quotes to the DB. You can't get a quote!")
    else:
        rand_num = random.randint(0, redis_connection.json().arrlen('quotes', '$')[0]-1)
        qt = redis_connection.json().get('quotes', f'$[{rand_num}]')[0]
        author, quote = qt['author'], qt['quote']

        print_rand_quote(author=author, quote=quote)


if __name__ == '__main__':
    get_rand_quote(main.redis_connection)
