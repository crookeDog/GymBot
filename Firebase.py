import firebase_admin
from firebase_admin import credentials, db

# Percorso corretto al file delle credenziali scaricato
cred = credentials.Certificate(r"my_credentials.json")

# Inizializzazione dell'app Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'my_database_url'
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

