from flask import Flask, render_template, request, g
import os
from PIL import Image
from Predictor import Predictor
from DB_Helper import DB_Helper
from random import randint
import sqlite3


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}


@app.before_request
def before_request():
    g.db = DB_Helper()
    g.predictor = Predictor(g.db)
    with open("static/Practice_labels.txt") as file:
        practice_answers = file.read()
    g.practice_answers = json.loads(practice_answers)
    with open("static/featuresynonyms.txt") as file:
        synonyms = file.read()
    g.synonyms = json.loads(synonyms)
    g.features = {'Cap Shape': ['Convex', 'Ovoid', 'Cylindric', 'Conical', 'Cuspidate', 'Campanulate', 'Umbonate', 'Papillate', 'Plane', 'Umbilicate', 'Depressed', 'Infundibuliform'], 'Cap Texture': ['Smooth', 'Uneven', 'Rugose', 'Scrobiculate', 'Virgate', 'Sericeous', 'Fibrilose', 'Squamose', 'Pulverulent', 'Zonate', 'Areolate', 'Glutinous', 'Pubescent', 'Floccose', 'Hispid', 'Villose'], 'Cap Color': ['White', 'Tan', 'Brown', 'Black', 'Yellow', 'Red', 'Orange', 'Purple'], 'Cap Margins': ['Entire', 'Appendiculate', 'Striate', 'Sulcate', 'Pilcate', 'Split', 'Lacerate', 'Hairy', 'Undulating', 'Serrate'], 'Gill Attachment': ['Adnate', 'Adnexed', 'Sinuate', 'Seceding', 'Decurrent', 'Subdecurrent', 'Free', 'Collared'], 'Gill Spacing': ['Crowded', 'Close', 'Distant'], 'Gill Color': ['White', 'Tan', 'Brown', 'Black', 'Yellow', 'Red', 'Orange'], 'Stem Shape': ['Cylindrical', 'Club', 'Bulbous'], 'Stem Texture': ['Smooth', 'Scaley', 'Hairy', 'Fuzzy', 'Wrinkled'], 'Stem Annulus': ['Superior', 'Median', 'Basal', 'None'], 'Stem Color': ['White', 'Tan', 'Brown', 'Black', 'Yellow', 'Red', 'Orange']}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def results():
    files = request.files.getlist('file')
    filepaths = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            width, height = img.size
            scale_factor = 224 / max(width, height)
    
            # Calculate the new dimensions while maintaining the aspect ratio
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
    
            # Resize the image
            resized_img = img.resize((new_width, new_height))
            resized_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepaths.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "Invalid file format"
    prediction, conf = g.predictor.predict(filepaths)
    return render_template('results.html', uploads=app.config['UPLOAD_FOLDER'], filename=filename, features=g.features, predictions=prediction, conf=conf)


@app.route('/comparison', methods=['POST'])
def comparison():
    Features = {}
    if request.method == 'POST':
        Featues['Image_file'] = request.form['filename']
        Featues['Cap_Shape'] = request.form['Cap Shape']
        Featues['Cap_Texture'] = request.form['Cap Texture']
        Featues['Cap_Color'] = request.form['Cap Color']
        Featues['Cap_Margins'] = request.form['Cap Margins']
        Featues['Gill_Attachment'] = request.form['Gill Attachment']
        Featues['Gill_Spacing'] = request.form['Gill Spacing']
        Featues['Gill_Color'] = request.form['Gill Color']
        Featues['Stem_Shape'] = request.form['Stem Shape']
        Featues['Stem_Texture'] = request.form['Stem Texture']
        Featues['Stem_Annulus'] = request.form['Stem Annulus']
        Featues['Stem_Color'] = request.form['Stem Color']
        if request.form.get('permission') == '1':
            g.db.save_entry(Features)
        # labels = {'Cap Shape':Cap_Shape, 'Cap Texture':Cap_Texture, 'Cap Color':Cap_Color, 'Cap Margins':Cap_Margins, 'Gill Attachment':Gill_Attachment, 'Gill Spacing':Gill_Spacing, 'Gill Color':Gill_Color, 'Stem Shape':Stem_Shape, 'Stem Texture':Stem_Texture, 'Stem Annulus':Stem_Annulus, 'Stem Color':Stem_Color}
        newSynonyms = {}
        for key, value in Features.items():
            if key != 'Image_file' and value:
                newSynonyms[value] = g.synonyms[value]
        prediction, conf = g.predictor.predict(os.path.join(app.config['UPLOAD_FOLDER'], Image_file))
        return render_template('comparison.html', labels=labels, filename=Image_file, features=g.features, predictions=prediction, conf=conf, synonyms=newSynonyms)
        
@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/practice')
def practice():
    filename = f'{randint(0,15)}.jpg'
    return render_template('practice.html', filename=filename, features=g.features)

@app.route('/answers', methods=['POST'])
def answer():
    if request.method == 'POST':
        labels = {}
        Image_file = request.form['filename']
        labels['Cap_Shape'] = request.form['Cap Shape']
        labels['Cap_Texture'] = request.form['Cap Texture']
        labels['Cap_Color'] = request.form['Cap Color']
        labels['Cap_Margins'] = request.form['Cap Margins']
        labels['Gill_Attachment'] = request.form['Gill Attachment']
        labels['Gill_Spacing'] = request.form['Gill Spacing']
        labels['Gill_Color'] = request.form['Gill Color']
        labels['Stem_Shape'] = request.form['Stem Shape']
        labels['Stem_Texture'] = request.form['Stem Texture']
        labels['Stem_Annulus'] = request.form['Stem Annulus']
        labels['Stem_Color'] = request.form['Stem Color']
        #labels = {'Cap Shape': Cap_Shape, 'Cap Texture': Cap_Texture, 'Cap Color': Cap_Color, 'Cap Margins': Cap_Margins,
        #          'Gill Attachment': Gill_Attachment, 'Gill Spacing': Gill_Spacing, 'Gill Color': Gill_Color,
        #         'Stem Shape': Stem_Shape, 'Stem Texture': Stem_Texture, 'Stem Annulus': Stem_Annulus,
        #         'Stem Color': Stem_Color}
        answers = g.practice_answers[Image_file]
        scores = {}
        for feature, response in labels.items():
            if response in answers[f'{feature}']:
                scores[f'{feature}'] = response
            else:
                if response == '':
                    temp = 'Unknown /'
                else:
                    temp = f"{response} / "
                if answers[f'{feature}'] == []:
                    temp += ' Unknown'
                else:
                    temp += f" {answers[f'{feature}']} "
                    scores[f'{feature}'] = temp

        return render_template('checkpractice.html', filename=Image_file, features=g.features, scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
