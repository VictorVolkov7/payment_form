import os

import stripe


def stipe_payment_created(object_, stripe_price):
    """
    Create a stripe session with discount.
    """
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    if hasattr(object_, 'discount') and object_.discount:
        discount = object_.discount.discount

        coupon = stripe.Coupon.create(
            percent_off=discount,
            duration="once",
        )

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': object_.name,
                    },
                    "unit_amount_decimal": stripe_price
                },
                'quantity': 1,
            }],
            discounts=[{
                'coupon': coupon.id
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
    else:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': object_.name,
                    },
                    "unit_amount_decimal": stripe_price
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )

    return session

