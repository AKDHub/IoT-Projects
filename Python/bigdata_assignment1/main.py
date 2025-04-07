import init_db
import get_quote
import add_quote
import redis

redis_connection = redis.Redis(
        host='localhost',
        port=6379,
        charset='utf-8',
        decode_responses=True
    )


def print_menu():
    print("Chose one of the following options:")
    print(
"""   [1] - Get a random quote!
   [2] - Add a quote!
   [3] - Search Quotes from author!
   [4] - Import Quote DB!
   [5] - Quit!""")


def main():
    not_quit = True
    print("Welcome to Quote Machine!!")
    print_menu()
    while not_quit:
        choice = input("")
        try:
            choice = int(choice)
        except ValueError:
            pass

        match choice:
            case 1:
                get_quote.get_rand_quote(redis_connection)
            case 2:
                add_quote.add_quote(redis_connection)
            case 3:
                author_name = input("Write authors name (parts of the name or full):\n")
                if len(author_name.strip()) > 0:
                    get_quote.get_author_quote(
                        redis_connection,
                        author_name=author_name
                    )
            case 4:
                init_db.init_redis(redis_connection)
            case 5:
                not_quit = False
                break
            case _:
                print("You have to choose a number in the menu!")

        input("Press [Enter] to get back to menu.\n")
        print_menu()

    print("Thank you for using Quote Machine!\nHave a nice day! Carpe Diem! Hope you've been enlightened!")


if __name__ == '__main__':
    main()
