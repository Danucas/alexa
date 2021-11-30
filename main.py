from rappi_api import Rappi

if __name__ == '__main__':
    rappi = Rappi()
    # try:
    #     rappi.login('3176923716', 'SMS')
    # except Exception as e:
    #     print(e)
    
    try:
        categories = rappi.list_food_categories()
        index = int(input('categories: {}'.format(", ".join([f'{i}. {n[1]}' for i, n in enumerate(categories)]))))
        restaurants = rappi.list_restaurants(category=categories[index][1])
        print(restaurants)
    except Exception as e:
        print(e)

