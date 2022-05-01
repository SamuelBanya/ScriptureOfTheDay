#!/usr/bin/python3

# scriptureOfTheDay.py - This program utilizes the random library to choose
# a random book from the Bible (King James Version), and selects
# a verse. Afterwards, it will then post the scripture on a resulting
# website in the given directory named "directory.txt" of your choosing.

import random
import os
import re
import pendulum
import shutil
from dotenv import load_dotenv
from pathlib import Path

# Global path variables
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
WEBSITE_PATH = os.getenv("WEBSITE_PATH")
print('WEBSITE_PATH: ' + str(WEBSITE_PATH))
WEBSITE_ADDRESS = os.getenv("WEBSITE_ADDRESS")
print('WEBSITE_ADDRESS: ' + str(WEBSITE_ADDRESS))
WEBSITE_FULL_ADDRESS = os.getenv("WEBSITE_FULL_ADDRESS")
print('WEBSITE_FULL_ADDRESS: ' + str(WEBSITE_FULL_ADDRESS))
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")
print('PROJECT_DIRECTORY: ' + str(PROJECT_DIRECTORY))

# Remove the "output.txt" file if it already exists to start fresh:
output_file = 'output.txt'
if os.path.isfile(output_file):
    os.remove(output_file)

book_list = [
    'Genesis',
    'Exodus',
    'Leviticus',
    'Numbers',
    'Deuteronomy',
    'Joshua',
    'Judges',
    'Ruth',
    '1 Samuel',
    '2 Samuel',
    '1 Kings',
    '2 Kings',
    '1 Chronicles',
    '2 Chronicles',
    'Ezra',
    'Nehemiah',
    'Esther',
    'Job',
    'Psalms',
    'Proverbs',
    'Ecclesiastes',
    'Song of Solomon',
    'Isaiah',
    'Jeremiah',
    'Lamentations',
    'Ezekiel',
    'Daniel',
    'Hosea',
    'Joel',
    'Amos',
    'Obadiah',
    'Jonah',
    'Micah',
    'Nahum',
    'Habakkuk',
    'Zephaniah',
    'Haggai',
    'Zechariah',
    'Malachi',
    'Matthew',
    'Mark',
    'Luke',
    'John',
    'The Acts',
    'Romans',
    '1 Corinthians',
    '2 Corinthians',
    'Galatians',
    'Ephesians',
    'Philippians',
    'Colossians',
    '1 Thessalonians',
    '2 Thessalonians',
    '1 Timothy',
    '2 Timothy',
    'Titus',
    'Philemon',
    'Hebrews',
    'James',
    '1 Peter',
    '2 Peter',
    '1 John',
    '2 John',
    '3 John',
    'Jude',
    'Revelation'
]


def copyOverCSS():
    css_file_path = str(WEBSITE_PATH + '/css/scriptureOfTheDay.css')
    print('css_file_path: ' + str(css_file_path))
    shutil.copyfile(str(PROJECT_DIRECTORY) + '/css/scriptureOfTheDay.css', css_file_path)


def obtainBookChoice():
    book_choice = random.choice(book_list)
    # print('Book: %s' %(book_choice))

    return book_choice


def runSystemCommand(book_choice):
    # This is if I want to store the result into a text file:
    os.chdir('/tmp/')
    system_command = str('./kjv ' + book_choice + ' >> output.txt')
    # system_command = str('./kjv ' + book_choice)

    # Remove the output file if it already exists:
    scripture_file = 'output.txt'

    if os.path.isfile(scripture_file):
        os.remove(scripture_file)

    os.system(system_command)

    return scripture_file


def obtainVerseList(scripture_file):
    os.chdir('/tmp/')
    with open(scripture_file, 'r') as f:
        scripture_data = f.readlines()
        book_line = scripture_data[0]
        verse_list = []
        # print('\nChecking scripture_data: ')
        for i, line in enumerate(scripture_data):
            # Skip the initial book line:
            if i == 0:
                continue
            else:
                # print('i: %s' %(i))
                # print('line: %s' %(line))
                snippet = line[0:6]
                # print('snippet: %s' %(snippet))
                if snippet[1] == ':' and not snippet[0].isalpha():
                    verse = snippet[0:4]
                    verse_list.append(verse)
                elif snippet[2] == ':' and not snippet[0].isalpha():
                    verse = snippet[0:5]
                    verse_list.append(verse)
                elif snippet[3] == ':' and not snippet[0].isalpha():
                    verse = snippet[0:6]
                    verse_list.append(verse)
    # Close the file
    f.close()

    return verse_list

