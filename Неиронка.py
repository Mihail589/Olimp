import cv2
import os
from fps import *
import multiprocessing as m, requests
from tkinter import *
def main():
	v = 0
	  # predict on an image
	url = "https://api.ultralytics.com/v1/predict/us3AzJNqQZx4cA9KdAbG"
	headers = {"x-api-key": "cf245df58a239f127ef11053218ebd3c65f62a88ff"}
# Inference arguments (optional)
	data = {"size": 640, "confidence": 0.25, "iou": 0.45}
	flag = True
	cap = cv2.VideoCapture(0)
	DIR = os.listdir("img/")
	for x in range(len(DIR)):
		os.remove(f"img/{DIR[x]}")
	fps = FPS()
	counter = 0
	while True:
    # Read a frame from the video
		success, frame = cap.read()
		#data1000(fps(), True)
		v  += 1
	#cv2.resize(frame, (640))
		cv2.imwrite("img/img_"+str(v)+".jpg", frame)
		with open("img/img_"+str(v)+".jpg", "rb") as image_file:
			files = {"image": image_file}
			response = requests.post(url, headers=headers, files=files, data=data)
			res = response.json()
		for i in res["data"]:
			for a in i:
				if i["class"] == 0 and flag:
					counter += 1
					flag = False
					box = i["box"] 
				#cv2.rectangle(frame, (box["x1"], box["y1"]), (box["x1"] + box["x2"], box["y1"] + box["y2"]), (0, 255, 0), 2)
				#cv2.imshow("frame", frame)
			flag = True
		print(f"[LOG] Количество людей = {counter}")
		print(fps())
		cv2.putText(frame, str(counter), (300, 180),cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 10)
		cv2.imshow("frame", frame)
		counter = 0
		#img = cv2.imread(f"img/img_{str(v)}.jpg")
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cap.release()
	cv2.destroyAllWindows()
	exit(0)
if __name__ == "__main__":
	p2 = m.Process(target=main())
	#ggui(1000, 700, "Управление рециркулятором")
	p2.start()
	
