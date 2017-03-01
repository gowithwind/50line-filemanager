import os,sys,urllib
if sys.version_info >= (3,):# download bottle,dont use wget for windows
    import urllib.request as urllib #for python 3
if not os.path.exists('bottle.py'):
    urllib.urlretrieve ("http://bottlepy.org/bottle.py", "bottle.py")
from bottle import route, run, request, redirect, static_file
html='''<!DOCTYPE html><html><head><meta charset="utf-8">
<div id ="file-drop" style="width:800px;border:2px dashed;">
<h1>Bottle File Mannger, surport drag file to upload</h1><p id="log"></p>
<form  method="post" enctype="multipart/form-data">
<input type="file" multiple id="file" name="file">
<input type="submit" id="submit"></form>
<div>%s</div></div><script>
document.getElementById('log').textContent=window.location.hash.slice(1);
var file_drop = document.getElementById('file-drop');
file_drop.addEventListener('dragover',
  function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy';
  },false)
file_drop.addEventListener('drop',
  function(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    var files = evt.dataTransfer.files;  // FileList object.
    if(files.length==0)return;
    document.getElementById('file').files = files;
    document.getElementById('submit').click();
  },false)
</script>'''
@route('/')
def index():
    p = request.query.get('p','')
    if os.path.isfile(p):
        return redirect('/static/'+p)
    files = ['<p><a href="/?p=%s">%s</a></p>'%(os.path.join(p,f), f) for f in os.listdir(p or './')]
    return html%(''.join(files))
@route('/', method='POST')
def upload():
    upload  = request.files.get('file')
    upload.save(request.query.get('p','./'),overwrite=True)
    redirect("/?p=%s#success"%request.query.get('p',''))
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename,  root=sys.argv[1])
run(host='0.0.0.0', port=7777, debug=True,reloader=True)