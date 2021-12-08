# Pronunciation Download
Download and play all pronunciations of an English word, showing phonetics.
This script crowls [www.oxfordlearnersdictionaries.com](https://www.oxfordlearnersdictionaries.com) website.

## Usage
Run python script in this way:
```
usage: pronunciation_download.py [-h] [--web] word

Download pronunciation of an English word.

positional arguments:
  word        an English word

optional arguments:
  -h, --help  show this help message and exit
  --web       to open the webpage on the browser
```

## Example
For example, to check out the word "increase" you should run:
```
python pronunciation_download.py increase
```
then the output will be like:
```
increase  (verb) /ɪnˈkriːs/
increase  (noun) /ˈɪŋkriːs/
```
and it will store `increase (noun).mp3` and `increase (verb).mp3` files and play each one.

## Run
This script is tested on Ubuntu 20.04. First, install pre-requirement for `PyGObject`
package as mentioned [here](https://github.com/pygobject/pycairo/issues/89):
```
sudo apt install libcairo2-dev libgirepository1.0-dev
```

Then install python packages:
```
pip install -r requirements.txt
```
Now you can use the script like the example above.
