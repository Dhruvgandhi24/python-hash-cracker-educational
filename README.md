# Python Hash Cracker (Educational)

This project demonstrates basic hash cracking techniques in Python
using wordlists and numeric brute force.

## Features
- Supports MD5, SHA1, SHA256, SHA384, SHA512
- Wordlist-based cracking
- Numeric brute-force mode
- Verbose output option

## Usage

Wordlist:
python hash.py -t md5 -h <hash> -w wordlist.txt

Numeric brute force:
python hash.py -t md5 -h <hash> -n

## Disclaimer
This project is for educational purposes only.
It is not intended for real-world password cracking.
