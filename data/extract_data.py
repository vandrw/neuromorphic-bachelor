import os
import sys
import shutil
import argparse


def moveFiles(origin, dest, ext, prev, skip):
    new_name = ""
    # traverse root directory and its folders
    for root, _, files in os.walk(origin):
        for file_name in files:
            i = 0
            extension = file_name.split(".")[-1]
            if extension.lower() in ext:
                init_path = os.path.join(root, file_name)
                target_path = os.path.join(dest, file_name)

                if skip and os.path.exists(target_path):
                    print("[INFO] ' {} ' Found duplicate. Skipping.".format(file_name))
                    continue

                new_name = file_name
                if prev == 0:
                    while os.path.exists(target_path):
                        new_name = (
                            file_name.split(".")[0]
                            + "_Copy"
                            + str(i)
                            + "."
                            + file_name.split(".")[1]
                        )
                        i += 1
                        target_path = os.path.join(dest, new_name)

                else:
                    new_name = "_".join(root.split(os.sep)[-prev:]) + "_" + file_name

                target_path = os.path.join(dest, new_name)
                print("[INFO] Moving ' {} ' to  ' {} '".format(file_name, target_path))

                shutil.copy2(init_path, target_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--append",
        type=int,
        default=0,
        help="How many folder names should be appended to the destination file name. Useful when files have the same name, but placed in different folders.",
    )

    parser.add_argument(
        "-s",
        "--skip",
        action="store_true",
        default=False,
        help="Skip duplicate files when copying.",
    )

    parser.add_argument(
        "-y",
        action="store_true",
        default=False,
        help="Does not ask for user confirmation.",
    )

    parser.add_argument(
        dest="origin", type=str, help="The origin folder where the files are located."
    )
    parser.add_argument(
        dest="destination",
        type=str,
        help="The destination folder where the files will be moved to.",
    )
    parser.add_argument(
        dest="extension",
        type=str,
        nargs="+",
        help="The extension(s) of the files that you would like to extract.",
    )

    args = parser.parse_args()

    extension = args.extension
    origin = args.origin
    destination = args.destination
    append = args.append
    skip = args.skip
    skip_user = args.y

    if not (os.path.exists(origin)):
        print('"', origin, '" does not exist!')
        sys.exit()

    if not (os.path.exists(destination)):
        print('"', destination, '" does not exist! Creating it...')
        os.mkdir(destination)

    print(
        "The script will move all the {} files in {} to {}.".format(
            extension, origin, destination
        )
    )

    if not skip_user:
        ans = input("Do you wish to continue?[y/n] ")
        if not (ans == "y"):
            sys.exit()

    moveFiles(origin, destination, extension, append, skip)
