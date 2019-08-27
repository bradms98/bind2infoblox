from flask import Flask, render_template, url_for, flash, redirect, Response
from forms import InputForm
from b2i import b2i

app = Flask(__name__)

app.config['SECRET_KEY'] = '23eb28c4c8bc3cafa6faf2968fa6f322'

bindInput = 'this is the input text'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    output = ''
    if form.in_string.data:
        converted = b2i(form.in_string.data)
        #for line in converted.csvOutput:
        #    output = output + '\n' + line
        #flash('Output: ' + output, 'danger')
        #flash('Received: \n' + converted.bindInput, 'success')
        return Response(
            converted.csvOutput,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=" + converted.zone + ".csv"})
    else: 
        return render_template('home.html', form=form, output=output, title='Home')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')