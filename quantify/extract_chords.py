import os
import re


def main():
    with open("quantify/chords.txt", 'w') as chords:
        for root, _, files in os.walk("data/McGill-Billboard-Salami"):
            for file in files:
                file_path = os.path.join(root, file)
                chords.write('\n#' + root +'\n')

                with open(file_path, 'r') as salami:
                    for line in salami:
                        search = [m.group() for m in re.finditer(r"((?:[A-Z]|[a-z]|#)+:(?:[a-z]|\d)+)(?:(\(.+?\))*)(?:\/.?)*", line)]
                        if search:
                            chords.write(' '.join(search) + '\n')

if __name__ == "__main__":
    main()
