from efficientnet_pytorch import EfficientNet
from PIL import Image
import torch



class Predictor:
    def __init__(self, db, img_processor):
        # # used to rebuild specieslist if changes occur
        # destination = 'C:\\Users\\garyk\\Downloads\\Capstone\\selectset2_test'
        # self.specieslist = []
        #
        # for dir in os.listdir(destination):
        #     # os.mkdir(os.path.join(destination, dir))
        #     self.specieslist.append(dir)
        #
        # print(self.specieslist)
        self.db = db
        self.img_procesor = img_processor
        self.specieslist = ['Agaricus_arvensis', 'Agaricus_bernardii', 'Agaricus_bisporus', 'Agaricus_campestris', 'Agaricus_moelleri', 'Agaricus_xanthodermus',
                            'Amanita_ceciliae', 'Amanita_echinocephala', 'Amanita_fulva', 'Amanita_gemmata', 'Amanita_phalloides', 'Amanita_porphyria', 'Amanita_rubescens',
                            'Ampulloclitocybe_clavipes', 'Chroogomphus_rutilus', 'Clitocybe rivulosa', 'Coprinellus_micaceus', 'Coprinopsis_atramentaria', 'Coprinus_comatus', 'Cortinarius_caerulescens',
                            'Entoloma_rhodopolium', 'Entoloma_sinuatum', 'Galerina_marginata', 'Hygrocybe_punicea', 'Hygrophorus_chrysodon', 'Hypholoma_fasciculare',
                            'Hypholoma lateritium', 'Hypholoma_marginatum', 'Inocybe rimosa', 'Lactarius_chrysorrheus', 'Lactarius_deliciosus', 'Lactarius_fulvissimus', 'Lactarius_piperatus', 'Lactarius_subdulcis',
                            'Lentinellus_cochleatus', 'Lepiota_cristata', 'Lepista (Clitocybe) saeva', 'Macrolepiota_mastoidea', 'Macrolepiota_procera', 'Marasmius_oreades', 'Mycena_pura',
                            'Omphalotus_olearius', 'Paxillus_involutus', 'Russula_aurea', 'Russula_emetica', 'Russula_virescens', 'Tricholoma_equestre', 'Tricholoma_pardinum',
                            'Tricholoma_portentosum', 'Tricholoma_sulphureum']

        PATH = "static/5_9_species_effnet0_adam_10.pt"

        self.model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=46)
        self.model.load_state_dict(torch.load(PATH))

        self.model.eval()

    def predict(self, img_paths):
        conf_scores = {}
        for img_path in img_paths:
            tensor = g.img_processor.totensor(img_path)
            output = self.model(tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            conf = probs.squeeze().tolist()

            for id_num, prob in enumerate(conf):
                species = self.specieslist[int(id_num)].replace('_', ' ')
                if species in conf_scores.keys():
                    conf_scores[f'{species}'].append(prob)
                else:
                    conf_scores[f'{species}'] = [prob]
        for species in conf_scores:
            avg_conf = sum(conf_scores[f'{species}']) / len(conf_scores[f'{species}']) // .0001 / 100
            conf_scores[f'{species}'] = avg_conf
        sorted_conf_scores = {k: v for k, v in sorted(conf_scores.items(), key=lambda item: item[1], reverse=True)}
        top_5_species = list(sorted_conf_scores.keys())[:5]
        top_species_data = []
        for x in top_5_species:
            top_species_data.append(self.db.query(x))

        return top_species_data, conf_scores
