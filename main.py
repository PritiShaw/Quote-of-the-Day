from flask import Flask, request, Response, redirect
from PIL import Image
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/image', methods=['GET'])
def output():
    response = requests.get('http://quotes.rest/qod.json')
    jsonResponse = response.json()
    q = jsonResponse["contents"]["quotes"][0]["quote"]
    a = jsonResponse["contents"]["quotes"][0]["author"]
    burl = jsonResponse["contents"]["quotes"][0]["background"]
    #q = "Do not worry if you have built your castles in the air. They are where they should be. "
    #a =  "Henry David Thoreau "
    #burl = 'https://theysaidso.com/img/qod/qod-inspire.jpg'
    
    response = requests.get(burl)
    img = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(img)
    (x, y) = (10, 100)
    font = ImageFont.truetype('Pacifico-Regular.ttf', size=25)
    color = 'rgb(255, 255, 255)' # white color
    draw.text((x, y), q, fill=color, font= font )
    (x, y) = (600, 250)
    a = '~'+a
    draw.text((x, y), a, fill=color, font= font)
    #img.save('greeting_card.png')
    buffer = BytesIO()
    img.save(buffer,format="JPEG")                  #Enregistre l'image dans le buffer
    myimage = buffer.getvalue()   
    return (redirect("data:image/jpeg;base64,"+ (base64.b64encode(myimage)).decode("utf-8"), code= 301))
    #return Response(response=("data:image/jpeg;base64,"+ (base64.b64encode(myimage)).decode("utf-8") ), status=200, mimetype=" image/jpeg"c

if __name__ == '__main__':
    app.run(debug=True) 