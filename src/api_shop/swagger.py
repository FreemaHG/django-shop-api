from drf_yasg import openapi


filter_param = openapi.Parameter(
    'filter',
    openapi.IN_QUERY,
    description="search text",
    type=openapi.TYPE_OBJECT,
    value={
          "name": "string",
          "minPrice": 0,
          "maxPrice": 0,
          "freeDelivery": False,
          "available": True
        }
)

category = openapi.Parameter(
    'category',
    openapi.IN_QUERY,
    description="id category",
    type=openapi.TYPE_NUMBER,
    default=1
)

sort = openapi.Parameter(
    'sort',
    openapi.IN_QUERY,
    description="Available values: rating, price, reviews, date",
    type=openapi.TYPE_STRING,
    default="date",
    enum=["rating", "price", "reviews", "date"]
)

sortType = openapi.Parameter(
    'sortType',
    openapi.IN_QUERY,
    description="Available values: dec, inc",
    type=openapi.TYPE_STRING,
    default="dec",
    enum=["dec", "inc"]
)

limit = openapi.Parameter(
    'limit',
    openapi.IN_QUERY,
    type=openapi.TYPE_NUMBER,
    default=20
)

basket_data = openapi.Parameter(
    'data',
    openapi.IN_QUERY,
    type=openapi.TYPE_OBJECT,
    value={
          "id": 123,
          "count": 5
        }
)

order_id = openapi.Parameter(
    'id',
    openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description="order id"
)
