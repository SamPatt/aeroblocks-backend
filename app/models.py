from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, DictField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class CanvasState(EmbeddedDocument):
    name = StringField(required=True)
    data = DictField()  
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(CanvasState, self).save(*args, **kwargs)

class User(Document):
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    canvases = ListField(EmbeddedDocumentField(CanvasState))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)