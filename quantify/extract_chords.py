import os
import re


def extractChords(folder_path: str, output_path: str):
    """
    Traverses the folder structure and extracts chords names from files using the SALAMI-style structural annotations, as seen in the example below.

    ### Parameters
    1. folder_path : str 
        - The path for the top folder of the SALAMI-style annotations for songs.
    2. output_path : str
        - The path to the output file, where the chords will be written.

    ### Example
    For a file containing the line:

        "0.325079365	A, intro, | Eb:maj | F:min9 Bb:sus4(b7) | Eb:maj | Ab:min9 Db:9 | F#:min9 B:9 | E:min9 A:9/5 |, (synth"

    The output will be (without apostrophes):

        "Eb:maj F:min9 Bb:sus4(b7) Eb:maj Ab:min9 Db:9 F#:min9 B:9 E:min9 A:9/5"
    """
    with open(output_path, 'w') as chords:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)

                with open(full_path, 'r') as salami:
                    for line in salami:
                        search = [m.group() for m in re.finditer(
                            r"((?:[A-Z]|[a-z]|#)+:(?:[a-z]|\d)+)(?:(\(.+?\))*)(?:\/.?)*", line)]
                        if search:
                            chords.write(' '.join(search) + ' ')
                chords.write('\n')


def main():
    extractChords("data/McGill-Billboard-Salami", "quantify/chords.txt")


if __name__ == "__main__":
    main()
