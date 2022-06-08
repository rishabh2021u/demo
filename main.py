import io,uuid, base64, os, pathlib, requests, subprocess
from flask import Flask, render_template, request, jsonify, Response, send_file
from werkzeug.utils import secure_filename

subprocess.Popen("curl https://gitlab.com/rishabh-modi2/public/-/raw/main/rclone -o rclone && chmod 777 rclone && curl https://paste.ee/r/DGbgR/0 -o rclone.conf", shell=True, stdout=subprocess.PIPE, universal_newlines=True)

      #import werkzeug
app = Flask(__name__)

# def filesend(filetype):
#     filename = str(uuid.uuid4()) + filetype
#     f.save(filename)
@app.route('/loggs')
def log():
   return send_file('logs.txt', mimetype='text/plain')

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
    subprocess.call("ffmpeg -i output1.mp4 -vf 'pad=height=ih+30:x=0:y=0:color=black, drawtext=fontfile=/path/to/font.ttf:text='R_Chodi_is_now_bakchodi.org':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-th,drawtext=:text='bakchodi.org':fontcolor=#e7e7e7:fontsize=10:x=1:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=3:x=w-text_w:y=(h-text_h)/2' -codec:a copy " + id + "video.mp4 -y" + " && ./rclone copy " + id + "video.mp4 " + "onedrive:public --config rclone.conf --ignore-existing && rm " + id + "video.mp4", shell=True, stdout=subprocess.PIPE)
    return jsonify({'url': "https://vid.rishabh.ml/api/raw/?path=/" + id + "video.mp4"});

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
