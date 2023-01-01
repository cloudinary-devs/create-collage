from flask import Flask, render_template, request
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
import json
from time import sleep

# read from .env file
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

config = cloudinary.config(secure=True)



imgs=["docs/collage/photo-01","docs/collage/photo-02","docs/collage/photo-03","docs/collage/photo-04","docs/collage/photo-05","docs/collage/photo-06","docs/collage/photo-07","docs/collage/photo-08","docs/collage/photo-09","docs/collage/photo-10","docs/collage/photo-11","docs/collage/photo-12"]

def getURL(publicID):
  collage=cloudinary.api.resource(publicID)  
  return collage['secure_url']


@app.route("/", methods=['GET', 'POST'])
def index(): 
  if request.method == 'POST':
    
    try:
      result = cloudinary.uploader.destroy('docs/collage/new_collage')

    except Exception:
      pass     

    



    Url="https://api.cloudinary.com/v1_1/demo/image/create_collage" 
    test=[request.form.get('pos1'),request.form.get('pos2'),request.form.get('pos3'),request.form.get('pos4'), request.form.get('pos5'),request.form.get('pos6'),request.form.get('pos7'), request.form.get('pos8'),request.form.get('pos9'),request.form.get('pos10'),request.form.get('pos11'),request.form.get('pos12')]
  
    pos=[]
    try:
      for j in test:
        pos.append(ord(j)-64)
    except:
      msg1=""
      url=""
      msg2=""
      return render_template('index.html',msg1=msg1,url=url,msg2="")
      
    # Build array of assets:
    images=[]
    for p in pos:
      images.append(imgs[p-1])
      
    uniqueList = []
    for pic in images:
      if pic not in uniqueList:
          uniqueList.append(pic)
    
    assets=[]
    for s in uniqueList:
      assets.append({"media": s})
 



  
    # Build template:
    temp=[]
  
    j=1
    is_working="yes"
    for i,p in enumerate(pos):
      is_duplicate="no"
      for compare in range(0,i):
        if p==pos[compare]:
          is_duplicate="yes"
          temp.append(temp[compare])
          break
          
      if is_duplicate=="no":
        temp.append(j)
        print(j)
        j+=1
        
  
    mj = {
        "template": [[temp[0],temp[1],temp[2],temp[3]],
                    [temp[4],temp[5],temp[6],temp[7]],
                    [temp[8],temp[9],temp[10],temp[11]]],
        "width": 600,
        "height": 450,
        "columns": 4,
        "rows": 3,
        "spacing": 1,
        "color": "white",
        "assetDefaults": { "kind": "upload", "crop": "fill", "gravity": "center", "format":"auto", "quality":"auto" },
        "assets": assets
      }

    manifestJSON=json.dumps(mj)
    print(manifestJSON)

    Data={
        "public_id": "docs/collage/new_collage",
        "manifest_json": manifestJSON,
        "resource_type": "image",
        "upload_preset": "email_uploader",
        "method": "POST"
    }

  


  
    r = requests.post(url = Url, data = Data)
    print(r.text)
       
    while True:
      try:
        sleep(3)
        url=getURL("docs/collage/new_collage") 
        break
      except:
        continue

    msg="Your customized architecture collage"
    return render_template('done.html', msg=msg, url=url)

  return render_template('index.html', msg="", url="")
    
  
  
  
@app.route("/done", methods=['GET','POST'])
def done():
  if request.method == 'POST':
    url = getURL("docs/collage/start_architecture") 
    msg1="Create a collage with Cloudinary!"
    return render_template('index.html', msg1=msg1, url=url)
  url=getURL("docs/collage/start_architecture") 
  msg1="Create a collage with Cloudinary!"
  return render_template('done.html', msg1=msg1, url=url)



if __name__ == "__main__":
  app.run()


  
