import os


def is_in_file(word: str, file_path: str) -> bool:
    """ Check if word is in file with file_path """
    try:
        with open(file_path, encoding="utf-8") as file:
            if word.lower() in [w.lower() for w in file.read().split()]:
                return True
            else:
                return False
    except FileNotFoundError:
        raise FileNotFoundError("Failed to open file in file path:\n" + os.path.abspath(file_path))


def get_paths_for_word(search_word: str, search_dir: str) -> str:
    """ Recursive search for all paths to files containing 'search_word' from directory 'search_dir'. """
    all_paths = ""
    for file in os.listdir(search_dir + "/."):
        file_path = search_dir + "/" + file

        if os.path.isdir(file_path):
            # Rekursivt anrop för att kontrollera underliggande mappar
            all_paths += get_paths_for_word(search_word, file_path)

        elif file.endswith(".txt"):
            # Basfall: inga fler mappar, kontrollerar text-filens innehåll
            if is_in_file(search_word, file_path):
                all_paths += os.path.abspath(file_path) + "\n"
    return all_paths


def main():
    search_word = input("Skriv sökord: ")
    print(get_paths_for_word(search_word=search_word, search_dir="TestData").strip())


if __name__ == '__main__':
    main()
