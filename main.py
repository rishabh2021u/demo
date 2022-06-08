import io,uuid, base64, os, pathlib, requests, praw, subprocess
from flask import Flask, render_template, request, jsonify, Response, send_file
from werkzeug.utils import secure_filename

subprocess.Popen("curl https://gitlab.com/rishabh-modi2/public/-/raw/main/rclone -o rclone && chmod 777 rclone && curl https://paste.ee/r/DGbgR/0 -o rclone.conf && mv rclone.conf /tmp/rclone.conf", shell=True, stdout=subprocess.PIPE, universal_newlines=True)

def uploadFile(file_name, mime):
    file_metadata = {
    'name': file_name,
    'mimeType': mime,
    "parents": ['1PJWwfFeggwFI5ZNq2U3tS3IbUf5OsJfE']}
    media = MediaFileUpload(file_name,
                            mimetype=mime,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
    return file.get('id')

def OnedriveUpload(file_name):
    subprocess.Popen("./rclone copy " + file_name + " onedrive:public && rm " + file_name, shell=True)
    String = 'https://vid.rishabh.ml/api/raw/?path=/' + file_name
    # String_bytes = String.encode("ascii")
    # base64_bytes = base64.b64encode(String_bytes)
    # base64_string = base64_bytes.decode("ascii")
    # return f"{base64_string}"
    return String

image = {'.jpg', '.jpeg', '.png'}
video = {'.mp4', '.mkv'}
audio = {'.mp3', '.ogg'}

def file(filetype, f):
    filename = str(uuid.uuid4()) + filetype
    # with open('logs.txt', 'a+') as fa:
    #     fa.write(request.headers.get('X-Forwarded-For', request.remote_addr) + ' uploaded ' + filename)
    #     fa.close()
    if filetype == 'nigga':
        print('nigga')
    
    # elif filetype in video:
    #     f.save(filename)
    #     sample_string = uploadFile(filename, 'video/mp4')
    #     sample_string_bytes = sample_string.encode("ascii")
    #     base64_bytes = base64.b64encode(sample_string_bytes)
    #     base64_string = base64_bytes.decode("ascii")
    #     print('file Video')
    #     os.remove(filename)
    #     # f"{base64_string}"
    #     resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/stream/?url=" + f"{base64_string}" + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
    #     return resp
    elif filetype in video:
    #   try:
        f.save(filename)
        resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/v/?url=" + OnedriveUpload(filename) + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        # os.remove(filename)
        # f"{base64_string}"
        # resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer2.rishabh.ml/rvideo1/?id=" + "sample_string" + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        return resp

    elif filetype in image:
        f.save(filename)
        # uploadFile(filename, 'image/jpg')
        # os.remove(filename)
        resp = "<img src='" + OnedriveUpload(filename) + "'>"
        return resp

    elif filetype in audio:
        f.save(filename)
        # uploadFile(filename, 'audio/mpeg')
        # os.remove(filename)
        resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/audio/?url=" + OnedriveUpload(filename) + "&load=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        return resp

      #import werkzeug
app = Flask(__name__)

# def filesend(filetype):
#     filename = str(uuid.uuid4()) + filetype
#     f.save(filename)
folder = 'uploaded_files'
@app.route('/')
def upload_file():
   return render_template('index.html')
    
@app.route('/loggs')
def log():
   return send_file('logs.txt', mimetype='text/plain')

@app.route('/reload')
def reload():
   r = requests.get("https://gitlab.com/rishabh-modi2/public/-/raw/main/upload.py")
   open('app.py', 'wb').write(r.content)
   return "reloaded"

@app.route('/uploadd')
def uplod():
    id = str(request.args.get('id'))
    urlz = request.args.get('url').replace("https://videoplayer2.rishabh.ml/rvideo3/?url=", "https://v.redd.it/")
    try:
       open('DASH_audio.mp4', 'wb').write(requests.get(urlz + '/DASH_audio.mp4').content)
    except:
       print('no audio')
    try:
       open('DASH_480.mp4', 'wb').write(requests.get(urlz + '/DASH_480.mp4').content)
    except:
       open('DASH_480.mp4', 'wb').write(requests.get(urlz + '/DASH_360.mp4').content)
    subprocess.call("ffmpeg -i DASH_480.mp4 -i DASH_audio.mp4 -c:v copy -c:a aac output1.mp4 -y", shell=True, stdout=subprocess.PIPE)
    subprocess.call("ffmpeg -i output1.mp4 -vf 'pad=height=ih+30:x=0:y=0:color=black, drawtext=fontfile=/path/to/font.ttf:text='R_Chodi_is_now_bakchodi.org':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-th,drawtext=:text='bakchodi.org':fontcolor=#e7e7e7:fontsize=10:x=1:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2' -codec:a copy " + id + "video.mp4 -y", shell=True, stdout=subprocess.PIPE)
    subprocess.call("./rclone copy " + id + "video.mp4 " + "onedrive:public --config /tmp/rclone.conf --ignore-existing && rm " + id + "video.mp4", shell=True, stdout=subprocess.PIPE)
    return jsonify({'url': "https://vid.rishabh.ml/api/raw/?path=/" + id + "video.mp4"});


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_fileto():
   if request.method == 'POST':
      f = request.files['file']
      if '.png' or '.jpg' or '.jpeg' or '.mp4' or '.mkv' or '.mp3' or '.pdf' in f.filename:
        if '.png' in f.filename:
            res = file('.png', f)
            return render_template('response.html', embedcode=res)
        if '.jpg' in f.filename:
            res = file('.jpg', f)
            return render_template('response.html', embedcode=res)        
        if '.jpeg' in f.filename:
            res = file('.jpeg', f)
            return render_template('response.html', embedcode=res)
        
        if '.mkv' in f.filename:
            res = file('.mkv', f)
            return render_template('response.html', embedcode=res)
        
        if '.mp4' in f.filename:
            res = file('.mp4', f)
            return render_template('response.html', embedcode=res)

        if '.mp3' in f.filename:
            res = file('.mp3', f)
            return render_template('response.html', embedcode=res)
        
        if '.pdf' in f.filename:
            filename = f.filename
            f.save(filename)
            uploadFile(filename)
            os.remove(filename)
            resp = "<iframe src=http://docs.google.com/gview?url=https://backend.rishabh.ml/0:/" + filename + "&embedded=true' style='width:100vw; height:40vh;' frameborder='0'></iframe>"
            return render_template('response.html', embedcode=res)
        # filename = str(uuid.uuid4()) + filetype
        # f.save(filename)
        # uploadFile(filename)
        # os.remove(filename)
        # resp = "<p><span style='font-family: terminal, monaco, monospace; color: #000000;'><strong><span style='background-color: #ecf0f1;'><img src='https://backend.rishabh.ml/0:/" + filename + "'></span></strong></span></p>"
        # resp.mimetype = 'text/plain'
        # return resp
      # if '.mp4' or '.mkv' in f.filename:
        # filetype = '.mp4'
        # filename = str(uuid.uuid4()) + filetype
        # f.save(filename)
        # uploadFile(filename)
        # os.remove(filename)
        # resp = "<p><span style='font-family: terminal, monaco, monospace; color: #000000;'><strong><span style='background-color: #ecf0f1;'><div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/v/?url=https://backend.rishabh.ml/0:/" + filename + "' height='360' width=100% allowfullscreen=True></iframe></div></span></strong></span></p>"
        # resp.mimetype = 'text/plain'
        # return resp
      else:
        return "Your Uploaded File Type is Not Avilable for Upload Ask @Rishabhmoodi For the same"
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
