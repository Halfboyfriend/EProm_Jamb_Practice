import requests
import json
import io
import time

#------------API REQUESTS --------------

class QUESTIONS():

    def __init__(self, subject):
        self.subject = subject

    def fetch_questions(self):

        url = f"https://questions.aloc.com.ng/api/v2/m?subject={self.subject}"
        ACCESS_KEY = 'ALOC-58655dfcbd88362a1758'
        headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'AccessToken': ACCESS_KEY
        }

        response = requests.get(url=url, headers=headers)
        data = response.text
        new_data = []
        new_data.append(eval(data))

        with open(f"question_bank/{self.subject}.json", 'w', encoding='utf-8', newline='') as file:
            json.dump(new_data, file, indent=4)

    def load_question(self):
        for sub in self.subject:
            with io.open(f'question_bank/{sub}.json', 'r', encoding='utf-8') as file:
                data_log = json.load(file)
            return data_log
        
    



SUBJECTS = ['english', 'physics', 'english']

que = QUESTIONS(SUBJECTS)

loaded = que.load_question()
print(loaded)

# for sub in SUBJECTS:
#     question = QUESTIONS(sub)
#     loaded = question.load_question()
#     more = 1
#     while more < 40:
#         try:
#             for i in range(1, more +1):
#                 print(loaded[0]['data'][i])
#                 print(f'Total loaded is {i}')
#         except UnicodeEncodeError:
#             pass
#         more += 1
    