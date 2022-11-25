from flask import Flask, render_template, request, send_file, flash
import pandas as pd
import os
import tempfile

__author__ = 'Tasman Bruce'

app = Flask(__name__)
APP_ROOT = tempfile.gettempdir()
upload_ID = 1


def convert_csv(csv_path):
    print('Processing CSV...')
    quote_target = os.path.join(APP_ROOT, 'quote')

    if not os.path.isdir(quote_target):
        print("No quote folder, creating now..")
        os.mkdir(quote_target)

    print("Quote folder found")

    output_dir = os.path.normpath(os.path.join(APP_ROOT, 'quote/PlumbingWorldQuote-' + str(upload_ID) + '.csv'))

    print("Reading CSV..")
    file = pd.read_csv(csv_path)
    header = file.iloc[2]
    file = file[3:]
    file.columns = header

    print("CSV Updated, saving now..")
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
        csv_target = os.path.join(APP_ROOT, 'csv')

        # Preparing directory
        if not os.path.isdir(csv_target):
            print("CSV folder not found, creating now...")
            os.mkdir(csv_target)

        print("CSV folder found")

        # Uploading File
        for file in request.files.getlist('file'):
            filename = str(upload_ID) + "-" + file.filename
            destination = "/".join([csv_target, filename])
            print("Uploading CSV...")
            file.save(destination)

            # Creating images
            if os.path.isfile(destination):
                return convert_csv(destination)
    except Exception as error:
        print(error.__str__())
        return render_template('failed.html')


if __name__ == '__main__':
    app.run()
