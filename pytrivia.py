import html
import random

import click
import requests

import db_record

mult_choice = ["a", "b", "c", "d"]

url = "https://opentdb.com/api.php?amount=10&type=multiple"

req = requests.get(url).json()

q_set = req["results"]

questions = [html.unescape(resp["question"]) for resp in q_set]
corr_answer = [html.unescape(resp["correct_answer"]) for resp in q_set]

poss_answers = [list(map(html.unescape, q_set[resp]["incorrect_answers"])) + [corr_answer[resp]] for resp in range(len(q_set))]
for answers in poss_answers:
    random.shuffle(answers)

poss_selctions = [{k:v for (k, v) in zip(mult_choice, lst)} for lst in poss_answers]

connection = db_record.create_connection("pt.sqlite")
db_record.execute_query(connection, db_record.create_users_table)

def answer_check(poss_choices: dict, correct: str):
    valid_ans = False
    while not valid_ans:
        user_select = input()
        if user_select == "quit":
            return "q"
        elif user_select not in mult_choice:
            click.echo("Invalid answer")
            continue
        elif user_select in mult_choice:
            user_answer = poss_choices[user_select]
            if user_answer == correct:
                click.echo("Correct! :D")
                return True
            click.echo("Incorrect :(")
            return False
        valid_ans = True

if __name__ == "__main__":
    results = []
    user_name = input("What is your name?\n")
    click.echo(f"\n{user_name}, this is a {len(questions)} question multiple choice quiz. "
               "Make a selection from 'a', 'b', 'c', 'd' when prompted. \n"
               "Type 'quit' to stop at any time. Good luck!")
    for i, question in enumerate(questions):
        click.echo()
        click.echo(f"{question}\n{poss_selctions[i]}")
        get_answer = answer_check(poss_selctions[i], corr_answer[i])
        if get_answer == "q":
            break
        else:
            results.append(get_answer)

    final_score = sum(results)

    create_scores = f"""
    INSERT INTO
        users (name, score)
    VALUES
        ('{user_name}', '{final_score}')
    """

    db_record.execute_query(connection, create_scores)

    select_users = """
    SELECT * FROM (
        SELECT * FROM users ORDER BY id DESC LIMIT 5)
    ORDER BY id ASC;
    """

    users_scores = db_record.execute_read_query(connection, select_users)

    click.echo(f"Final score: {final_score}/{len(questions)}")

    for user in users_scores:
        click.echo(user)