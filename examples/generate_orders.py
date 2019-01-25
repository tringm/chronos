import pandas as pd
from config import root_path
import random
import numpy as np
from examples.lib.helper import divide_by_proportion, random_date_time
from math import ceil
import uuid

### Load Data
users_path = root_path() / 'examples' / 'io' / 'users.csv'
users_data = pd.read_csv(users_path, delimiter=',')

products_path = root_path() / 'examples' / 'io' / 'products.csv'
products = pd.read_csv(products_path, delimiter=',')

### Generate users and budgets
USER_PROP = 0.8
n_user = ceil(users_data.shape[0] * USER_PROP)
users = users_data.sample(n_user)

budgets = [(100, 200), (300, 500), (600, 1000), (1000, 1500), (2000, 5000)]
budgets_proportion = [0.4, 0.2, 0.2, 0.1, 0.1]
n_user_by_budget = divide_by_proportion(budgets_proportion, n_user)

users_budgets = [np.random.randint(budgets[idx][0], budgets[idx][1], n_user_by_budget[idx])
                 for idx in range(len(budgets))]
users_budgets = np.concatenate(users_budgets, axis=0)
random.shuffle(users_budgets)

products_categories = list(products.category.unique())

orders = []

for idx in range(n_user):
    user = users.iloc[idx]
    n_orders = random.randint(1, 20)
    interests = random.sample(products_categories, 20)
    main_interest = interests[:12]
    sub_interest = interests[12:]
    products_in_main_interest = products[products['category'].isin(main_interest)]
    products_in_sub_interest = products[products['category'].isin(sub_interest)]
    u_budget = users_budgets[idx]

    for order_idx in range(n_orders):
        order_id = uuid.uuid4().hex[:10]

        # Generate datetimes
        datetime = random_date_time()

        order_total = 0
        chosen_products = set()

        while order_total <= u_budget:
            is_main_interest = np.random.binomial(1, .7)
            while True:
                if is_main_interest:
                    product = products_in_main_interest.sample(1)
                else:
                    product = products_in_sub_interest.sample(1)
                product_sku = product.iloc[0]['sku']
                if product_sku not in chosen_products:
                    chosen_products.add(product_sku)
                    break
            product_price = product.iloc[0]['sale_price']
            if product_price > u_budget:
                quantity = 1
            else:
                quantity = random.randint(1, 10)
            order_total += float(product['sale_price']) * quantity
            orders.append({'id': order_id, 'user': user['id'], 'product': product.iloc[0]['sku'],
                           'quantity': quantity, 'time': datetime})

orders_df = pd.DataFrame(orders)
orders_df = orders_df.sort_values(by='time')
orders_df = orders_df[['id', 'user', 'product', 'quantity', 'time']]
orders_df.to_csv((root_path() / 'examples' / 'io'/ 'orders.csv'), index=False)
