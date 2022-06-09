"""
MIT License

Copyright (c) 2021-2022 MShawon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import hashlib
from random import choices

from .colors import *


def load_url():
    print(bcolors.WARNING + 'Loading urls...' + bcolors.ENDC)

    with open('urls.txt', encoding="utf-8") as fh:
        links = [x.strip() for x in fh if x.strip() != '']

    print(bcolors.OKGREEN +
          f'{len(links)} url loaded from urls.txt' + bcolors.ENDC)

    links = choices(links, k=len(links)*3) + links

    return links


def load_search():
    print(bcolors.WARNING + 'Loading queries...' + bcolors.ENDC)

    with open('search.txt', encoding="utf-8") as fh:
        search = [[y.strip() for y in x.strip().split('::::')]
                  for x in fh if x.strip() != '' and '::::' in x]

    print(bcolors.OKGREEN +
          f'{len(search)} query loaded from search.txt' + bcolors.ENDC)

    search = choices(search, k=len(search)*3) + search
    
    return search


def get_hash(path):
    with open(path, "rb") as f:
        current_hash = hashlib.md5(f.read()).hexdigest()

    return current_hash
