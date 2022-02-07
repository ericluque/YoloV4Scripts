import cv2
import time

CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]


# Criar o array de nomes a partir do arquivo names
class_names = []
with open("labels.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

# Carregar os pesos e configs da Yolo
net = cv2.dnn.readNet("backup/lampadas_10000.weights", "lampadas.cfg")
#net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")

#Setar o modelo para usar a GPU
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#Carregar o modelo

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(608, 608), scale=1/255)

#Inicia a detecção

frame = cv2.imread("backup/508.jpg")

scale_percent = 50 # percent of original size
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

# Detecta os objetos
classes, scores, boxes = model.detect(resized, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)


# Plota os bboxes na imagem gravando tempo de inicio e fim apra referência.
for (classid, score, box) in zip(classes, scores, boxes):
    color = COLORS[int(classid) % len(COLORS)]
    label = "%s : %f" % (class_names[classid], score)
    cv2.rectangle(resized, box, color, 2)
    cv2.putText(resized, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Cria uma String com os tempos de referência, adiciona na imagem e plota na tela
cv2.imshow("A.I.nstens - Descomplicando I.A.", resized)
        
    



