from rest_framework.generics import GenericAPIView
import base64
import cv2
import easyocr
from datetime import datetime
from django.shortcuts import render
import os




class CovertBASEDatToImage(GenericAPIView):

    def get(self,request):
        return render(request,'index.html')
    

    def post(self, request):
        response = {}
        data = request.data
        try:
            file_name = str(datetime.now()).replace(':','-') + '.jpg'
            base64_string = bytes(data['base64_string'],'utf-8')
            image_data = base64.b64decode(base64_string)
            img_file = open(file_name, 'wb')
            img_file.write(image_data)
            img_file.close()

            image = cv2.imread(file_name)
            reader = easyocr.Reader(['en'])
            results = reader.readtext(image, detail = 0)
            # results = reader.readtext(image)
            
            response['status'] = 1
            
        except Exception as exp:
            results= []
            response['err'] = str(exp)
            response['status'] = 0
        response['data'] = results
        os.remove(file_name)
        return render(request,'index.html',response)
    
