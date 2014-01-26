import npyscreen
import sqlite3

class AddressDatabase(object):
    def __init__(self, filename="book.db"):
        self.dbfilename = filename
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute(
        "CREATE TABLE IF NOT EXISTS records\
            ( record_internal_id INTEGER PRIMARY KEY, \
              cognome     TEXT, \
              nome   TEXT, \
              ragione_sociale TEXT \
              )" \
            )
        db.commit()
        c.close()

    def add_record(self, cognome = '', nome='', ragione_sociale=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('INSERT INTO records(cognome, nome, ragione_sociale) \
                    VALUES(?,?,?)', (cognome, nome, ragione_sociale))
        db.commit()
        c.close()

    def update_record(self, record_id, cognome = '', nome='', ragione_sociale=''):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('UPDATE records set cognome=?, nome=?, ragione_sociale=? \
                    WHERE record_internal_id=?', (cognome, nome, ragione_sociale, \
                                                        record_id))
        db.commit()
        c.close()

    def delete_record(self, record_id):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('DELETE FROM records where record_internal_id=?', (record_id,))
        db.commit()
        c.close()

    def list_all_records(self, ):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * from records')
        records = c.fetchall()
        c.close()
        return records

    def get_record(self, record_id):
        db = sqlite3.connect(self.dbfilename)
        c = db.cursor()
        c.execute('SELECT * from records WHERE record_internal_id=?', (record_id,))
        records = c.fetchall()
        c.close()
        return records[0]



class RecordList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(RecordList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "%s %s" % (vl[1], vl[2])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITRECORDFM').value =act_on_this[0]
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').value = None
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
        self.parent.update_list()
def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
        self.parent.update_list()
        
class RecordListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = RecordList
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.myDatabase.list_all_records()
        self.wMain.display()

class EditRecord(npyscreen.ActionForm):
    def create(self):
        self.value = None

        self.add(npyscreen.TitleFixedText, name = "------------ STIPULA CONTRATTO DONAZIONE ----------------")
        self.wgDataStipula = self.add(npyscreen.TitleDateCombo, name = "il: ")
        self.wgLuogoStipula = self.add(npyscreen.TitleText, name = "in: ")
        self.add(npyscreen.TitleFixedText, name = "------------ ANAGRAFICA ----------------")
        self.wgCognome = self.add(npyscreen.TitleText, name = "Cognome:",)
        self.wgNome = self.add(npyscreen.TitleText, name = "Nome:")
        self.wgRagSociale = self.add(npyscreen.TitleText, name = "Ente/Soc:")
        self.wgCFIVA = self.add(npyscreen.TitleText, name = "CF/PIVA:")
        self.wgComuneNascita = self.add(npyscreen.TitleText, name = "Nato a:")
        self.wgProvNascita = self.add(npyscreen.TitleText, name = "Prov.:")
        self.wgDataNascita = self.add(npyscreen.TitleDateCombo, name = "Data Nascita:")


        self.add(npyscreen.TitleFixedText, name = "--------------------- RESIDENZA -------------------------")
        self.wgVia = self.add(npyscreen.TitleText, name = "Via:")
        self.wgCivicoVia = self.add(npyscreen.TitleText, name = "N.:")
        self.wgComuneRes = self.add(npyscreen.TitleText, name = "Comune:")
        self.wgProvRes = self.add(npyscreen.TitleText, name = "Prov.:")

        self.add(npyscreen.TitleFixedText, name = "--------------------- CONTATTI -------------------------")
        self.wgTel = self.add(npyscreen.TitleText, name = "Tel:")
        self.wgEmail = self.add(npyscreen.TitleText, name = "Email:")


    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_record(self.value)
            self.name = "Record id : %s" % record[0]
            self.record_id = record[0]
            self.wgCognome.value = record[1]
            self.wgNome.value = record[2]
            self.wgRagSociale.value = record[3]
        else:
            self.name = "Ass. Cult. Verde Binario # Nuovo Record"
            self.record_id          = ''
            self.wgCognome.value   = ''
            self.wgNome.value = ''
            self.wgRagSociale.value    = ''
            self.wgComuneNascita.value = ''
            self.wgProvNascita.value  = ''
            self.wgDataNascita.value  = ''
            self.wgTel.value      = ''
            self.wgEmail.value    = ''
            
            
    def on_ok(self):
        if self.record_id: # We are editing an existing record
            self.parentApp.myDatabase.update_record(self.record_id,
                                            cognome=self.wgCognome.value,
                                            nome = self.wgNome.value,
                                            ragione_sociale = self.wgRagSociale.value,
                                            )
        else: # We are adding a new record.
            self.parentApp.myDatabase.add_record(cognome=self.wgCognome.value,
            nome = self.wgNome.value,
            ragione_sociale = self.wgRagSociale.value,
            )
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
        
class AddressBookApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = AddressDatabase()
        self.addForm("MAIN", RecordListDisplay)
        self.addForm("EDITRECORDFM", EditRecord)

if __name__ == '__main__':
    myApp = AddressBookApplication()
    myApp.run()
        