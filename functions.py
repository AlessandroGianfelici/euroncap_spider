import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def find_key_section(all_sections, key):
    return map(str, filter(lambda x : key in str(x), all_sections))


def find_value_in_section(key_section):
    try:
        str_value = list(filter(lambda x : 'value' in x, concatenate_vector(key_section).split('\n')))[0]
        return int(re.findall('[0-9]+', str_value)[0])
    except:
        return None

def concatenate_vector(key_section):
    return str("\n".join(list(key_section)))

def get_car_name(html_soup):
    return str(html_soup.find('h1')).replace('<h1 class="car-name">', "").replace("</h1>", "")

def isolate_key(key, html_soup):
    return list(filter(lambda x: key in x, map(str, html_soup.find_all('p'))))

def get_kerb_weight(html_soup):
    try:
        return int(re.search(r'([0-9]+(kg))', isolate_key('Kerb Weight', html_soup)[0]).group(1).replace("kg",""))
    except Exception as e:
        print(e)
        return None
    
def get_body_type(html_soup):
    try:
        body_type = isolate_key('Body Type', html_soup)[0]
        parsed_html = BeautifulSoup(body_type)
        return parsed_html.body.find('span', attrs={'class':'tcol2'}).text
    except Exception as e:
        print(e)
        return None    
    
def get_VIN_included_in_test(html_soup):
    try:
        body_type = isolate_key('VIN From Which Rating Applies', html_soup)[0]
        parsed_html = BeautifulSoup(body_type)
        return parsed_html.body.find('span', attrs={'class':'tcol2'}).text
    except Exception as e:
        print(e)
        return None    
    
def get_year_of_publication(html_soup):
    try:
        body_type = isolate_key('Year Of Publication', html_soup)[0]
        parsed_html = BeautifulSoup(body_type)
        return parsed_html.body.find('span', attrs={'class':'tcol2'}).text
    except Exception as e:
        print(e)
        return None
    
def get_car_class(html_soup):
    try:
        body_type = isolate_key('Class', html_soup)[0]
        parsed_html = BeautifulSoup(body_type)
        return parsed_html.body.find('span', attrs={'class':'tcol2'}).text
    except Exception as e:
        print(e)
        return None
    
def get_star_number(html_soup):
    my_str = html_soup.find('div', attrs={'class':'stars'})
    return int(re.search(r'((stars)+[0-9])', 
                         str(html_soup.find('div', 
                                            attrs={'class':'stars'}))).group(1).replace('stars', ''))

def get_model_year(html_soup):
    return int(re.search(r'(("year">)[0-9]+)', 
                         str(html_soup.find('div', 
                                            attrs={'class':'year'}))).group(1).replace('"year">', ''))


def parse_car(resp_body):
    html_soup = BeautifulSoup(resp_body, 'html.parser')
    all_sections = html_soup.find_all('li')

    keys = ["Vulnerable Road Users",
            "Pedestrian",
            "Adult Occupant",
            "Child Occupant",
            "Safety Assist"]

    get_results = lambda key : find_value_in_section(find_key_section(all_sections, key))

    car_name = {'Car Name' : [get_car_name(html_soup)]}
    model_year = {'Model Year' : [get_model_year(html_soup)]}

    kerb_weight = {'Kerb Weight [kg]' : [get_kerb_weight(html_soup)]}
    body_type = {'Body Type' : [get_body_type(html_soup).replace("- ", "")]}
    year_of_publication = {'Year Of Publication' : [get_year_of_publication(html_soup)]}
    car_class = {'Class' : [get_car_class(html_soup)]}
    VIN_included_in_test = {'VIN range' : [get_VIN_included_in_test(html_soup).replace("- ", "")]}
    stars_number = {'Overall Valuation' : [get_star_number(html_soup)]}


    results = {key + ' Score': [get_results(key)] for key in keys}

    return pd.DataFrame(car_name | 
             model_year |
             body_type |
             kerb_weight | 
             car_class |
             VIN_included_in_test |
             results |
             stars_number |
             year_of_publication)                                            