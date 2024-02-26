import sqlite3

class DB_Helper:
    def __init__(self):
        self.conn = sqlite3.connect('static/Species_info.db')
        self.conn.row_factory = sqlite3.Row
        
  def query(self, species):
        cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM species_info WHERE Species=?", (species,))
        data = self.cursor.fetchone()
        cursor.close
        return data

  def save_entry(
        cursor = self.conn.cursor()
        self.cursor.execute("INSERT INTO user_labels (ImageFile, CapShape, CapTexture, CapColor, CapMargins, GillAttachment, GillSpacing, GillColor, StemShape, StemTexture, StemAnnulus, StemColor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (Image_file, Cap_Shape, Cap_Texture, Cap_Color, Cap_Margins, Gill_Attachment, Gill_Spacing, Gill_Color, Stem_Shape, Stem_Texture, Stem_Annulus, Stem_Color))
        self.conn.commit()
        cursor.close
