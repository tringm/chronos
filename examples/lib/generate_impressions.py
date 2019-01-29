from pprint import pprint

import uuid
import pandas as pd
from whoosh.analysis import *
from whoosh.fields import *
from whoosh.index import create_in, open_dir
from numpy import random
from config import root_path
from lib.whoosh import query
from whoosh.lang.morph_en import variations

products = pd.read_csv((root_path() / 'examples' / 'io' / 'products.csv'), delimiter=',')
orders = pd.read_csv((root_path() / 'examples' / 'io' / 'orders.csv'), delimiter=',')


def init_indexer():
    schema = Schema(sku=TEXT(stored=True), name=TEXT(analyzer=LanguageAnalyzer('en')),
                    description=TEXT(analyzer=LanguageAnalyzer('en')),
                    category=TEXT(analyzer=LanguageAnalyzer('en')))
    ix = create_in(str(root_path() / 'examples' / 'whoosh'), schema)
    w = ix.writer()
    for idx, row in products.iterrows():
        w.add_document(sku=row['sku'], name=row['name'], description=row['description'], category=row['category'])
        # w.add_document(sku=row['sku'], description=row['description'])
    w.commit()
    return ix


def load_indexer():
    return open_dir(str(root_path() / 'examples' / 'whoosh'))


def search_term_from_name(name):
    tokenizer = RegexTokenizer()
    terms_tokenized = tokenizer(name)
    search_term = []
    for idx, token in enumerate(terms_tokenized):
        is_included = random.binomial(1, 0.3)
        if is_included:
            varied_words = list(variations(token.text))
            search_term.append(random.choice(varied_words))
    return ' '.join(search_term)


impressions = []

indexer = load_indexer()
fields = ['name', 'description', 'category']

extra_impressions = 0

for idx, order in orders.iterrows():
    print(idx)
    user_id = order['user']
    prod = products[products['sku'] == order['product']]
    search_term = search_term_from_name(prod.iloc[0]['name'])

    # Bought product
    impressions.append({'id': len(impressions), 'user': user_id, 'query': search_term, 'product': prod.iloc[0]['sku'],
                        'click': True, 'purchase': True})
    n_limit = random.randint(1, 10)
    results = query(indexer=indexer, search_term=search_term, fields=fields, scoring_method='tfidf', limit=n_limit)

    for r in results:
        extra_impressions += 1
        is_clicked = bool(random.binomial(1, 0.6))
        impressions.append({'id': len(impressions), 'user': user_id, 'query': search_term,
                            'product': r['sku'], 'click': is_clicked, 'purchase': False})

print(extra_impressions)

impressions_df = pd.DataFrame(impressions)
impressions_df = impressions_df[['id', 'user', 'query', 'product', 'click', 'purchase']]
impressions_df.to_csv((root_path() / 'examples' / 'io'/ 'impressions.csv'), index=False)