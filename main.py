from flask import *
import requests
import json
# from datetime import date

app = Flask(__name__)


@app.route("/")
def home():
    ACCESS_KEY = 'uhTPYDLCZsCUu5LJi-h16w37TwaiZWXTYwvJ7JtzUD4'
    query = 'depression mental health'
    params = {'query': query, 'client_id': ACCESS_KEY, 'w': 720, 'h': 600}
    endpoint = f"https://api.unsplash.com/photos/random"
    # #can use like this also
    # endpoint = f"https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}&w=720&h=600&query={query}" 

    # Make the API request
    response = requests.get(endpoint, params=params)

    # Parse the response data as JSON
    data = response.json()
    img_url = data['urls']['regular']

    return render_template('home.html', img_url=img_url)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/og')
def og():
    return render_template('OngoingElection.html')

def depressionSeveraity(score):
    if(score<=4):
        return ("Minimal or No depression", "Your score suggests minimal or no depression. However, if you're experiencing any other concerns or symptoms, it's important to reach out to a healthcare professional for further evaluation and support.")
    elif(score<=9) :
        return ("Mild depression", "Your score indicates mild depression. It's essential to pay attention to your mental health and well-being. Consider seeking support from a healthcare professional, counselor, or therapist who can provide guidance and help you manage your symptoms.")
    elif(score<=14) :
        return ("Moderate depression", "Your score suggests moderate depression. It's crucial to address your mental health concerns and seek professional help. Consider reaching out to a healthcare provider or mental health specialist who can provide appropriate treatment options and support.")
    elif(score<=19) :
        return ("Moderately severe depression", "Your score indicates moderately severe depression. It's important to prioritize your mental health and seek professional support. Contact a healthcare professional or mental health specialist to discuss your symptoms and develop a comprehensive treatment plan.")
    elif(score<=27) :
        return ("Severe depression", "Your score suggests severe depression. It's crucial to seek immediate professional help and support. Contact a healthcare professional, therapist, or mental health crisis hotline to discuss your symptoms and access appropriate interventions for managing severe depression.")
    

@app.route('/result', methods=['post'])
def result():
    score = int(request.form['score'])
    depression,text = depressionSeveraity(score)

    return render_template('result.html', score=score, depression=depression ,text=text)








###################################################################################################
from camera import VideoCamera
import os

def read_count_file(file_path):
    with open(file_path, 'r') as f:
        line = f.readline().strip()

    counts = line.split()
    if len(counts) == 2:
        negative_emotions_count = int(counts[0])
        total_emotions_count = int(counts[1])
    else:
        negative_emotions_count = 0
        total_emotions_count = 0

    return negative_emotions_count, total_emotions_count

file_name = 'emotion_count.txt'
file_path = os.path.abspath(file_name)

# negative_count, total_count = read_count_file(file_path)
# print(negative_count , total_count)
# print(int(negative_count/total_count * 100 ))
###################################################################################

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +  
               b'\r\n\r\n')
        camera.update_count_file()  # Update the count file


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video-test')
def video_test():
    return render_template('video_test.html')


@app.route('/video-result', methods=['post'])
def video_result():
    score = int(request.form['score'])
    depression,text = depressionSeveraity(score)

    negative_count, total_count = read_count_file(file_path)
    emotions =  int(negative_count/(total_count+1) * 100) 

    combined_score =  ((score/27)*0.7) + ((emotions/100)*0.3)
    combined_score =  round(combined_score ,  2)

    return render_template('video_result.html', score=score, depression=depression ,text=text, emotions=emotions, combined_score=combined_score)

if __name__ == "__main__":
    app.run(port=80, debug=True)
