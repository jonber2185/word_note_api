import errors.base as _errors
from db import modules as _db_modules


from db.modules.words import getWords

def getWordsDetail(words: list) -> list:
    if words == [] or words is None: 
        raise _errors.WordError("words is required")
    
    return _db_modules.words.getWordsDetail(words)

def setWords(set_id, words):
    if words == []: raise _errors.WordError("words is required")
    error_words = []
    for word in words:
        word_id = word.get("word_id")
        meaning = word.get('meaning', "")

        try:
            int(meaning)
            if word_id is None: raise TypeError
            if _db_modules.words.get_detail(word_id) is None: raise TypeError
            if _db_modules.words.getWord(
                set_id=set_id, 
                word_id=word_id
            ) is not None: raise TypeError
        except (TypeError): 
            error_words.append(word)
            continue
        
        _db_modules.words.setWord(
            set_id=set_id,
            word_id=word_id,
            meaning=meaning
        )
    if len(error_words) != 0:
        raise _errors.WordError(
            message="Invalid 'id' or 'meaning' value.",
            payload={ "error_data": error_words }
        )
    
def updateWords(set_id, words):
    if words == []: raise _errors.WordError("words is required")
    error_words = []
    for word in words:
        word_id = word.get("word_id")
        meaning = word.get('meaning', "")

        try:
            int(meaning)
            if word_id is None: raise TypeError
            if _db_modules.words.get_detail(word_id) is None: raise TypeError
        except TypeError: 
            error_words.append(word)
            continue

        _db_modules.words.updateWord(
            meaning=meaning,
            set_id=set_id,
            word_id=word_id
        )

        
    if len(error_words) != 0:
        raise _errors.WordError(
            message="Invalid 'id' or 'meaning' value.",
            payload={ "error_data": error_words }
        )
    
def deleteWords(set_id, word_ids):
    if not isinstance(word_ids, list): raise _errors.WordError("word_ids must be list")
    elif word_ids == []: return
    _db_modules.words.deleteWords(set_id, word_ids)
