import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('gita-daily-ee5f6-25032c526a9d.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


doc_ref = db.collection(u'json').stream()
user = dict()
i = 1
for doc in doc_ref:
    print(i)
    i = i + 1
    document = db.collection(u'json').document(doc.id).get().to_dict()['data']
    print(document)
    for key in document.keys():
        user[key] = document[key]

print(user)