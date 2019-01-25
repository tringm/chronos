import pickle
import pandas as pd
import numpy as np
import random
import uuid
import datetime as dt
from config import root_path, in_path


# columns = ['invoice_id', 'order_id', 'customer_id', 'time', 'products_id', 'products_name', 'products_desc', 'products_quantity', 'products_unit_price', 'products_total_price', 'total_price', 'sales_rep', 'warehouse', 'distributor']
# remove total price because of nan and price range data
columns = ['id', 'order_id', 'customer_id', 'time', 'product_id', 'product_quantity', 'product_unit_price',
           'product_total_price', 'sales_rep', 'warehouse', 'distributor']


#############################################################################3
def load_data():
    # Load customers
    products_path = root_path() / 'examples' / 'io' / 'products.csv'
    products = pd.read_csv(products_path)

    # Load customers
    customers_path = root_path() / 'examples' / 'io' /'users.csv'
    customers = pd.read_csv(customers_path)


    # Load orders
    orders_path = root_path() / 'examples' / 'io' /'orders.csv'
    orders = pd.read_csv(orders_path)

    return products, customers, orders


def load_mockup_data(n_unique_names, n_unique_warehouse_names, n_unique_distributor_names):
    # Load mock up names
    mock_path = in_path() / 'mock_data' / 'pickle'

    names_pickle_filename = str(mock_path / 'names.pkl')
    with open(names_pickle_filename, 'rb') as f:
        names = pickle.load(f)
    names = names.iloc[random.sample(range(0, len(names)), n_unique_names)]['name'].tolist()
    # print(names)

    # Load mock up warehouse name
    warehouse_names_pickle_filename = str(mock_path / 'warehouse_names.pkl')
    with open(warehouse_names_pickle_filename, 'rb') as f:
        warehouse_names = pickle.load(f)
    warehouse_names = warehouse_names.iloc[random.sample(range(0, len(warehouse_names)), n_unique_warehouse_names)]['warehouse'].tolist()

    # Load mock up distributor name
    distributor_names_pickle_filename = str(mock_path / 'distributor_names.pkl')
    with open(distributor_names_pickle_filename, 'rb') as f:
        distributor_names = pickle.load(f)
    distributor_names = distributor_names.iloc[random.sample(range(0, len(distributor_names)), n_unique_distributor_names)]['distributor'].tolist()

    return names, warehouse_names, distributor_names


####################################################################################
def match_distributors_with_cities(unique_cities, distributor_names):
    """Summary
    Match unique cities with a list of distributor based on generated neighbourhood between cities
    Args:
        unique_cities (list of string): list of unique cities name
        distributor_names (list of string): list of distributor names to be chosen

    Returns:
        cities_distributors (list of stirng): list of list of distributors that match with each city
    """
    # print(unique_cities)
    has_distributor = np.random.binomial(1, .2, len(unique_cities))			#Random if a city have a designated distributor
    # print('has_distributor ', has_distributor)

    designated_distributor = []
    for i in range(len(unique_cities)):
        if has_distributor[i]:
            designated_distributor.append(distributor_names[random.randint(0, len(distributor_names) - 1)])
        else:
            designated_distributor.append("")

    # Generate neighbourhood
    adjacency_matrix = np.zeros((len(unique_cities), len(unique_cities)))
    for i in range(len(unique_cities)):
        exist_neighbours = np.sum(adjacency_matrix[i, :])
        # print('exist_neighbours', exist_neighbours)
        max_neighbours = random.randint(2, 5)
        # print('max_neighbours', max_neighbours)

        if exist_neighbours < max_neighbours:
            remaining_index = [index for index in range(0, len(unique_cities)) if (index != i) and (adjacency_matrix[i, index] == 0)]

            random_index = random.sample(remaining_index, int(max_neighbours - exist_neighbours))
            # print('random_index', random_index)
            for j in random_index:
                adjacency_matrix[i, j] = 1
                adjacency_matrix[j, i] = 1

    # print('adjacency_matrix')
    # for p in adjacency_matrix:
    # 	print(p, np.sum(p))

    neighbour_cities = []
    for i in range(len(unique_cities)):
        city = unique_cities[i]
        neighbourhood = []
        for j in range(len(unique_cities)):
            if (j != i) and (adjacency_matrix[i, j]):
                neighbourhood.append(unique_cities[j])
        neighbour_cities.append(neighbourhood)

    # print('neighbour_cities', neighbour_cities)

    cities_distributors = []
    for i in range(len(unique_cities)):
        # print(i)

        city = unique_cities[i]
        city_distributors = []

        if has_distributor[unique_cities.index(city)]:
            city_distributors.append(designated_distributor[unique_cities.index(city)])

        else:
            # finding distributor in neighbour_cities
            neighbourhood = neighbour_cities[i]
            while not city_distributors:
                # print('xD')
                # print(neighbour_cities)
                neighbours_neighbours = []
                for neighbour_city in neighbourhood:
                    if has_distributor[unique_cities.index(neighbour_city)]:
                        city_distributors.append(designated_distributor[unique_cities.index(neighbour_city)])
                    for neighbour_neighbour_city in neighbour_cities[unique_cities.index(neighbour_city)]:
                        neighbours_neighbours.append(neighbour_neighbour_city)
                neighbourhood = neighbours_neighbours

        cities_distributors.append(city_distributors)
    return cities_distributors


