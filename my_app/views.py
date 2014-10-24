from flask import render_template, jsonify, request, Response

from my_app import app

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        # form.get is used to access the data from a form POST request
        title = int(request.form.get('form_title'))
        rent = int(request.form.get('form_rent'))
        total = rent + title
        data = {"total": str(total)}
        return jsonify(data)

    #if POST doesn't render - render the below GET instead
    return render_template("calculator.html")
