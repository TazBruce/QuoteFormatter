from flask import Flask, render_template, request, send_file
import pandas as pd
import os

__author__ = 'Tasman Bruce'

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
upload_ID = 1


def convert_csv(csv_path):
    quote_target = os.path.join(APP_ROOT, 'static/quote')

    if not os.path.isdir(quote_target):
        os.mkdir(quote_target)

    output_dir = os.path.normpath(os.path.join(APP_ROOT, 'static/quote/PlumbingWorldQuote-' + str(upload_ID) + '.csv'))
    file = pd.read_csv(csv_path)
    header = file.iloc[2]
    file = file[3:]
    file.columns = header
    file.to_csv(output_dir, index=False)
    return send_file(output_dir, as_attachment=True)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        global upload_ID
        upload_ID += 1
        csv_target = os.path.join(APP_ROOT, 'static/csv')

        # Preparing directory
        if not os.path.isdir(csv_target):
            os.mkdir(csv_target)

        # Uploading File
        for file in request.files.getlist('file'):
            filename = str(upload_ID) + "-" + file.filename
            destination = "/".join([csv_target, filename])
            file.save(destination)

            # Creating images
            if os.path.isfile(destination):
                return convert_csv(destination)
    except Exception as error:
        print(error.__str__())
        return render_template('failed.html')


if __name__ == '__main__':
    app.run()