####################################################################################
def generate_warehouse(price_range, warehouse_names):

    #################################################
    # More random, each price range has 2 warehouse
    # random_index = random.sample(range(1, len(warehouse_names)), (len(price_range) + 1) * 2)
    # price_range_warehouses = []			# Coresponding warehouses for each price range

    # for i in range(len(price_range) + 1):
    # 	price_range_warehouses.append([warehouse_names[random_index[i * 2]], warehouse_names[random_index[i * 2 + 1]]])
    # # print('price_range_warehouses', price_range_warehouses)

    # # print(random_index)
    # remaining_index = [index for index in range(1, len(warehouse_names)) if index not in random_index]
    # # print(remaining_index)
    # remaining_warehouses = [warehouse_names[index] for index in remaining_index]
    # # print(remaining_warehouses)
    # big_warehouse = np.random.choice(remaining_warehouses)
    # # print(big_warehouse)

    #################################################
    random_index = random.sample(range(1, len(warehouse_names)), (len(price_range) + 1))
    price_range_warehouses = []			# Coresponding warehouses for each price range

    for i in range(len(price_range) + 1):
        price_range_warehouses.append(warehouse_names[random_index[i]])
    # print('price_range_warehouses', price_range_warehouses)

    # print(random_index)
    remaining_index = [index for index in range(1, len(warehouse_names)) if index not in random_index]
    # print(remaining_index)
    remaining_warehouses = [warehouse_names[index] for index in remaining_index]
    # print(remaining_warehouses)
    big_warehouse = np.random.choice(remaining_warehouses)
    # print(big_warehouse)

    return(big_warehouse, price_range_warehouses)


####################################################################################
def generate_sales_rep(names, total_order_cost_range):
    # print('generate_sales_rep')
    # print(names)
    high_spent_customer_sales_rep = random.choice(names)
    remaining_sales_rep = [name for name in names if name != high_spent_customer_sales_rep]
    # print(high_spent_customer_sales_rep)
    # print(remaining_sales_rep)

    price_range_sales_rep = [names[index] for index in random.sample(range(0, len(remaining_sales_rep)), len(total_order_cost_range))]
    # print(price_range_sales_rep)
    remaining_sales_rep = [name for name in names if ((name != high_spent_customer_sales_rep) and (name not in price_range_sales_rep))]
    # print(remaining_sales_rep)
    newly_hired_sales_rep = random.choice(remaining_sales_rep)
    # print(newly_hired_sales_rep)

    return(high_spent_customer_sales_rep, price_range_sales_rep, newly_hired_sales_rep)

####################################################################################
####################################################################################
####################################################################################
# Load data
n_unique_names = 10
n_unique_warehouse_names = 10
n_unique_distributor_names = 15

products, customers, orders = load_data()
names, warehouse_names, distributor_names = load_mockup_data(n_unique_names, n_unique_warehouse_names, n_unique_distributor_names)

# print("number of orders: ", len(orders))

####################################################################################
# Prepare
unique_orders_id = set(orders['id'].tolist())
unique_orders_id = list(unique_orders_id)
unique_cities = customers.city.unique().tolist()

cities_distributors = match_distributors_with_cities(unique_cities, distributor_names)

product_price_range = [10, 50, 200]
total_order_cost_range = [100, 500, 1000]
big_warehouse, price_range_warehouses = generate_warehouse(product_price_range, warehouse_names)

customers_spent_history = {}

high_spent_customer_sales_rep, price_range_sales_rep, newly_hired_sales_rep = generate_sales_rep(names, total_order_cost_range)

# print('sales_rep')
# print(high_spent_customer_sales_rep)
# print(price_range_sales_rep)
# print(newly_hired_sales_rep)
# print('#########################')

####################################################################################
# Generate Invoice
unique_orders_id = set(orders['id'].tolist())
unique_orders_id = list(unique_orders_id)
unique_cities = customers.city.unique().tolist()
invoices_data = []

n_orders_processed = 0

