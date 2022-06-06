# Imports
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import json
from pprint import PrettyPrinter
# Env variables load and declaration
load_dotenv(find_dotenv())
mongo_pwd = os.environ.get('MONGODB_PWD')
# Global variables
printer = PrettyPrinter()
# Mongo connection
connection_string = f'mongodb+srv://WiktorB2004:{mongo_pwd}@data.g6nqmlw.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
# Database and questions collection
db = client.db
question = db.question

# Matches similar values to query in path and print them
def fuzzy_matching():
    result = question.aggregate([
        {
            '$search': {
                'index': 'language_search',
                'text': {
                    'query': 'computer',
                    'path': 'category',
                    'fuzzy': {}
                }
            }
        }
    ])
    printer.pprint(list(result))

# Matches using available in DB collection synonyms and print them
def synonyms_matching():
    result = question.aggregate([
        {
            '$search': {
                'index': 'language_search',
                'text': {
                    'query': 'computer',
                    'path': 'category',
                    'synonyms': 'mapping'
                }
            }
        }
    ])
    printer.pprint(list(result))
    
# Autocomplete questions which has similar phrase to query and print them
def autocomplete():
    result = question.aggregate([
        {
            '$search':{
                'index': 'language_search',
                'autocomplete': {
                    'query': 'computer programmer',
                    'path': 'question',
                    'tokenOrder': 'sequential',
                    'fuzzy': {}
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'question': 1
            }
        }
    ])
    printer.pprint(list(result))
    
# Matches using compound terms and print found elements
def compount_queries():
    result = question.aggregate([
        {
            '$search': {
                'index': 'language_search',
                'compound': {
                    'must': [
                        {
                            'text': {
                                'query': ['COMPUTER', 'CODING'],
                                'path': 'category'
                            }
                        }
                    ],
                    'mustNot': [{
                            'text': {
                                'query': 'codes',
                                'path': 'category'
                            }
                    }],
                    'should': [
                        {
                            'text': {
                                'query': 'application',
                                'path': 'answer'
                            }
                        }
                    ]
                }
            }
        },
            {'$project': {
                'question': 1,
                'answer': 1,
                'category': 1,
                'score': {'$meta': 'searchScore'}
            }
        }
    ])
    printer.pprint(list(result))
    
    
def relevance():
    result = question.aggregate([
        {
            '$search': {
                'index': 'language_search',
                'compound': {
                    'must': [
                        {
                            'text': {
                                'query': 'geography',
                                'path': 'category'
                            }
                        },
                    ],
                    'should': [
                        {
                            'text': {
                                'query': 'Final Jeopardy',
                                'path': 'round',
                                'score': {'boost': {'value': 3.0}}
                            }
                        },
                        {
                            'text': {
                                'query': 'Double Jeopardy',
                                'path': 'round',
                                'score': {'boost': {'value': 2.0}}
                            }
                        }
                    ]
                }
            }
        },
        {
            '$project': {
                'question': 1,
                'answer': 1,
                'category': 1,
                'round': 1,
                'score': {'$meta': 'searchScore'}
            }
        }, 
        {
            '$limit': 10
        }
    ])
    printer.pprint(list(result))
    
relevance()