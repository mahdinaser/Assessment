How many orders were completed in 2018? 9227
## The definition of "completed" is not clear, I assumed that it doesn't relate to "return" field
## Otherwise, we can set "returned=False" to only consider items that have not been returned

select count(*)
from orders
where 
CAST(SUBSTR(order_timestamp, 1, 4) AS integer)==2018 

## and returned=="False"


How many orders were completed in 2018 containing at least 10 units? 29120

select  count(*)
from orders, line_items
where 
CAST(SUBSTR(order_timestamp, 1, 4) AS integer)==2018 
AND
orders.order_id == line_items.order_id
AND
quantity>='10'

How many customers have ever purchased a medium sized sweater with a discount?
753
### this value is number of costumer that at least one time bought the sweater
### we can remove the distinct function to get total number of items that have been bought 

select  count(distinct(customers.customer_uid))
from customers , orders , line_items 
where discount!='0.0'
AND
customers.customer_uid = orders.customer_uid
AND
line_items.order_id = orders.order_id
AND
product_category=='Sweater'
AND
size = 'M'

How profitable was our most profitable month? May

## I defined profit with the below equation, what customer paid - what we paid
## That should give us revenue - cost 
'Profit == What customer paid - What we paid
'(selling_price + shipping_revenue) - (shipping_cost + supplier_cost)

select ((selling_price + shipping_revenue) - (shipping_cost + supplier_cost)) as profit, CAST(SUBSTR(order_timestamp, 6, 7) AS integer) as month, order_timestamp
from line_items, orders
where
orders.order_id = line_items.order_id
group by month
order by profit desc

### output:
Profit Month
6.31	5
-1.92	4
-1.95	6
-2.13	7
-4.21	1
-4.95	2
-5.77	12
-7.33	9
-7.39	10
-7.81	11
-12.16	3
-12.33	8

What is the return rate for business vs. non-business customers?



select is_business ,  returned , count(*) 
from orders,customers
where orders.customer_uid = customers.customer_uid
group by is_business,returned


is_business     returned    count
False	        False	    17378
False	        True	    900
True	        False	    26256
True	        True	    1899


900 / 17378 non-business rate of returned => ~5%
1899/26256 business rate of returned => ~7%
