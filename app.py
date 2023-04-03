from flask import Flask,request,render_template,url_for
from CUKU.components import details_collector as dc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    global result
    
    if result is not None:
        # The search has already been performed, return the result
        result_file = f"{name_to_search}_info.html"
        return render_template(result_file)

    print("running search")
    name_to_search = request.form['name_to_search']
    details_needed_amount = int(request.form['details_needed_amount'])
    run_in_backend = bool(request.form.get('run_in_backend'))

    result = dc.RUN(name_to_search, details_needed_amount, run_in_backend)

    result_file = f"{name_to_search}_info.html"
    return render_template(result_file)

# Define result before the function
result = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
