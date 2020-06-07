"""
    Filename: generate_numbers.py
    Description: Generate numbers for a particular club's lotto
    Author: Domhnall Boyle
    Maintained by: Domhnall Boyle
    Email: domhnallboyle@gmail.com
    Python Version: 3.6
"""
import argparse
import random

from find_numbers import scrape_numbers

MIN, MAX = 1, 32


def main(args):
    lotto_numbers = scrape_numbers(club_url=args.club_url)
    print('Numbers: ', lotto_numbers)
    num_lines = len(lotto_numbers)
    print('Number of lines: ', num_lines)

    common_numbers = []
    for i in range(MIN, MAX + 1):
        counter = 0
        for line in lotto_numbers:
            if i in line:
                counter += 1

        common_numbers.append([i, counter])

    common_numbers.sort(key=lambda x: x[1], reverse=True)
    common_numbers = common_numbers[:args.top_n]
    print('Common numbers: ', common_numbers)

    for i in range(args.num_lines):
        print(f'Line {i + 1}: ', end='')
        random_numbers = random.sample(common_numbers, args.num_numbers)
        print(random_numbers)

    # TODO: Check for numbers close to eachother e.g. 2, 3, 4

    common_pairings = []
    for i in range(MIN, MAX):
        for j in range(i + 1, MAX + 1):
            pairing = [i, j]
            counter = 0
            for line in lotto_numbers:
                if all(num in line for num in pairing):
                    counter += 1
    
            common_pairings.append([i, j, counter])
    
    common_pairings.sort(key=lambda x: x[2], reverse=True)
    print('Common pairings: ', common_pairings[:10])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('club_url', type=str)
    parser.add_argument('num_lines', type=int)
    parser.add_argument('--num_numbers', type=int, default=4)
    parser.add_argument('--top_n', type=int, default=10)

    main(parser.parse_args())
