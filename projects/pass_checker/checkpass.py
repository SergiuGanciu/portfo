import requests # type: ignore
import hashlib
import sys

def request_api_data(query_check):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_check)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error code: {res.status_code}. check api work!')
    
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5_char) 
    return get_password_leaks_count(response, tail)

def main(arg):
    file = open("pass_checker/pass_list.txt")
    for line in file:
        password = line.strip()
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times...')
        else:
            print(f'{password} was NOT FOUND!')
    return

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
