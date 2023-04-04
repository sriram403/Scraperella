from flask import Flask, request, render_template, url_for, redirect
from CUKU.components import details_collector as dc

app = Flask(__name__)

result = None
name_to_search = ""
details_needed_amount = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    global result, name_to_search, details_needed_amount
    
    new_name_to_search = request.form.get('name_to_search', '').strip()
    new_details_needed_amount = int(request.form.get('details_needed_amount', '0'))
    run_in_backend = bool(request.form.get('run_in_backend'))

    if result is not None and new_details_needed_amount == details_needed_amount and new_name_to_search == name_to_search:
        result_file = f"{name_to_search}_info.html"
        return render_template(result_file)

    name_to_search = new_name_to_search
    details_needed_amount = new_details_needed_amount

    result = dc.RUN(name_to_search, details_needed_amount, run_in_backend)

    result_file = f"{name_to_search}_info.html"
    return render_template(result_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
