import firebase_admin
from firebase_admin import credentials, db

# Percorso corretto al file delle credenziali scaricato
cred = credentials.Certificate(r"gymbot-c8ad7-firebase-adminsdk-w62qj-b1e546c2b8.json")

# Inizializzazione dell'app Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gymbot-c8ad7-default-rtdb.europe-west1.firebasedatabase.app'
})

# Funzione per creare o aggiornare un nodo nel database
def get_scheda(username, giorno):
    ref = db.reference(f'utenti/{username}/{giorno}')  # Percorso al nodo specifico
    scheda = ref.get()  # Lettura del valore
    if scheda:
        print(f"Scheda trovata per {username} nel giorno {giorno}: {scheda}")
    else:
        print(f"Nessuna scheda trovata per {username} nel giorno {giorno}.")
    return scheda   

def modifica_scheda_gym(username, giorno, scheda):
    ref = db.reference(f'utenti/{username}/{giorno}')  # Percorso al nodo specifico
    ref.set(scheda)  # Scrittura del valore
    print(f"Scheda modificata per {username} nel giorno {giorno}: {scheda}")

def aumenta_settimana_gym(username):
    ref = db.reference(f'utenti/{username}/settimana')
    sett = ref.get()
    int(sett)
    sett = sett +1

    ref.set(sett)
    print(f"Settimana aggiornata per {username} alla settimana n {sett}")

def resetta_settimana_gym(username):
    ref = db.reference(f'utenti/{username}/settimana')
    sett = ref.get()
    int(sett)
    sett = sett - (sett-1)
    ref.set(sett)
    print(f"Settimana aggiornata per {username} alla settimana n {sett}")

def visualizza_settimana_gym(username):
    ref = db.reference(f'utenti/{username}/settimana')
    sett = ref.get()
    return sett