import sqlite3

class DB_Helper:
    def __init__(self):
        self.known_conn = sqlite3.connect('static/Species_info.db')
        self.known_conn.row_factory = sqlite3.Row
        self.user_conn = sqlite3.connect('static/Labels.db')

    def query(self, species):
        cursor = self.known_conn.cursor()
        cursor.execute("SELECT * FROM species_info WHERE Species=?", (species,))
        data = cursor.fetchone()
        cursor.close()
        return data

    def save_entry(self, filename, features):
        cursor = self.user_conn.cursor()
        cursor.execute("INSERT INTO user_labels (ImageFile, CapShape, CapTexture, CapColor, CapMargins, GillAttachment, "
                       "GillSpacing, GillColor, StemShape, StemTexture, StemAnnulus, StemColor) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (filename, features['Cap_Shape'], features['Cap_Texture'],
                        features['Cap_Color'], features['Cap_Margins'], features['Gill_Attachment'],
                        features['Gill_Spacing'], features['Gill_Color'], features['Stem_Shape'],
                        features['Stem_Texture'], features['Stem_Annulus'], features['Stem_Color']))
        self.user_conn.commit()
        cursor.close()
