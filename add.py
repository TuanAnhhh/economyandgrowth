import json
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
cred = credentials.Certificate('admin.json')
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': 'https://datavisual-94374.firebaseio.com'
                              }
                              )
db = firestore.client()
doc_ref = db.collection("Data")


df = pd.read_json("data.json")
for i in df.values:
    data = {"IndicatorName": i[0],
            "Year_Value": i[1]
            }
    doc_ref.add(data)
