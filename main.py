import json 
import simplejson
import base64
import requests

def find_face(imgpath):
    print('Finding')

    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key":'gHhd8Nrx5yawR3FYcEMjqEyTBDB5fz8r',
            "api_secret":'cYekk5cmPp2YqyJg-wpNDuAy_RVnS8x-', "image_url":imgpath, "return_landmark": 1
            }
    files = {'image_file':open(imgpath, 'rb')}

    response = requests.post(http_url, data=data, files=files)
    # print(response)

    req_con = response.content.decode('utf-8')
    # print(req_con)

    this_json = simplejson.loads(req_con)
    faces = this_json['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    print(rectangle)

    return rectangle

def merge_face(image_url1, image_url2, image_url, number): # how close is the final picture
    ff1 = find_face(image_url1)
    ff2 = find_face(image_url2)

    rectangle1 = str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height'])
    rectangle2 = str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height'])

    f1 = open(image_url1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()


    f2 = open(image_url2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    url_add = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
    data = {"api_key":'gHhd8Nrx5yawR3FYcEMjqEyTBDB5fz8r',
            "api_secret":'cYekk5cmPp2YqyJg-wpNDuAy_RVnS8x-', "template_base64":f1_64, "template_rectangle":rectangle1,
            "merge_base64":f2_64, "merge_rectangle":rectangle2, "merge_rate": number}

    response1 = requests.post(url_add, data=data)
    req_con1 = response1.content.decode('utf-8')
    print(req_con1)

    req_dict = json.JSONDecoder().decode(req_con1)
    result = req_dict['result']
    imgdata = base64.b64decode(result)

    file = open(image_url, 'wb')
    file.write(imgdata)
    file.close()




image1 = r"D:\Code\CS50\Project\face1.jpg"
image2 = r"D:\Code\CS50\Project\face2.jpg"
image = r"D:\Code\CS50\Project\mergedFace.jpg"

merge_face(image1, image2, image, 100)
