from flask import Flask, Response
from deepface import DeepFace
import cv2
import os
import tempfile
from flask_apscheduler import APScheduler
import pymysql
import threading
import datetime
import time
from .model import add_emotion_record

app = Flask(__name__)
scheduler = APScheduler()

# 设置人脸数据库路径
face_db_path = "faces"  # 存储已知人脸图像的文件夹路径

# 读取数据库中人脸图像和姓名
face_db = []
for file in os.listdir(face_db_path):
    if file.endswith(".jpg") or file.endswith(".png"):
        face_db.append({
            "name": os.path.splitext(file)[0],  # 文件名作为姓名
            "path": os.path.join(face_db_path, file)
        })

# 摄像头捕获
cap = cv2.VideoCapture(0)


def generate_frames():
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        try:
            face_count = 0
            results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            faces = results if isinstance(results, list) else [results]
            face_count = len(faces)

            for face in faces:
                # 获取每张人脸的区域
                x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制人脸框

                # 获取情绪信息
                emotion = face['dominant_emotion']

                # 提取人脸区域图像
                face_image = frame[y:y + h, x:x + w]

                # 默认显示的名字是 "Unknown"
                found_name = "Unknown"

                # 将人脸区域图像保存为临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_filename = temp_file.name
                    cv2.imwrite(temp_filename, face_image)

                try:
                    # 使用 DeepFace 对比数据库
                    df_result = DeepFace.find(img_path=temp_filename, db_path=face_db_path, enforce_detection=False)
                    if len(df_result) > 0:
                        # 获取识别的名字
                        found_name = os.path.splitext(os.path.basename(df_result[0]['identity'][0]))[0]
                except Exception as e:
                    print("识别失败:", e)
                finally:
                    # 删除临时文件
                    os.remove(temp_filename)

                # 显示姓名和情绪
                cv2.putText(frame, f"Name: {found_name}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            # 显示总人脸数
            cv2.putText(frame, f"Total Faces: {face_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        except Exception as e:
            print("分析失败:", e)

        # 将帧编码为 JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def start_runner():
    def start_analysis():
        global found_name, emotion
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            try:
                face_count = 0
                results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                faces = results if isinstance(results, list) else [results]
                face_count = len(faces)

                for face in faces:
                    # 获取每张人脸的区域
                    x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制人脸框

                    # 获取情绪信息
                    emotion = face['dominant_emotion']

                    # 提取人脸区域图像
                    face_image = frame[y:y + h, x:x + w]

                    # 默认显示的名字是 "Unknown"
                    found_name = "Unknown"

                    # 将人脸区域图像保存为临时文件
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                        temp_filename = temp_file.name
                        cv2.imwrite(temp_filename, face_image)

                    try:
                        # 使用 DeepFace 对比数据库
                        df_result = DeepFace.find(img_path=temp_filename, db_path=face_db_path, enforce_detection=False)
                        if len(df_result) > 0:
                            # 获取识别的名字
                            found_name = os.path.splitext(os.path.basename(df_result[0]['identity'][0]))[0]
                    except Exception as e:
                        print("识别失败:", e)
                    finally:
                        # 删除临时文件
                        os.remove(temp_filename)

                    # 显示姓名和情绪
                    cv2.putText(frame, f"Name: {found_name}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0),
                                2)
                    cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),
                                2)

                # 显示总人脸数
                cv2.putText(frame, f"Total Faces: {face_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            except Exception as e:
                print("分析失败:", e)

    @scheduler.task('interval', id='job_1', seconds=10, misfire_grace_time=10)
    def store_student_emotion():
        add_emotion_record(found_name, emotion)
    thread = threading.Thread(target=start_analysis)
    thread.start()
