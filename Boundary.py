import cv2
import pickle


img_path = '/Users/mahmoudsami/Desktop/git/frame_660.jpg'
output_file = '/Users/mahmoudsami/Desktop/git/parking_layout_new3.pkl'

SENSOR_W, SENSOR_H = 20, 20 

IMG_W, IMG_H = 1280, 720

try:
    with open(output_file, 'rb') as f:
        sensorList = pickle.load(f)
    print(f"تم تحميل {len(sensorList)} حساس سابق.")
except:
    sensorList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        x1 = x - SENSOR_W // 2
        y1 = y - SENSOR_H // 2
        sensorList.append((x1, y1))
        
        with open(output_file, 'wb') as f:
            pickle.dump(sensorList, f)

    # حذف حساس (بالنقر باليمين)
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(sensorList):
            x1, y1 = pos
            # إذا النقرة داخل مربع الحساس
            if x1 < x < x1 + SENSOR_W and y1 < y < y1 + SENSOR_H:
                sensorList.pop(i)
                with open(output_file, 'wb') as f:
                    pickle.dump(sensorList, f)
                break

while True:
    img = cv2.imread(img_path)
    if img is None: break
    
    img = cv2.resize(img, (IMG_W, IMG_H))

    for i, pos in enumerate(sensorList):
        x, y = pos
        # رسم مربع الحساس (لون أزرق مميز للحساسات)
        cv2.rectangle(img, (x, y), (x + SENSOR_W, y + SENSOR_H), (255, 0, 255), 2)
        # كتابة رقم الـ ID
        cv2.putText(img, str(i + 1), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    cv2.imshow("Parking Sensor Setup", img)
    cv2.setMouseCallback("Parking Sensor Setup", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()