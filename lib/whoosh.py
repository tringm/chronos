from random import choice

import whoosh.index as w_index
from whoosh.analysis import RegexTokenizer
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.lang.morph_en import variations
from whoosh.qparser import MultifieldParser
from whoosh.query import FuzzyTerm
from whoosh.scoring import *
from whoosh.collectors import TimeLimitCollector, TimeLimit

from config import in_path


def generate_schema(indexing_fields, types, is_stored):
    types = [t.lower() for t in types]

    class MySchema(SchemaClass):
        whoosh_types = {'text': TEXT, 'keyword': KEYWORD, 'id': ID, 'stored': STORED, 'numeric': NUMERIC,
                        'datetime': DATETIME, 'boolean': BOOLEAN}
        for idx, field in enumerate(indexing_fields):
            t = types[idx]
            if t not in whoosh_types:
                raise ValueError('Wrong type ', t)
            if is_stored[idx]:
                setattr(field, t(stored=True))
            else:
                setattr(field, t)

    return MySchema()


# schema = Schema(sku=TEXT(stored=True), name=TEXT(stored=True),
#                 description=TEXT(stored=True), category=TEXT(stored=True))

def create_index(schema, index_name='innominatam'):
    """
    :param schema: generated schema as class or schema
    :param index_name:
    :return:
    """
    whoosh_path = in_path() / 'whoosh'
    storage = FileStorage(str(whoosh_path))
    version = 0
    while w_index.exists(storage, index_name):
        index_name+= 'v' + str(version)
        version += 1
    ix = storage.create_index(schema, index_name)
    return ix


def add_document_dict_rows(ix, rows):
    """
    
    :param ix: whoosh index
    :param rows: rows as list of dictionary
    :return: 
    """
    # TODO: rows as pandas
    # TODO: check with ix schema
    writer = ix.writer()
    for r in rows:
        writer.add_documents(**r)
    writer.commit()


def query(indexer, search_term, fields, limit=10, scoring_method=None, fuzzy=True):
    all_scoring_methods = {'tfidf': TF_IDF()}
    if scoring_method:
        searcher = indexer.searcher(weighting=all_scoring_methods[scoring_method])
    else:
        searcher = indexer.searcher()
    if fuzzy:
        parser = MultifieldParser(fields, schema=indexer.schema, termclass=FuzzyTerm)
    else:
        parser = MultifieldParser(fields, schema=indexer.schema)
    q = parser.parse(search_term)
    c = searcher.collector(limit=limit)
    tlc = TimeLimitCollector(c, timelimit=3.0)
    try:
        searcher.search_with_collector(q=q, collector=tlc)
    except TimeLimit:
        print('Search too long')
    return tlc.results()


def transform_search_term(search_term):
    tokenizer = RegexTokenizer()
    terms_tokenized = tokenizer(search_term)
    new_search_terms = []
    for idx, token in enumerate(terms_tokenized):
        varied_words = list(variations(token.text))
        new_search_terms.append(choice(varied_words))
    return ' '.join(new_search_terms)
