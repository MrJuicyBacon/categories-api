# categories-api

Simple API project example in Django framework with DRF.

## Requirements
* Required python version: 3.6+
* Dependencies: `Django==2.2.7`, `djangorestframework==3.10.3`

## Usage
Before running, install dependencies (`pip install -r requirements.txt`)  
To run, migrate with `manage.py migrate`, then use `manage.py runserver [<ip>:<port>]`.


### Endpoints
1. `GET /categories/<id>/`:  
Returns a response with JSON serialized category object with the following fields: `id`, `name`, `parents`, `children`, `siblings`.

2. `POST /categories/`:  
Accepts JSON serialized category object with the following fields:  
-`name`: category name  
-`children`: children category object (any nesting depth)  
Returns JSON serialized category object that's been created with the following fields: `id`, `name`, `parents`, `children`, `siblings` in case of success, error with the description otherwise.


### Examples
Request:  
```
POST /categories/
```
```json
{
    "name": "Category 1",
    "children": [
        {
            "name": "Category 1.1",
            "children": [
                {
                    "name": "Category 1.1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1.1"
                        },
                        {
                            "name": "Category 1.1.1.2"
                        },
                        {
                            "name": "Category 1.1.1.3"
                        }
                    ]
                },
                {
                    "name": "Category 1.1.2",
                    "children": [
                        {
                            "name": "Category 1.1.2.1"
                        },
                        {
                            "name": "Category 1.1.2.2"
                        },
                        {
                            "name": "Category 1.1.2.3"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Category 1.2",
            "children": [
                {
                    "name": "Category 1.2.1"
                },
                {
                    "name": "Category 1.2.2",
                    "children": [
                        {
                            "name": "Category 1.2.2.1"
                        },
                        {
                            "name": "Category 1.2.2.2"
                        }
                    ]
                }
            ]
        }
    ]
}
```
Response:
```json
{"id":1,"name":"Category 1","parents":[],"children":[{"id":2,"name":"Category 1.1"},{"id":11,"name":"Category 1.2"}],"siblings":[]}
```
---
Request:
```
GET /categories/8/
```
Response:
```json
{"id":8,"name":"Category 1.1.2.1","parents":[{"id":7,"name":"Category 1.1.2"},{"id":2,"name":"Category 1.1"},{"id":1,"name":"Category 1"}],"children":[],"siblings":[{"id":9,"name":"Category 1.1.2.2"},{"id":10,"name":"Category 1.1.2.3"}]}
```
