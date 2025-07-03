# read from .env file
from dotenv import load_dotenv
load_dotenv()

# read from .env file
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
import json
from time import sleep
import time

app = Flask(__name__)

config = cloudinary.config(secure=True)

# List of (image_url, public_id) pairs
# The public_id should include the 'docs/collage/' prefix to place it in the correct asset folder
images_to_upload = [
    ("https://res.cloudinary.com/demo/image/upload/v1663148439/docs/collage/photo-01.jpg", "docs/collage/photo-01"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148545/docs/collage/photo-02.jpg", "docs/collage/photo-02"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148563/docs/collage/photo-03.jpg", "docs/collage/photo-03"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148564/docs/collage/photo-04.jpg", "docs/collage/photo-04"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148572/docs/collage/photo-05.jpg", "docs/collage/photo-05"),
    ("https://res.cloudinary.com/demo/image/upload/v1663082653/docs/collage/photo-06.jpg", "docs/collage/photo-06"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148574/docs/collage/photo-07.jpg", "docs/collage/photo-07"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148594/docs/collage/photo-08.jpg", "docs/collage/photo-08"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148608/docs/collage/photo-09.jpg", "docs/collage/photo-09"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148601/docs/collage/photo-10.jpg", "docs/collage/photo-10"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148574/docs/collage/photo-11.jpg", "docs/collage/photo-11"),
    ("https://res.cloudinary.com/demo/image/upload/v1663148566/docs/collage/photo-12.jpg", "docs/collage/photo-12"),
    ("https://res.cloudinary.com/demo/image/upload/v1663149550/docs/collage/start_architecture.png", "docs/collage/start_architecture")
]

for image_url, public_id in images_to_upload:
    try:
        result = cloudinary.uploader.upload(
            image_url,
            public_id=public_id,  # This will place it in docs/collage/
            overwrite=True,
            resource_type="image"
        )
        print(f"Uploaded {image_url} to {public_id}: {result['secure_url']}")
    except Exception as e:
        print(f"Failed to upload {image_url}: {e}") 


imgs=["docs/collage/photo-01","docs/collage/photo-02","docs/collage/photo-03","docs/collage/photo-04","docs/collage/photo-05","docs/collage/photo-06","docs/collage/photo-07","docs/collage/photo-08","docs/collage/photo-09","docs/collage/photo-10","docs/collage/photo-11","docs/collage/photo-12"]

def getURL(publicID):
  collage=cloudinary.api.resource(publicID)  
  return collage['secure_url']


@app.route("/", methods=['GET', 'POST'])
def index(): 
  if request.method == 'POST':
    # Generate a unique public ID using the current timestamp
    collage_public_id = f"docs/collage/new_collage_{int(time.time())}"

    try:
      result = cloudinary.uploader.destroy(collage_public_id)

    except Exception:
      pass     

    



    # Use the configured cloud name for the collage creation URL
    Url = f"https://api.cloudinary.com/v1_1/{config.cloud_name}/image/create_collage"
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
        "public_id": collage_public_id,
        "manifest_json": manifestJSON,
        "resource_type": "image",
        "upload_preset": "my_preset",
        "method": "POST"
    }

  


  
    r = requests.post(url = Url, data = Data)
    print("*************")
    print(r.text)
       
    while True:
      try:
        sleep(3)
        url=getURL(collage_public_id) 
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


  
