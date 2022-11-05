from flask import Flask, request, render_template, flash, redirect
from ocr import extractInfo
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/images'

# checking file extension
EXT = ['jpg', 'jpeg', 'png']
def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1) in EXT

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file.filename == '':
        flash('No image selected')
        return redirect(request.url)
    elif file :#and allowedFile(file.filename):
        file_dir = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_dir)

        info = extractInfo(file_dir)
        name = ', '.join(info.extract_name())
        email = ', '.join(info.extract_email())
        contact = ', '.join(info.extract_contact_number())
        
        # card_info = {'name': name, 'email': email, 'contact': contact}
        return render_template('home.html', name=name, email=email, contact=contact)
    else:
        flash('Allowed image extension are jpeg, jpg, png')
        return redirect(request.url)
if __name__ == '__main__':
    app.run(debug=True)