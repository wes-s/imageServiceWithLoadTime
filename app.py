from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from PIL import Image
import requests
from io import BytesIO
from flask import send_file
import time

app = Flask(__name__)
api =Api(app)

class getImage(Resource):
    def get(self, imageName):

        imageService = ['https://upload.wikimedia.org/wikipedia/commons/a/a5/Cylon_Centurion_head.jpg'
                        ,'https://picsum.photos/550/800'
                        ,'https://inspirobot.me/api?generate=true']

        if request.args:
            loadTime = request.args.get('load',0)
            try:
                imageSource = imageService[int(request.args.get('source', '0'))]
            except IndexError:
                imageSource = imageService[0]
        else:
            loadTime = 0
            imageSource = imageService[0]
            
        outImg = Image.new('RGBA', (256, 256), (255, 0, 0, 0))

        if int(request.args.get('source',0)) == 2:
            # inspirobot can be a bit racy
            url = requests.get(imageSource).content
            if not url:
               url = 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Cylon_Centurion_head.jpg'
        else:
            url = imageSource
        
        response = requests.get(url)
        
        if(response):
        # if no response this return will not happen. return outside if statement will return stream of empty Out image instantiated above
            time.sleep(float(loadTime))
            return send_file(BytesIO(response.content), mimetype='image/png')
        else:
            return send_file(BytesIO(outImg), mimetype = 'image/png')
        

api.add_resource(getImage,"/getImage/<string:imageName>")

# run.py in local werkzeug simple server when locally testing
if __name__ == "__main__":
    app.run(debug=True)