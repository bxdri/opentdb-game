import requests
import json
import sqlite3

question_amount = int(input("How many questions? (Max. 50): "))
answered_correctly = 0

conn = sqlite3.connect('data_db.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS data( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
question VARCHAR(100),
answered_correctly VARCHAR(30))
''')  ## ქმნის database-ს სადაც შეინახება დასმული შეკითხვები, და გაეცა თუ არა მომხმარებელმა პასუხი სწორად

response = requests.get(f"https://opentdb.com/api.php?amount={question_amount}")
if response.status_code != 200:
    print("Something went wrong, please try again")

content = response.json()

file = open("content.json", "w")
file.write(json.dumps(content, indent=4)) ## წერს მონაცემებს .json ფორმატში
file.close()

import random
while question_amount != 0:
    print(f'{content["results"][question_amount - 1]["question"]} Answers:')
    correct_answer = content["results"][question_amount-1]["correct_answer"]
    incorrect_answers = content["results"][question_amount - 1]["incorrect_answers"]

    answers = [correct_answer]
    for i in incorrect_answers:
        answers.append(i)

    for i in range(len(answers)): ## რანდომულად პრინტავს პასუხებს, რათა პირველი პასუხი ყოველთვის სწორი არ იყოს
        random_index = random.randrange(len(answers))
        print(answers[random_index])
        del answers[random_index]

    user_answers = input("Enter answer: ")
    if user_answers.upper() == correct_answer.upper():
        print("Correct!")
        answered_correctly += 1
        c.execute(f"INSERT INTO data (question, answered_correctly) VALUES (?, ?)", (content['results'][question_amount - 1]['question'], "Yes"))
    else:
        print(f"Incorrect, the correct answer was {correct_answer}")
        c.execute(f"INSERT INTO data (question, answered_correctly) VALUES (?, ?)", (content['results'][question_amount - 1]['question'], "No"))

    question_amount -= 1

print(f"You got {answered_correctly} question(s) correct")

conn.commit()
conn.close()
