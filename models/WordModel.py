from flask import Flask
import json
from models._shared import db

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(160), nullable=False)
    definitions = db.relationship('Definition', backref='words', lazy=True)

    def json(self):
        return {"id": self.id, "word": self.word, "definitions": [definition.json() for definition in self.definitions]}

    def doesExist(_id):
        does_exist = Word.query.filter_by(id=_id).first()
        return bool(does_exist)
    
    def add_word(_id, _word):
        new_word = Word(id=_id, word=_word)
        db.session.add(new_word)
        db.session.commit()
    
    def get_all_words():
        return [Word.json(word) for word in Word.query.all()]
    
    def get_word(_id):  
        return Word.json(Word.query.filter_by(id=_id).first())

    def delete_word(_id):
        is_successful = Word.query.filter_by(id=_id).delete()
        db.session.commit()
        return bool(is_successful)

    def replace_word(_id, _word):
        word_to_replace = Word.query.filter_by(id=_id).first()
        word_to_replace.word = _word
        db.session.commit()

    def __repr__(self):
        word_object = {
            'id': self.id,
            'word': self.word,
            'definitions': self.definitions
        }
        return json.dumps(word_object)

