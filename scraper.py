#import what we are going to use
import requests
import lxml.html as html
import json


LIST_OF_LINKS = []

def get_drink_links():
    global LIST_OF_LINKS
    XPATH_LINK_TO_ARTICLE_DRINK = '//a[@class="recipeCard__titleLink"]/@href'

    for i in range(10):
        try:
            PAGES_OF_DRINKS = i + 1
            PAGE_LIST_DRINKS = f'https://www.allrecipes.com/element-api/content-proxy/aggregate-load-more?sourceFilter=alrcom&id=cms%2Fonecms_posts_alrcom_2002925&excludeIds=cms%2Fonecms_posts_alrcom_214367&page={PAGES_OF_DRINKS}&orderBy=Popularity30Days&docTypeFilter=content-type-recipe&size=24&pagesize=24&x-ssst=iTv629LHnNxfbQ1iVslBTZJTH69zVWEa&variant=food'

            response = requests.get(PAGE_LIST_DRINKS)
            if response.status_code == 200:
                home = response.content.decode('utf-8')
                jsonify = json.loads(home)
                htmlString = jsonify["html"]
                home_parsed = html.fromstring(htmlString)
                links_to_drinks = home_parsed.xpath(
                    XPATH_LINK_TO_ARTICLE_DRINK)
                LIST_OF_LINKS = LIST_OF_LINKS + links_to_drinks

            else:
                raise ValueError(f'Error: {response.status_code}')

        except ValueError as ve:
            print(ve)

def get_recipes_info():
    START_ID = 1000000
    DATA = []
    XPATH_TITLE_RECIPE = '//div[@class="intro article-info"]/div/h1[@class="headline heading-content"]/text()'
    XPATH_LIST_INGREDIENTS = '//ul[@class="ingredients-section"]/li[@class="ingredients-item"]/label/span/span[@class="ingredients-item-name"]/text()'
    for i in range(len(LIST_OF_LINKS)):
        try:
            response = requests.get(LIST_OF_LINKS[i])
            if response.status_code == 200:
                article_recipe_html = response.content.decode('utf-8')
                recipe_parsed = html.fromstring(article_recipe_html)
                title = recipe_parsed.xpath(XPATH_TITLE_RECIPE)[0]
                ingrediends = recipe_parsed.xpath(XPATH_LIST_INGREDIENTS)

                cleanList = []
                for ingredient in ingrediends:
                    ingredient = " ".join(ingredient.split())
                    cleanList.append(ingredient)
                obj = {
                    "id": START_ID,
                    "name": title,
                    "ingredients": cleanList}
                DATA.append(obj)
                START_ID = START_ID + 1

            else:
                raise ValueError(f'Error: {response.status_code}')

        except ValueError as ve:
            print(ve)
    with open(f'data.json', 'w', encoding='utf-8') as f:
      f.write(str(DATA))

def run():
    get_drink_links()
    get_recipes_info()


if __name__ == '__main__':
    run()


