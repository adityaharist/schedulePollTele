import requests
import json
import schedule
import time

# chat_id = -1002261380303 (grup AI/testing) , -1002480946780 (channel catatan skb), -1002199224078 (grup diskusi skb)
# token = 7822122704:AAG53aitpT0LSvmGY0jfL9xBC15Dr9yBnxg (Nami), 7265588452:AAGjRY77LhnYmqhi7PeIs-JdYwqNeSl1m5U (Chopper)

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
    with open('quizzes.json', 'r') as f:
        data = json.load(f)
        for quiz in data['quizzes']:
            send_quiz(quiz['chat_id'], quiz['question'], quiz['options'], quiz['correct_option_id'])
            time.sleep(300)  # Jeda selama 10 menit (60 detik = 1 menit)

# Schedule adjusted to every 10 minutes (change as needed) jika menit=minutes, jika detik=seconds
schedule.every(1).seconds.do(job)
# Jadwalkan pengiriman kuis setiap kali program dijalankan
# schedule.every().day.at("07:11", "Asia/Jakarta").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)