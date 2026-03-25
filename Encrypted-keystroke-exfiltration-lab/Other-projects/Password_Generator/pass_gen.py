import argparse
from zxcvbn import zxcvbn
import itertools

#--------------PASSWORD ANALYSIS-----------------
def analyze_password(password):
    result = zxcvbn(password)

    print("\n Password Strength Analysis")
    print("Score (0-4):", result['score'])
    print("Crack Time:", result['crack_times_display']['offline_fast_hashing_1e10_per_second'])
    print("Feedback:", result['feedback'])

#-----------------LEETSPEAK----------------------
leet_map = {
    'a':['a', '@', '4'],
    'e':['e', '3'],
    'i':['i', '1'],
    'o':['o', '0'],
    's':['s', '$', '5']
    }

def generate_leet(word):
    variations = []

    for char in word:
        if char.lower() in leet_map:
            variations.append(leet_map[char.lower()])
        else:
            variations.append([char])


    return [''.join(p) for p in itertools.product(*variations)]


# ------------------ WORDLIST GENERATOR ------------------
def generate_wordlist(inputs):
    wordlist = set()

    # basic words
    for word in inputs:
        wordlist.add(word)
        wordlist.add(word.lower())
        wordlist.add(word.capitalize())

        # leetspeak
        wordlist.update(generate_leet(word))

    # combinations
    for combo in itertools.permutations(inputs, 2):
        combined = ''.join(combo)
        wordlist.add(combined)

    # append years
    years = ['2023', '2024', '2025', '123', '1234']

    final_list = set()

    for word in wordlist:
        final_list.add(word)
        for y in years:
            final_list.add(word + y)

    return final_list

# ------------------ SAVE ------------------
def save_wordlist(wordlist, filename="wordlist.txt"):
    with open(filename, "w") as f:
        for word in wordlist:
            f.write(word + "\n")

    print(f"\n Wordlist saved as {filename}")
    print(f"Total words: {len(wordlist)}")

# ------------------ MAIN ------------------
def main():
    parser = argparse.ArgumentParser(description="Password Analyzer & Wordlist Generator")

    parser.add_argument("-p", "--password", help="Password to analyze")
    parser.add_argument("-i", "--inputs", nargs='+', help="Inputs for wordlist (name, pet, date)")
    parser.add_argument("-o", "--output", default="wordlist.txt", help="Output file")

    args = parser.parse_args()

    if args.password:
        analyze_password(args.password)

    if args.inputs:
        wl = generate_wordlist(args.inputs)
        save_wordlist(wl, args.output)

if __name__ == "__main__":
    main()
