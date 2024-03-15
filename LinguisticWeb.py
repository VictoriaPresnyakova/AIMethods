import os

from flask import Flask, render_template, request

from LinguisticScale import LinguisticScale

app = Flask(__name__)

scale = LinguisticScale()


@app.route("/")
def Display_IMG():
    plot = os.path.join('static', 'images', "plot.png")
    return render_template("LinguisticScale.html", user_image=plot)


@app.route("/change-plot", methods=['POST'])
def Change_IMG():
    try:
        scale.add_label(request.form['label'], [int(val) for val in request.form['values'].split()])
    except Exception as ex:
        print(ex)
    return Display_IMG()


if __name__ == '__main__':
    app.run(debug=True)
