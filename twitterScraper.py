#!/usr/local/bin/python3

import argparse
import searchForTwitterImages as sti

# import downloadUrlImage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get profile image URLs from Twitter.')
    parser.add_argument('-i', '--interactive',
                        dest='i',
                        action='store_true',
                        help='makes this program interactive where it will prompt the user for input')
    parser.add_argument('-s', '--search_terms',
                        dest='search',
                        nargs='+',
                        help='search terms upon which to query twitter')
    parser.add_argument('searchDefault', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.i:
        strIgnore = ''
        if args.search and len(args.search) > 0:
            strIgnore = ' Ignoring command line search criteria.'
        sti.searchForTwitterImages_interactive(strIgnore)
    else:
        print(f"Search terms: {args}")
        if args.search:
            sti.searchForTwitterImages(args.search)
        elif args.searchDefault:
            sti.searchForTwitterImages(args.searchDefault)
        else:
            print(f"No search terms given.  Switching to interactive mode.")
            sti.searchForTwitterImages_interactive()
