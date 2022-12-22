import os
import argparse
from pathlib import Path
from tqdm import tqdm


def get_all_files_in_folder_rec(path: str, file_ext: str):
    files = list(Path(path).rglob(f"*{file_ext}"))
    return files

def decrypt_all_in_foler(args):
    files = get_all_files_in_folder_rec(args.folder, args.ext)

    for f in tqdm(files):
        decrypt_file(f, delete_after=args.delete)

def decrypt_file(path_obj, delete_after: bool = False):
    new_filepath = os.path.join(path_obj.parent, path_obj.stem)
    os.system(f"gpg -o {new_filepath} -d {path_obj}")
    if delete_after:
        os.remove(path_obj)


def encrypt_all_in_folder(args):
    files = get_all_files_in_folder_rec(args.folder, args.ext)

    for f in tqdm(files):
        encrypt_file(f, recipient=args.email, ext=args.ext, delete_after=args.delete)

def encrypt_file(path_obj, recipient: str, ext: str, delete_after: bool = False):
    new_filepath = str(path_obj) + ext
    os.system(f"gpg -o {new_filepath} -a -r {recipient} -e {path_obj}")
    if delete_after:
        os.remove(path_obj)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="Email of recipient", type=str)
    parser.add_argument("-e", action="store_true", help="Encrypt operations", required=False)
    parser.add_argument("-d", action="store_true", help="Decrypt operations. Note: on using encryption and decryption at the same time, first - decryption.", required=False)
    parser.add_argument("--folder", help="Repository path.", type=str)
    parser.add_argument("--ext", help="GPG file extention. Default = .gpg", required=False, default=".gpg")
    parser.add_argument("--delete", action="store_true", help="Old files will be deleted")
    args = parser.parse_args()

    if (args.d):
        decrypt_all_in_foler(args)
    if (args.e):
        encrypt_all_in_folder(args)


if __name__ == "__main__":
    main()