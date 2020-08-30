from flask import Flask
import json
from models._shared import db

class Definition(db.Model):
    __tablename__ = 'definitions'
    id = db.Column(db.Integer, primary_key=True)
    part_of_speech = db.Column(db.String(160), nullable=False)
    definition = db.Column(db.String(500), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)

    def json(self):
        return {"id": self.id, "part_of_speech": self.part_of_speech, "definition": self.definition}

    def add_definition(_id, _part_of_speech, _definition, _word_id):
        new_definition = Definition(id=_id, part_of_speech=_part_of_speech, definition=_definition, word_id=_word_id)
        db.session.add(new_definition)
        db.session.commit()
    
    def doesExist(_id):
        does_exist = Definition.query.filter_by(id=_id).first()
        return bool(does_exist)
    
    def get_all_definitions():
        return [Definition.json(definition) for definition in Definition.query.all()]

    def get_definition(_id): 
        return Definition.json(Definition.query.filter_by(id=_id).first())

    def delete_definition(_id):
        is_successful = Definition.query.filter_by(id=_id).delete()
        db.session.commit()
        return bool(is_successful)
    
    def update_definition_part_of_speech(_id, _part_of_speech):
        definition_to_update = Definition.query.filter_by(id=_id).first()
        definition_to_update.part_of_speech = _part_of_speech
        db.session.commit()
    
    def update_definition_definition(_id, _definition):
        definition_to_update = Definition.query.filter_by(id=_id).first()
        definition_to_update.definition = _definition
        db.session.commit()
    
    def update_definition_word_id(_id, _word_id):
        definition_to_update = Definition.query.filter_by(id=_id).first()
        definition_to_update.word_id = _word_id
        db.session.commit()
    
    def replace_definition(_id, _part_of_speech, _definition, _word_id):
        definition_to_replace = Definition.query.filter_by(id=_id).first()
        definition_to_replace.id = _id
        definition_to_replace.definition = _definition
        db.session.commit()
    
    def __repr__(self):
        definition_object = {
            'id': self.id,
            'partOfSpeech': self.part_of_speech,
            'definition': self.definition,
            'wordId': self.word_id
        }
        return json.dumps(definition_object)

