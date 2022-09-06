from ctypes import cast
from os import environ
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError
import pandas as pd

while True:
    try:
        psql_engine = create_engine(environ["POSTGRESQL_CS"], pool_pre_ping=True, pool_size=10)
        break
    except OperationalError:
        sleep(0.1)
print('Connection to PostgresSQL successful.')

# Question 1
# First computed frequency of different film catagories for each customer by joining all the relevant tables by creating CTE t1,
# then calculated personal favourite category for each customer
# At the last computed the five favorite categories for most number of customers

sql_query1 = """

                WITH t1 AS (
                    SELECT c4.customer_id, c4.first_name, category.category_id, category.name as category_name, 
                           COUNT(category.category_id) as count_category  
                    FROM(
                        SELECT c3.customer_id, c3.first_name, c3.email, film_category.category_id, film_category.film_id 
                        FROM (
                            SELECT c2.customer_id, c2.first_name, c2.email, c2.rental_id, c2.inventory_id, c2.film_id 
                            FROM(
                                SELECT c1.customer_id, c1.first_name, c1.email, c1.rental_id, inventory.inventory_id, inventory.film_id 
                                FROM (
                                    SELECT customer.customer_id, customer.first_name, customer.email, rental.rental_id, rental.inventory_id 
                                    FROM customer 
                                    LEFT JOIN rental ON customer.customer_id = rental.customer_id) c1
                                LEFT JOIN inventory ON c1.inventory_id= inventory.inventory_id) c2
                            LEFT JOIN film ON c2.film_id= film.film_id) c3
                        LEFT JOIN film_category ON c3.film_id= film_category.film_id) c4
                    LEFT JOIN category ON c4.category_id= category.category_id
                    GROUP BY c4.customer_id, c4.first_name, category.name, category.category_id
                    ORDER BY c4.customer_id, count_category DESC)


                SELECT category_name, COUNT(customer_id) AS no_of_cusomters
                FROM (
                     SELECT DISTINCT ON (customer_id)
                            customer_id, category_id, first_name, category_name, count_category
                     FROM t1 
                     ) t2
                GROUP BY category_name
                ORDER BY no_of_cusomters DESC
                Limit 5
                
            """

try:
    df_fav_category = pd.read_sql_query(sql_query1 , con=psql_engine)
    print("Question 1: Top 5 customer favourite categories")
    print(df_fav_category)
except (OperationalError, ProgrammingError) as e:
    print('Error occured while pulling data from PostgreSQL {}'.format(e.args))


# Question 2
# The percentage for each film title was calculated seprately for both years 2005 and 2006, based on the rental in each year divided by total rental.

sql_query2 = """ 

                WITH t1 AS (
                    SELECT film_inventory.film_id, film_inventory.title, 
                           EXTRACT(year FROM rental_date) as year,  
                           1.0 * COUNT(rental.rental_id) as count_rental 
                    FROM (
                         Select film.film_id, film.title, inventory.inventory_id 
                         FROM film 
                         LEFT JOIN inventory ON film.film_id = inventory.film_id) film_inventory
                    LEFT JOIN rental ON film_inventory.inventory_id=rental.inventory_id
                    WHERE EXTRACT(year FROM rental_date) BETWEEN '2005' and '2006'
                    GROUP BY film_inventory.film_id, film_inventory.title, EXTRACT(year from rental_date))
                
                SELECT film_id, title, year, count_rental, 
                       (count_rental)/(SUM(count_rental) OVER (PARTITION BY title)) as rental_percentage 
                FROM t1

            """ 

try:
    df_rental_percentage= pd.read_sql_query(sql_query2 , con=psql_engine)
    print("Question 2: The percentage of rental for each film title between the year 2005 and 2006")
    print(df_rental_percentage)
except (OperationalError, ProgrammingError) as e:
    print('Error occured while pulling data from PostgreSQL {}'.format(e.args))