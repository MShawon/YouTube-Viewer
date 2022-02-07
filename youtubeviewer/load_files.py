import hashlib

from .colors import bcolors


def load_url():
    print(bcolors.WARNING + 'Loading urls...' + bcolors.ENDC)

    with open('urls.txt', encoding="utf-8") as fh:
        links = [x.strip() for x in fh if x.strip() != '']

    print(bcolors.OKGREEN +
          f'{len(links)} url loaded from urls.txt' + bcolors.ENDC)

    return links


def load_search():
    print(bcolors.WARNING + 'Loading queries...' + bcolors.ENDC)

    with open('search.txt', encoding="utf-8") as fh:
        search = [[y.strip() for y in x.strip().split('::::')]
                  for x in fh if x.strip() != '' and '::::' in x]

    print(bcolors.OKGREEN +
          f'{len(search)} query loaded from search.txt' + bcolors.ENDC)

    return search


def get_hash(path):
    with open(path, "rb") as f:
        current_hash = hashlib.md5(f.read()).hexdigest()
    
    return current_hash
