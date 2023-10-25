import sqlite3
from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from PIL import Image
import torch


class Predictor():
    def __init__(self):
        ## used to rebuild specieslist if changes occur
        # destination = 'C:\\Users\\garyk\\Downloads\\Capstone\\Initial_train_species'
        # self.specieslist = []
        #
        # for dir in os.listdir(destination):
        #     # os.mkdir(os.path.join(destination, dir))
        #     self.specieslist.append(dir)
        #
        # print(self.specieslist)
        conn = sqlite3.connect('my_database.db')
        self.cursor = conn.cursor()
        self.specieslist = ['Agaricus_arvensis', 'Agaricus_bernardii', 'Agaricus_bisporus', 'Agaricus_campestris', 'Agaricus_moelleri', 'Agaricus_xanthodermus',
                            'Amanita_ceciliae', 'Amanita_echinocephala', 'Amanita_fulva', 'Amanita_gemmata', 'Amanita_phalloides', 'Amanita_porphyria', 'Amanita_rubescens',
                            'Ampulloclitocybe_clavipes', 'Chroogomphus_rutilus', 'Coprinellus_micaceus', 'Coprinopsis_atramentaria', 'Coprinus_comatus', 'Cortinarius_caerulescens',
                            'Entoloma_rhodopolium', 'Entoloma_sinuatum', 'Galerina_marginata', 'Hygrocybe_punicea', 'Hygrophorus_chrysodon', 'Hypholoma_fasciculare',
                            'Hypholoma_marginatum', 'Lactarius_chrysorrheus', 'Lactarius_deliciosus', 'Lactarius_fulvissimus', 'Lactarius_piperatus', 'Lactarius_subdulcis',
                            'Lentinellus_cochleatus', 'Lepiota_cristata', 'Macrolepiota_mastoidea', 'Macrolepiota_procera', 'Marasmius_oreades', 'Mycena_pura',
                            'Omphalotus_olearius', 'Paxillus_involutus', 'Russula_aurea', 'Russula_emetica', 'Russula_virescens', 'Tricholoma_equestre', 'Tricholoma_pardinum',
                            'Tricholoma_portentosum', 'Tricholoma_sulphureum']


        PATH = "CNN_test\\5_9_species_effnet0_adam_10.pt"

        # Replace the final fully connected layer
        # num_features = self.model.fc.in_features
        # self.model.fc = nn.Linear(num_features, 46)

        self.model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=46)
        self.model.load_state_dict(torch.load(PATH))

        self.model.eval()

    def predict(self, img_path):
        process = transforms.ToTensor()
        image = Image.open(img_path).convert('RGB')
        tensor = process(image)
        tensor = torch.unsqueeze(tensor, 0)
        output = self.model(tensor)
        probs = torch.nn.functional.softmax(output, dim=1)
        conf, indx = torch.topk(probs, k=3, dim=1)
        conf = conf.squeeze().tolist()
        predicted = []
        conf_score = []
        for x in indx.squeeze().tolist():
            id = self.specieslist[x].replace('_', ' ')
            predicted.append(self.query(id))
        for i in range(len(predicted)):
            conf_score.append(conf[i] // .0001 / 100) #turn to percent and round value
        return predicted, conf_score

    def query(self, species):
        self.cursor.execute("SELECT * FROM my_table WHERE Species=?", (species,))
        data = self.cursor.fetchone()
        return data