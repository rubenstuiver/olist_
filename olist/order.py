import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=False):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """

        orders = self.data['corders'].copy()

        # filter delivered orders
        if is_delivered:
            orders = orders.query("order_status=='delivered'").copy()



        # handle datetime
        orders.loc[:, 'order_delivered_customer_date'] = \
            pd.to_datetime(orders['order_delivered_customer_date'])
        orders.loc[:, 'order_estimated_delivery_date'] = \
            pd.to_datetime(orders['order_estimated_delivery_date'])
        orders.loc[:, 'order_purchase_timestamp'] = \
            pd.to_datetime(orders['order_purchase_timestamp'])

        # compute delay vs expected
        orders.loc[:, 'delay_vs_expected'] = \
            (orders['order_delivered_customer_date'] -
             orders['order_estimated_delivery_date']) / np.timedelta64(24, 'h')

        def handle_delay(x):
            # only keep delay where wait_time longer than expected
            if x > 0:
                return x
            else:
                return 0

        orders.loc[:, 'delay_vs_expected'] = \
            orders['delay_vs_expected'].apply(handle_delay)

        # compute wait time
        orders.loc[:, 'wait_time'] = \
            (orders['order_delivered_customer_date'] -
             orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

        # compute expected wait time
        orders.loc[:, 'expected_wait_time'] = \
            (orders['order_estimated_delivery_date'] -
             orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

        return orders[[
            'order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
            'order_status'
        ]]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        # import data
        reviews = self.data['order_reviews']

        def dim_five_star(d):
            if d == 5:
                return 1
            else:
                return 0

        def dim_three_star(d):
            if d == 3:
                return 1
            else:
                return 0

        def dim_two_star(d):
            if d == 2:
                return 1
            else:
                return 0

        def dim_one_star(d):
            if d == 1:
                return 1
            else:
                return 0

        reviews.loc[:, 'dim_is_five_star'] =\
            reviews['review_score'].apply(dim_five_star)

        reviews.loc[:, 'dim_is_three_star'] =\
            reviews['review_score'].apply(dim_three_star)

        reviews.loc[:, 'dim_is_two_star'] =\
            reviews['review_score'].apply(dim_two_star)

        reviews.loc[:, 'dim_is_one_star'] =\
            reviews['review_score'].apply(dim_one_star)

        return reviews[[
            'order_id', 'dim_is_five_star','dim_is_three_star','dim_is_two_star','dim_is_one_star', 'review_score'
        ]]

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        data = self.data
        products = \
            data['order_items']\
            .groupby('order_id',
                     as_index=False).agg({'order_item_id': 'count'})
        products.columns = ['order_id', 'number_of_products']
        return products

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        data = self.data
        sellers = \
            data['order_items']\
            .groupby('order_id')['seller_id'].nunique().reset_index()
        sellers.columns = ['order_id', 'number_of_sellers']

        return sellers


    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """

        data = self.data
        price_freight = \
            data['order_items']\
            .groupby('order_id',
                     as_index=False).agg({'price': 'sum',
                                          'freight_value': 'sum'})

        return price_freight
