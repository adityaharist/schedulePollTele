import requests
import json
import schedule
import time

def send_quiz(chat_id, question, options, correct_option_id):
    base_url = "https://api.telegram.org/bot7822122704:AAG53aitpT0LSvmGY0jfL9xBC15Dr9yBnxg/sendPoll"  # Replace with your actual bot token
    parameters = {
        "chat_id": chat_id,
        "question": question,
        "options": json.dumps(options),
        "is_anonymous": False,
        "type": "quiz",
        "correct_option_id": correct_option_id
    }
    try:
        resp = requests.get(base_url, data=parameters)
        resp.raise_for_status()  # Raise an exception for non-200 status codes
        print(f"Quiz sent successfully: {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending quiz: {e}")

def job():
    sent_quizzes = set()
    try:
        with open('sent_quizzes.json', 'r') as f:
            sent_quizzes.update(json.load(f))
    except FileNotFoundError:
        pass

    with open('sent_quizzes.json', 'r') as f:
        data = json.load(f)
        quizzes = data['quizzes']
		
        quiz_index = 0  # Initialize counter at 0 (first element)
        while quiz_index < len(quizzes):
            quiz = quizzes[quiz_index]  # Access quiz based on counter

            # Mulai dari ID 1 dan increment secara otomatis
            next_id = 1
            for quiz in quizzes:
                # Jika 'id' tidak ada, berikan ID yang sudah ditentukan
                if 'id' not in quiz:
                    quiz['id'] = next_id
                    next_id += 1

                if quiz['id'] not in sent_quizzes:
                    send_quiz(quiz['chat_id'], quiz['question'], quiz['options'], quiz['correct_option_id'])
                    sent_quizzes.add(quiz['id'])
                    time.sleep(300) #tidur bentar 5 menit / delay
        
        quiz_index += 1  # Increment counter after processing

# schedule.every().day.at("21:30", "Asia/Jakarta").do(job)  # Change to desired scheduling interval

while True:
    schedule.run_pending()
    time.sleep(1)
