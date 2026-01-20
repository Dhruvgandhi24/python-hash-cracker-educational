import getopt
import hashlib
import sys
import os
import time

"""
Educational Python Hash Cracker
Supports wordlist-based cracking and numeric brute force.
For learning purposes only.
"""

print("\nPython Hash-Cracker")


def info():
    print("\nInformation:")
    print("[*] Options:")
    print("[*] (-h) Hash")
    print("[*] (-t) Type [See supported hashes]")
    print("[*] (-w) Wordlist")
    print("[*] (-n) Numbers bruteforce")
    print("[*] (-v) Verbose [{WARNING} Slows cracking down!]\n")
    print("[*] Examples:")
    print("[>] python hash.py -h <hash> -t md5 -w wordlist.txt")
    print("[>] python hash.py -h <hash> -t sha256 -n -v")
    print("[*] Supported Hashes:")
    print("[>] md5, sha1, sha224, sha256, sha384, sha512")


def checkOS():
    if os.name == "nt":
        return "Windows"
    elif os.name == "posix":
        return "Linux / macOS"
    return "Unknown"


class HashCracker:

    def hashCrackWordlist(
        self,
        userHash,
        hashType,
        wordlist=None,
        verbose=False,
        bruteForce=False,
        max_number=10_000_000
    ):
        start = time.time()
        self.lineCount = 0

        # Select hashing algorithm
        if hashType == "md5":
            h = hashlib.md5
        elif hashType == "sha1":
            h = hashlib.sha1
        elif hashType == "sha224":
            h = hashlib.sha224
        elif hashType == "sha256":
            h = hashlib.sha256
        elif hashType == "sha384":
            h = hashlib.sha384
        elif hashType == "sha512":
            h = hashlib.sha512
        else:
            print(f"[-] Unsupported hash type: {hashType}")
            sys.exit(1)

        # Numeric brute-force mode
        if bruteForce:
            while self.lineCount <= max_number:
                attempt = str(self.lineCount)
                attempt_hash = h(attempt.encode()).hexdigest()

                if verbose:
                    sys.stdout.write("\rTrying: " + attempt)
                    sys.stdout.flush()

                if attempt_hash == userHash:
                    end = time.time()
                    print(f"\n[+] Hash is: {attempt}")
                    print(f"[*] Time: {round(end - start, 2)} seconds")
                    self.saveHash(attempt, attempt_hash)
                    return

                self.lineCount += 1

            print("\n[-] Brute force stopped (limit reached)")
            return

        # Wordlist mode
        try:
            with open(wordlist, "r", errors="ignore") as infile:
                for line in infile:
                    word = line.strip()
                    word_hash = h(word.encode()).hexdigest()

                    if verbose:
                        sys.stdout.write("\rTrying: " + word)
                        sys.stdout.flush()

                    if word_hash == userHash:
                        end = time.time()
                        print(f"\n[+] Hash is: {word}")
                        print(f"[*] Words tried: {self.lineCount}")
                        print(f"[*] Time: {round(end - start, 2)} seconds")
                        self.saveHash(word, word_hash)
                        return

                    self.lineCount += 1

            end = time.time()
            print("\n[-] Cracking Failed")
            print("[*] Reached end of wordlist")
            print(f"[*] Words tried: {self.lineCount}")
            print(f"[*] Time: {round(end - start, 2)} seconds")

        except IOError:
            print("[-] Could not open wordlist file")

    @staticmethod
    def saveHash(plaintext, hashvalue):
        with open("SavedHashes.txt", "a+") as f:
            f.write(f"{plaintext}:{hashvalue}\n")
        print("[*] Hash saved to SavedHashes.txt")


def main(argv):
    hashType = None
    userHash = None
    wordlist = None
    verbose = False
    numbersBruteForce = False

    print(f"[Running on {checkOS()}]\n")

    try:
        opts, _ = getopt.getopt(argv, "ih:t:w:nv")
    except getopt.GetoptError:
        print("[*] python hash.py -t <type> -h <hash> -w <wordlist>")
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-i":
            info()
            sys.exit()
        elif opt == "-t":
            hashType = arg.lower()
        elif opt == "-h":
            userHash = arg.lower()
        elif opt == "-w":
            wordlist = arg
        elif opt == "-n":
            numbersBruteForce = True
        elif opt == "-v":
            verbose = True

    # Argument validation
    if not hashType or not userHash:
        print("[*] python hash.py -t <type> -h <hash> [-w wordlist | -n]")
        sys.exit(1)

    if numbersBruteForce and wordlist:
        print("[-] Do not use -w with -n")
        sys.exit(1)

    print(f"[*] Hash: {userHash}")
    print(f"[*] Hash type: {hashType}")
    print(f"[*] Wordlist: {wordlist}")
    print("[+] Cracking...\n")

    cracker = HashCracker()
    cracker.hashCrackWordlist(
        userHash,
        hashType,
        wordlist=wordlist,
        verbose=verbose,
        bruteForce=numbersBruteForce
    )


if __name__ == "__main__":
    main(sys.argv[1:])
