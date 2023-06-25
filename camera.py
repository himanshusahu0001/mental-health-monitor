import cv2
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

class VideoCamera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.negative_emotions_count = 0
        self.total_emotions_count = 0
        self.file_path = 'emotion_count.txt'  # Path to the file
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        ret, frame = self.video.read() # ret are success flags/(bool values)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3 ,5)

        # for (x,y,w,h) in faces:
        #     cv2.rectangle(frame, (x,y) , (x+w,y+h), (0,0,255), 3)
        #     # break

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255),2)
            roi = frame[y:y+h,x:x+w]
            roi = cv2.resize(roi, (64, 64))

            predictions = DeepFace.analyze(roi, actions=['emotion'], enforce_detection=False) 
            label = predictions[0]['dominant_emotion']
            # ###################################
            if label in ['sad', 'angry', 'disgust', 'fear']:
                self.negative_emotions_count += 1
            self.total_emotions_count += 1
            # #####################################
            label_pos = (y-10, x)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, label,label_pos, font,1,(0,255,0),2)


        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def update_count_file(self):
        with open(self.file_path, 'w') as f:
            f.write(f"{self.negative_emotions_count}  {self.total_emotions_count}\n")

    def get_negative_emotions_count(self):
        return self.negative_emotions_count