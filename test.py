from deepface import DeepFace
import cv2
import os
import tempfile

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

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 初始化人脸计数
    face_count = 0

    try:
        # 使用DeepFace检测和分析人脸
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # 如果检测到人脸，可能是单个人脸或多个人脸
        if isinstance(results, list):
            faces = results
        else:
            faces = [results]  # 包装为列表，以便统一处理

        # 统计人脸个数
        face_count = len(faces)

        for face in faces:
            # 获取每张人脸的区域
            x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制人脸框

            # 获取情绪信息
            emotion = face['dominant_emotion']

            # 提取人脸区域图像
            face_image = frame[y:y+h, x:x+w]

            # 人脸识别：默认“Unknown”，匹配数据库
            found_name = "Unknown"
            
            # 将人脸区域图像保存为临时文件，用于 DeepFace.find()
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_filename = temp_file.name + ".jpg"
                cv2.imwrite(temp_filename, face_image)

            try:
                # 使用 DeepFace 对比已知人脸数据库
                df_result = DeepFace.find(img_path=temp_filename, db_path=face_db_path, enforce_detection=False)
                if len(df_result) > 0:
                    # 提取人名（只显示文件名部分，去除路径和扩展名）
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
        continue

    # 显示实时视频帧
    cv2.imshow('Face Recognition and Emotion Analysis', frame)

    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