# print('\nChecking verse_list: ')
# for item in verse_list:
# print('item: %s' %(item))

def obtainRandomVerse(verse_list):
    random_verse = random.choice(verse_list)
    # print('random_verse: %s' %(random_verse))

    return random_verse


def obtainScriptureOfTheDay(book_choice, random_verse):
    os.chdir('/tmp/')
    scripture_text_file = 'scripture.txt'    
    # Remove the scripture_text_file so that there's a fresh new
    # file each time it is run:
    if os.path.isfile(scripture_text_file):
        os.remove(scripture_text_file)    
    
    scripture_choice = str(book_choice + ' ' + random_verse)
    # print('scripture_of_the_day: %s' %(scripture_of_the_day))

    # 'cd' into the correct directory:
    cd_command = 'cd /tmp'

    os.system(cd_command)
    
    system_command = str('./kjv ' + scripture_choice + ' >> scripture.txt')

    os.system(system_command)

    # print('scripture_choice: %s' %(scripture_choice))

    scripture_of_the_day = ''

    with open(scripture_text_file, 'r') as f:
        scripture_data = f.readlines()
        book_line = scripture_data[0]
        verse_list = []
        # print('\nChecking scripture_data: ')
        for i, line in enumerate(scripture_data):
            # print('line: %s' %(line))
            scripture_of_the_day += line

    # print('scripture_of_the_day: \n\n%s' %(scripture_of_the_day))
            
    return scripture_of_the_day


def createOutputWebpage(scripture_of_the_day):
    current_date_eastern = pendulum.now('America/New_York').format('dddd, MMMM D, YYYY')
    current_time_eastern = pendulum.now('America/New_York').format('hh:mm:ss A')
    with open('/var/www/musimatic/pythonprojectwebsites/ScriptureOfTheDay/output.html', 'w') as f:
        f.write('<html>')
        f.write('<head>')
        f.write('<link rel="stylesheet" href="css/scriptureOfTheDay.css" type="text/css"/>')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">')
        f.write('<title>Scripture Of The Day</title>')
        f.write('<meta charset="utf-8"/>')
        f.write('</head>')
        f.write('<body>')
        f.write('<div id="content">')
        f.write('<nav class="navbar navbar-expand-lg navbar-dark bg-dark" aria-label="Ninth navbar example">')
        f.write('<div class="container-xl">')
        f.write('<a class="navbar-brand" href="#">Scripture Of The Day</a>')
        f.write('<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample07XL" aria-controls="navbarsExample07XL" aria-expanded="false" aria-label="Toggle navigation">')
        f.write('<span class="navbar-toggler-icon"></span>')
        f.write('</button>')
        f.write('<div class="collapse navbar-collapse" id="navbarsExample07XL">')
        f.write('<ul class="navbar-nav me-auto mb-2 mb-lg-0">')
        f.write('<li class="nav-item">')
        f.write('<a class="nav-link active" aria-current="page" href="http://www.musimatic.xyz">Home</a>')
        f.write('</li>')
        f.write('</div>')
        f.write('</div>')
        f.write('</nav>')        
        f.write('<h1 id="program_header">Scripture Of The Day</h1>')
        f.write('\n')
        f.write('<h2 id="updated_header">Last Time Updated: ' + str(current_date_eastern) + ' at ' + str(current_time_eastern) + ' EST</h2>')
        f.write('<br />')
        f.write('<a class="btn btn-primary" href="https://github.com/SamuelBanya/ScriptureOfTheDay">Source Code Link</a>')
        f.write('<br />')
        f.write('<br />')
        f.write('\n')
        f.write('<p>This is a Python 3 program that obtains a random verse from the King James Version of the Bible.</p>')
        f.write('<br />')
        f.write('<br />')
        f.write('<h2>Scripture For Today: </h2>')
        f.write('<p>' + scripture_of_the_day + '</p>')
        f.write('</div>')
        f.write('</body>')
        f.write('</html>')
    f.close()

    
def main():
    copyOverCSS()
    book_choice = obtainBookChoice()
    scripture_file = runSystemCommand(book_choice)
    verse_list = obtainVerseList(scripture_file)
    random_verse = obtainRandomVerse(verse_list)
    scripture_of_the_day = obtainScriptureOfTheDay(book_choice, random_verse)
    createOutputWebpage(scripture_of_the_day)


if __name__ == '__main__':
    main()
