import torch
from torch.autograd import Variable
import cv2
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd
import imageio

def detect(frame,net,transform):
    height,width = frame.shape[:2]
    frame_transform = transform(frame)[0]
    x = torch.from_numpy(frame_transform).permute(2,0,1)
    x = Variable(x.unsqueeze(0))
    y = net(x)
    detection = y.data
    scale = torch.Tensor([width,height,width,height])
    for i in range(detection.size(1)):
        j=0
        while detection[0,i,j,0]>= 0.6:
            take = (detection[0,i,j,1:]*scale).numpy()
            cv2.rectangle(frame,(int(take[0]),int(take[1])),(int(take[2]),int(take[3])),(200,0,0),2)
            cv2.putText(frame,labelmap[i-1],(int(take[0]),int(take[1])),cv2.FONT_HERSHEY_SIMPLEX,2,(100,0,255),2,cv2.LINE_AA)
            j += 1
    return frame


net = build_ssd('test') 

net.load_state_dict(torch.load('ssd300_mAP_77.43_v2.pth', map_location = lambda storage, loc: storage))
transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))

reader = imageio.get_reader('man_chair.mp4')


#fps = reader.get_meta_data()['fps']
writer = imageio.get_writer('output_man.mp4')#,fps=fps)


for i,frame in enumerate(reader):
    frame = detect(frame,net.eval(),transform)
    writer.append_data(frame)
    print(i)

writer.close()


    


# Object Detection

