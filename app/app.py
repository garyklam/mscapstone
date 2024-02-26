from flask import Flask, render_template, request, g, session
import os
import json
from Predictor import Predictor
from DB_Helper import DB_Helper
from Image_Preprocessor import Image_Preprocessor
from random import randint


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}


@app.before_request
def before_request():
    g.db = DB_Helper()
    g.img_processor = Image_Preprocessor()
    g.predictor = Predictor(g.img_processor)
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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            g.img_processor.resize(file, filepath)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepaths.append(filepath)
        else:
            return "Invalid file format"
    print(f'____________________________Results: {filepaths}')
    top5, conf = g.predictor.predict(filepaths)
    session['top5'] = top5
    session['conf'] = conf
    top_species_data = []
    for x in top5:
        top_species_data.append(g.db.query(x))
    #might have to change filename=filepaths[0] to include all images
    return render_template('results.html', uploads=app.config['UPLOAD_FOLDER'], filename=filepaths[0],
                           features=g.features, predictions=top_species_data, conf=conf)


@app.route('/comparison', methods=['POST'])
def comparison():
    Features = {}
    if request.method == 'POST':
        top5 = session.get('top5', None)
        top_species_data = []
        for x in top5:
            top_species_data.append(g.db.query(x))
        conf = session.get('conf', None)
        Image_file = request.form['filename']
        Features['Cap_Shape'] = request.form['Cap Shape']
        Features['Cap_Texture'] = request.form['Cap Texture']
        Features['Cap_Color'] = request.form['Cap Color']
        Features['Cap_Margins'] = request.form['Cap Margins']
        Features['Gill_Attachment'] = request.form['Gill Attachment']
        Features['Gill_Spacing'] = request.form['Gill Spacing']
        Features['Gill_Color'] = request.form['Gill Color']
        Features['Stem_Shape'] = request.form['Stem Shape']
        Features['Stem_Texture'] = request.form['Stem Texture']
        Features['Stem_Annulus'] = request.form['Stem Annulus']
        Features['Stem_Color'] = request.form['Stem Color']
        if request.form.get('permission') == '1':
            g.db.save_entry(Image_file, Features)
        newSynonyms = {}
        for key, value in Features.items():
            if value:
                newSynonyms[value] = g.synonyms[value]
        return render_template('comparison.html', labels=Features, filename=Image_file, features=g.features,
                               predictions=top_species_data, conf=conf, synonyms=newSynonyms)


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
