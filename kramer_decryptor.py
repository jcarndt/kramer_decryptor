import argparse
import binascii
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description="Decrypt a .pyc file that has been encrypted with Kramer encryption.")

    parser.add_argument(
        '-f', '--file',
        required=True,
        help='Path to the input file'
    )

    parser.add_argument(
        '-k', '--key',
        required=False,
        default=None,
        type=int,
        help='Key value to use for decrypting file (if known)'
    )

    return parser.parse_args()

class Kyrie(): #<- Class taken directly from Kramer encryptor

    def _dkyrie(text: str):
        r = ""
        for a in text:
            if a in strings:
                i = strings.index(a)+1
                if i >= len(strings):
                    i = 0
                a = strings[i]
            r += a
        return r

    def _encrypt(text: str, key: str = None):
        if type(key) == str:
            key = sum(ord(i) for i in key)
        t = [chr(ord(t)+key)if t != "\n" else "ζ" for t in text]
        return "".join(t)

    def _decrypt(text: str, key: str = None):
        if type(key) == str:
            key = sum(ord(i) for i in key)
        return "".join(chr(ord(t)-key) if t != "ζ" else "\n" for t in text)

class Key: #<- Class taken directly from Kramer encryptor

    def encrypt(e: str, key: str):
        e1 = Kyrie._ekyrie(e)
        return Kyrie._encrypt(e1, key=key)

    def decrypt(e: str, key: str):
        text = Kyrie._decrypt(e, key=key)
        return Kyrie._dkyrie(text)
    
python_indicators = {
    'keywords': {'import'} #<- Add more words as you see fit like 'def', 'str', 'int', 'set', 'list', 'dict'
    #'keywords': {'import', 'def', 'str', 'int'} <- Example
}

strings = "abcdefghijklmnopqrstuvwxyz0123456789"

def main():
    args = parse_arguments()

    file_path = args.file
    key = args.key

    if '\\' in file_path:
        file = file_path.split('\\')[-1]
    elif '/' in file_path:
        file = file_path.split('/')[-1]
    else:
        file = file_path

    #Open file
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    #Grab necessary encrypted strings from .pyc file
    pattern = r'ceb6.*ceb6\)'
    match = re.search(pattern,content)
    if match:
        result = match.group(0)

    #If key argument is provided
    if key is not None:
        print(f"Using key: {key}")
        content_split = result.split('/')

        _content_ = ""
        key = key

        #Decrypt content
        for item in content_split:
            try:
                unhexed = binascii.unhexlify(item).decode() #<- Unhexlify first
                _content_ += Key.decrypt(unhexed, key=key) #<- Send to decryptor
            except:
                pass

        #Create file name
        file = file + "_decrypted_" + str(key) + ".py.txt"
        print("DECRYPTED CONTENT: " + file)
        #Output _content_ to file
        with open(file, 'w', encoding='utf-8') as f:
            f.write(_content_)

    #If no key is provided
    else:
        print("**BRUTE FORCING KEY**")
        
        #Grab only beginning content, adjust as you see fit.
        first_600 = result[:600]
        content_split = first_600.split('/')

        #Begin brute forcing
        i = 3
        while i < 1000001:
            _content_ = ""

            for item in content_split:
                try:
                    unhexed = binascii.unhexlify(item).decode() #<- Unhexlify first
                    _content_ += Key.decrypt(unhexed, key=i) #<- Send to decryptor
                except:
                    pass
            for keyword in python_indicators['keywords']: #<- Check if likely a decrypted python script
                if keyword in _content_:
                    print("KEY: " + str(i) + "\r\nOUTPUT:\r\n" +_content_) #<- If so, print key used as well as output to verify
            i += 1

if __name__ == "__main__":
    main()