index_begin = 0
while index_begin < len(orders):
    order_id = orders.iloc[index_begin]['id']
    # print("###########################")
    # print("ORDER: ", order_id)
    index_end = index_begin
    while index_end < len(orders):
        if orders.iloc[index_end]['id'] != order_id:
            index_end -= 1
            break
        index_end += 1

    invoice_id = uuid.uuid4().hex[:10]
    customer_id = orders.iloc[index_begin]['user']

    if customer_id not in customers_spent_history:
        customers_spent_history[customer_id] = 0

    time = orders.iloc[index_begin]['time']

    matched_orders = orders[orders['id'] == order_id]

    products_id = matched_orders['product'].tolist()
    matched_products = products[products['sku'].isin(products_id)]
    products_quantity = matched_orders['quantity'].tolist()
    products_unit_price = matched_products['sale_price'].tolist()
    products_category = matched_products['category'].tolist()

    # Find product total price and add to customer spent history
    products_total_price = []
    order_total_price = 0
    for j in range(len(products_id)):
        products_total_price.append(products_unit_price[j] * products_quantity[j])
        order_total_price += products_total_price[j]
        customers_spent_history[customer_id] += products_total_price[j]


    # Pick distributor
    customer = customers[customers['id'] == customer_id]
    customer_city = customer['city'].values[0]
    distributor = np.random.choice(cities_distributors[unique_cities.index(customer_city)])


    # Pick warehouse
    warehouses = []
    for j in range(len(products_id)):
        if products_quantity[j] >= 10:
            warehouses.append(big_warehouse)
        else:
            for k in range(len(product_price_range)):
                if products_unit_price[j] <= product_price_range[k]:
                    # warehouses.append(np.random.choice(price_range_warehouses[k]))
                    warehouses.append(price_range_warehouses[k])
                    break
                if k == len(product_price_range) - 1:
                    # warehouses.append(np.random.choice(price_range_warehouses[k + 1]))
                    warehouses.append(price_range_warehouses[k + 1])


    # Pick sales_rep
    if customers_spent_history[customer_id] > 1500:
        sales_rep = high_spent_customer_sales_rep
    else:
        for k in range(len(total_order_cost_range)):
            # print(k, total_order_cost_range[k], price_range_sales_rep[k])
            if order_total_price <= total_order_cost_range[k]:
                sales_rep = price_range_sales_rep[k]
                time_datetime = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                if ((k == len(total_order_cost_range) - 1) and
                    ((time_datetime.year > 2015) or  ((time_datetime.year == 2015) and (time_datetime.month > 3)))):
                    sales_rep = newly_hired_sales_rep
                break


    n_orders_processed += len(products_id)
    index_begin = index_end + 1
    # print(len(products_id))
    # print(len(products_name))
    # print(len(products_desc))
    # print(len(products_quantity))
    # print(len(products_unit_price))
    # print(len(products_total_price))
    # print(len(warehouses))
    for j in range(len(products_id)):
        invoices_data.append([invoice_id, order_id, customer_id, time, products_id[j], products_quantity[j],
                              products_unit_price[j], products_total_price[j], sales_rep, warehouses[j], distributor])

# print('customers_spent_history', customers_spent_history)
# print('n_customers ', len(customers_spent_history))
# print(len(orders.customer_id.unique()))
# print('n_orders_processed', n_orders_processed)

#########################################################################################
#########################################################################################
#########################################################################################

# print(cities_distributors)

# invoices_data = []

# for i in range(len(unique_orders_id)):
# # for i in range(1):
# 	order_id = unique_orders_id[i]
# 	matched_orders = orders[orders['id'] == order_id]
# 	customer_id = matched_orders.iloc[0]['customer_id']
# 	time = matched_orders.iloc[0]['time']
# 	products_id = matched_orders['product_id'].tolist()
# 	matched_products = products[products['sku'].isin(products_id)]
# 	products_name = matched_products['name_title'].tolist()
# 	products_desc = matched_products['description'].tolist()
# 	products_quantity = matched_orders['quantity'].tolist()
# 	products_unit_price = matched_products['sale_price'].tolist()



# 	sales_rep = names[random.randint(0, len(names) - 1)]
# 	warehouse = warehouse_names[random.randint(0, len(warehouse_names) - 1)]
# 	distributor = distributor_names[random.randint(0, len(distributor_names) - 1)]
# 	# invoices_data.append(invoice_id, order_id, customer_id, time, products_id, products_name, products_desc, products_quantity, products_unit_price, products_total_price, total_price, sales_rep, warehouse, distributor)
# 	for j in range(len(products_id)):
# 		invoices_data.append([invoice_id, order_id, customer_id, time, products_id[j], products_name[j], products_desc[j], products_quantity[j], products_unit_price[j], products_quantity[j] * products_unit_price[j], sales_rep, warehouse, distributor])


###########################################################
invoices = pd.DataFrame(data=invoices_data, columns=columns)
invoices.to_csv((root_path()/'examples'/'io'/'invoices.csv'), index=False)
