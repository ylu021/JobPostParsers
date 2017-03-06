from flask import *
import indeed_parse2 as ip 
import urllib
import time
import os
app = Flask(__name__)
app.secret_key =  open("/dev/random","rb").read(32) 

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv

@app.route("/") #the route() decorator binds a function to a URL
@app.route("/<parsername>")
def index(parsername=None):
	return render_template('index.html', parsername=parsername) #look for templates in templates folder

@app.route("/indeedparser/result", methods=['GET', 'POST'])
def hello(uri=None):
	if request.method == 'POST':
		q = request.form['q']
		exp = request.form['exp'].replace(' ','_').lower()
		obj = {'q': q, 'explvl': exp}
		uri = urllib.urlencode(obj)
		url = 'https://www.indeed.com/jobs?'+uri
		return Response(stream_template('result.html', data=stream_with_context(ip.generate(url,0))))
		# return Response(stream_with_context(ip.generate(url,0)))
	# else:
	return render_template('result.html', uri=uri)	
	
if __name__=="__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
