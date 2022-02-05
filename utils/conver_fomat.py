import json
import glob

def coordinateCvt2YOLO(size, box):

    dw = 1. / size[0]
    dh = 1. / size[1]

        # (xmin + xmax / 2)
    x = (box[0] + box[2]) / 2.a0
        # (ymin + ymax / 2)
    y = (box[1] + box[3]) / 2.0

        # (xmax - xmin) = w
    w = box[2] - box[0]
        # (ymax - ymin) = h
    h = box[3] - box[1]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh

    return (round(x, 3), round(y, 3), round(w, 3), round(h, 3))
def convert_to_yolo(json_data,class_name,save):

   size =  [json_data['label_info']['image']['width'],json_data['label_info']['image']['height']]
   file_name = json_data['label_info']['image']['file_name'].split('.')[:-1][0]

   with open(f"{save}/{file_name}.txt" ,"w") as f:

    for bbox_dict in json_data['label_info']['annotations']:
        box = bbox_dict['bbox']
        yolo_box = coordinateCvt2YOLO(size, box)
        f.write(f"{class_name} {yolo_box[0]} {yolo_box[1]} {yolo_box[2]} {yolo_box[3]} \n")


def folder_convert_to_yolo(path,save_path):
    json_files = glob.glob(f"{path}/*.json")

    for json_path in json_files:
        if json_path.split("/")[-1].split('_')[1] == "cow":
            class_name = 0 
        elif json_path.split("/")[-1].split('_')[1] == "pig":
            class_name = 1 
        else:
            print(f'오류 {json_path}')

        with open(json_path, "r") as f:
            json_data = json.load(f)
        convert_to_yolo(json_data,class_name,save_path)

def jsontocsv(file_path,save_path):

    df = pd.read_json(file_path)
    df_s = pd.DataFrame()
    df_s['ImageID'] = df['image_id'].map(lambda x : x+'.jpg')
    df_s['LabelName'] =  df['category_id'].map(lambda x : 'cow' if x==1 else 'pig')
    df_s['Conf'] = df['score']
    df_s['XMin'] = df['bbox'].map(lambda x : x[0])
    df_s['XMax'] = df['bbox'].map(lambda x : x[2])
    df_s['YMin'] = df['bbox'].map(lambda x : x[1])
    df_s['YMax'] = df['bbox'].map(lambda x : x[3])

    df_s.to_csv(save_path)
