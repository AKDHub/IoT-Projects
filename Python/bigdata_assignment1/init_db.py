import json
import redis.exceptions
import requests
import main

QUOTE_LIMIT = 100


def init_redis(redis_connection: redis.Redis):
    """
    Initiates a quote database to Redis key 'quotes', using an imported json-string.
    :param redis_connection:
    """
    print("Downloading quotes.....")
    response = requests.get(f"https://dummyjson.com/quotes?limit={QUOTE_LIMIT}")

    if redis_connection.ping():
        print("Database connection established")
        quotes = json.loads(response.text)

        try:
            quotes_exists = redis_connection.json().get('quotes')
        except redis.exceptions.ResponseError as e:
            quotes_exists = False

        if quotes_exists:
            print("There's already quotes in the database. Do you want to delete existing ones?")
            match input("[y/n]: ").strip().lower():
                case "y":
                    redis_connection.json().set('quotes', '$', quotes["quotes"])
                    print("DB Init successfull!")
                case "n":
                    redis_connection.json().arrappend('quotes', '$', *quotes["quotes"])
                    print("Quotes appended to existing database!")
                case _:
                    print("Wrong command. No action taken.")
        else:
            redis_connection.json().set('quotes', '$', quotes["quotes"])
            print("DB Init successfull!")
    else:
        print("Couldn't connect to database.")

    print(f"{redis_connection.json().arrlen('quotes', '$')[0]} quotes exists in the DB.")


if __name__ == '__main__':
    init_redis(main.redis_connection)




