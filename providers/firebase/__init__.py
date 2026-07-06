import firebase_admin
from firebase_admin import credentials, firestore, storage
from core.config import settings

# Inicialización única de Firebase
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'storageBucket': f"{settings.FIREBASE_PROJECT_ID}.appspot.com"
            })
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            return None, None
            
    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket

db, bucket = initialize_firebase()

# --- PUENTE DE COMPATIBILIDAD PARA MÓDULOS LEGADOS ---
# Exportamos EXACTAMENTE lo que los archivos viejos (apps/user, apps/product, etc) están buscando
if db:
    user_collection = db.collection('users')
    products_collection = db.collection('products')
    # Por si acaso algún archivo lo busca en singular:
    product_collection = db.collection('products')
else:
    user_collection = None
    products_collection = None
    product_collection = None

# También exportamos db y bucket para uso general
db = db
bucket = bucket
