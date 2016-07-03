#SynonymGame.py
#By Michael W. Maher
#
#The Synonym Game presents random words and asks the player to guess the
#word's synonym.  Points are given for each correct answer.
#Scoring for each correct answer = 10 points + 1 point for each letter of the word and synonym
#Points are accumlated
#
#As a source of random words the program uses either a file called,
#   "list of common English words.txt" - DIFFICULT
#   OR
#   "list of top 1000 common English words.txt"
#The top 1000 common English words have been selected based on their use
#in the SAT and ACT tests.
#Synonyms are retrieved via the bighugelabs Thesaurus API.
#Thesaurus service provided by words.bighugelabs.com
#The dictionary API uses JSON.
#
import json
import urllib
import random
bighugelabskey = 'bighugelabskey.txt'
common_words = 'list of common English words.TXT'
top_1000_common_words = 'list of top 1000 common English words.TXT'
serviceurl = 'http://words.bighugelabs.com/api/2/'
synonym_list = []
#Check to see which list of words to play with
difficulty = raw_input('Do you prefer to play with the (1)Top 1000 words OR (2) Full dictionary')
if difficulty != '2':
    common_words = top_1000_common_words
#Load the common words file into a list
try:
   fh = open(common_words,'r')
except:
   print "File name not found:", common_words
   exit()
word_count = 0
word_list = list()
for word in fh:
    word_count = word_count + 1
    word = word.rstrip()
    word = word.lstrip('-')
    word_list.append(word)
print 'You are playing with a dictionary having', word_count, 'common English words. Good luck!'
print ''
print ''
#Load the dictionary key
try:
    fh = open(bighugelabskey, 'r')
except:
   print 'File name not found:', bighugelabskey
   print 'Please obtain your own key from: http://words.bighugelabs.com/getkey.php'
   print 'Store the key in a file called,', bighugelabskey, 'in the same directory as this Python program.'
   exit()
for key in fh:
    key = key.rstrip()
    continue
#Play the game
round = 10
plays = 0
score = 0
while plays < round:                                    #Play a round
    word_number = random.randint(1, word_count)         #Select a random number between 1 and the number of words in the list
    word = word_list[word_number]                       #The random word from the list
    url = serviceurl + key + '/' + word + '/json'       #Form the URL
    connection = urllib.urlopen(url)                    #Open the URL
    http_status_code = connection.getcode()             #Get the HTTP status code
    if http_status_code == 404:
        connection.close()                               #Close the url
    else:
        data = connection.read()                         #Read the data
        connection.close()                               #Close the url
        js = json.loads(data)
        found = False
        parts_of_speech = js.keys()
        plays = plays + 1                           #Track the play
        print '-----------------------------------------------------'
        answer = raw_input(('What is the synonym for "' + word +'"? '))          #Prompt the player
        for part in parts_of_speech:
            if 'syn' in js[part]:
                for synonym in js[part]['syn']:
                        if (synonym.lower() == answer.lower()) & (word.lower() != answer.lower()):      #perform a caseless comparison
                            found = True
                            continue
                        else:
                            if (word.lower() != answer.lower()):
                                synonym_list.append(synonym)
        #Update the score and provide feedback
        if found == True:
            score = score + 10 + len(word) + len(answer)
            print 'Good job! Your score:', score
            found = False
        else:
            print 'Sorry,', answer, 'is not a synonym of', word, ' Zero points earned.'
            synonym_output = ''.strip()
            for synonym in synonym_list:
                synonym_output = synonym + ', ' + synonym_output
            synonym_output = synonym_output[:len(synonym_output)-2]
            print 'Synonyms: ', synonym_output
            synonym_list[:] = []

print '--------------------------------------'
print 'Thank you for playing the SynonymGame.'
print 'Number of synonyms evaluated:', plays
print 'Your score:', score
print '--------------------------------------'
