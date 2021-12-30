#!/usr/bin/python3

# scriptureOfTheDay.py - This program utilizes the random library to choose
# a random book from the Bible (King James Version), and selects
# a verse. Afterwards, it will then post the scripture on a resulting
# website in the given directory named "directory.txt" of your choosing.

import random
import os
import re
import pendulum

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
    # TODO: Change to the output directory in the public_html/pythonprojectwebsites
    content = '<link rel="stylesheet" href="css/output.css" type="text/css"/>'
    
    content += '<h1 id="program_header">Scripture Of The Day</h1>'

    content += '\n'

    current_date_eastern = pendulum.now('America/New_York').format('dddd, MMMM D, YYYY')

    current_time_eastern = pendulum.now('America/New_York').format('hh:mm:ss A')

    content += '<h2 id="updated_header">Last Time Updated: ' + str(current_date_eastern) + ' at ' + str(current_time_eastern) + ' EST</h2>'

    content += '<br />'
    
    content += '<a href="http://www.musimatic.xyz">BACK TO HOMEPAGE</a>'
    
    content += '<br />'

    content += '<br />'
    
    content += '<a href="https://git.musimatic.xyz/ScriptureOfTheDay/tree/">Source Code Link</a>'
    
    content += '<br />'

    content += '<br />'    

    content += '\n'

    content += '<h2 class="description_headers">This is a program that obtains a random verse from the King James Version of the Bible.</h2>'

    content += '<h3>Scripture For Today: </h3>'

    content += '<p>' + scripture_of_the_day + '</p>'

    print('content: %s' %(content))

    with open('/var/www/musimatic/pythonprojectwebsites/ScriptureOfTheDay/output.html', 'w') as f:
        f.write(content)

    f.close()

    
def main():
    book_choice = obtainBookChoice()
    scripture_file = runSystemCommand(book_choice)
    verse_list = obtainVerseList(scripture_file)
    random_verse = obtainRandomVerse(verse_list)
    scripture_of_the_day = obtainScriptureOfTheDay(book_choice, random_verse)
    createOutputWebpage(scripture_of_the_day)


if __name__ == '__main__':
    main()
