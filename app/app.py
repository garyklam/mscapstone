from flask import Flask, render_template, request, g
import os
from PIL import Image
from Predictor import Predictor
from random import randint
import sqlite3


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}


@app.before_request
def before_request():
    g.predictor = Predictor()
    g.user_db = sqlite3.connect('static/Labels.db')
    g.user_db.row_factory = sqlite3.Row
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
    if request.method == 'POST':
        Image_file = request.form['filename']
        Cap_Shape = request.form['Cap Shape']
        Cap_Texture = request.form['Cap Texture']
        Cap_Color = request.form['Cap Color']
        Cap_Margins = request.form['Cap Margins']
        Gill_Attachment = request.form['Gill Attachment']
        Gill_Spacing = request.form['Gill Spacing']
        Gill_Color = request.form['Gill Color']
        Stem_Shape = request.form['Stem Shape']
        Stem_Texture = request.form['Stem Texture']
        Stem_Annulus = request.form['Stem Annulus']
        Stem_Color = request.form['Stem Color']
        if request.form.get('permission') == '1':
            cursor = g.user_db.cursor()
            cursor.execute("INSERT INTO user_labels (ImageFile, CapShape, CapTexture, CapColor, CapMargins, GillAttachment, GillSpacing, GillColor, StemShape, StemTexture, StemAnnulus, StemColor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (Image_file, Cap_Shape, Cap_Texture, Cap_Color, Cap_Margins, Gill_Attachment, Gill_Spacing, Gill_Color, Stem_Shape, Stem_Texture, Stem_Annulus, Stem_Color))
            g.user_db.commit()
            cursor.close
        labels = {'Cap Shape':Cap_Shape, 'Cap Texture':Cap_Texture, 'Cap Color':Cap_Color, 'Cap Margins':Cap_Margins, 'Gill Attachment':Gill_Attachment, 'Gill Spacing':Gill_Spacing, 'Gill Color':Gill_Color, 'Stem Shape':Stem_Shape, 'Stem Texture':Stem_Texture, 'Stem Annulus':Stem_Annulus, 'Stem Color':Stem_Color}
        newSynonyms = {}
        for key, value in labels.items():
            if value:
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
        Image_file = request.form['filename']
        Cap_Shape = request.form['Cap Shape']
        Cap_Texture = request.form['Cap Texture']
        Cap_Color = request.form['Cap Color']
        Cap_Margins = request.form['Cap Margins']
        Gill_Attachment = request.form['Gill Attachment']
        Gill_Spacing = request.form['Gill Spacing']
        Gill_Color = request.form['Gill Color']
        Stem_Shape = request.form['Stem Shape']
        Stem_Texture = request.form['Stem Texture']
        Stem_Annulus = request.form['Stem Annulus']
        Stem_Color = request.form['Stem Color']
        labels = {'Cap Shape': Cap_Shape, 'Cap Texture': Cap_Texture, 'Cap Color': Cap_Color, 'Cap Margins': Cap_Margins,
                  'Gill Attachment': Gill_Attachment, 'Gill Spacing': Gill_Spacing, 'Gill Color': Gill_Color,
                  'Stem Shape': Stem_Shape, 'Stem Texture': Stem_Texture, 'Stem Annulus': Stem_Annulus,
                  'Stem Color': Stem_Color}
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
