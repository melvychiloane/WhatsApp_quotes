import requests
from dotenv import load_dotenv
import random
import os

valid_categories_list = [
    "age", "alone", "amazing", "anger", "architecture", "art", "attitude", 
    "beauty", "best", "birthday", "business", "car", "change", "communication", 
    "computers", "cool", "courage", "dad", "dating", "death", "design", "dreams", 
    "education", "environmental", "equality", "experience", "failure", "faith", 
    "family", "famous", "fear", "fitness", "food", "forgiveness", "freedom", 
    "friendship", "funny", "future", "god", "good", "government", "graduation", 
    "great", "happiness", "health", "history", "home", "hope", "humor", 
    "imagination", "inspirational", "intelligence", "jealousy", "knowledge", 
    "leadership", "learning", "legal", "life", "love", "marriage", "medical", 
    "men", "mom", "money", "morning", "movies", "success"
]

def is_valid_category(category):
    if category.lower() in valid_categories_list:
        return True
    return False

def random_categories():
    cat_list = []
    for i in range(5):
        rand_num = random.randint(0,len(valid_categories_list)-1)
        if valid_categories_list[rand_num] not in cat_list:
            cat_list.append(valid_categories_list[rand_num])
    return cat_list
    
def get_a_Quote(category):
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get("API_KEY")})
    if response.status_code == requests.codes.ok:
        print(response.json())
        return response.json()
    else:
        print("Error:", response.status_code, response.text)

