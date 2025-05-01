-- # 103 Intermediate SQL
-- # 1. Intersect and Except
SELECT b.id FROM book_shop b
INTERSECT
SELECT f.id FROM favourite_book f;

SELECT b.id FROM book_shop b
EXCEPT
SELECT f.id FROM favourite_book f;

-- # 2. Union & Union All
SELECT * FROM book_shop
UNION ALL
SELECT * FROM book_shop_new
ORDER BY 3 DESC;

SELECT * FROM book_shop
UNION
SELECT * FROM book_shop_new
ORDER BY 3 DESC;

-- # 2. Subqueries
SELECT * FROM tracks t 
WHERE t.Milliseconds = (SELECT MAX(t.Milliseconds) FROM tracks t);

SELECT firstname, lastname, country 
FROM (SELECT * FROM customers WHERE country = 'USA');

-- # 3. Window function
select 
    *,
    sum(sales) over(order by quarter) as sum_sales_cumm,
    avg(sales) over(order by quarter) as mean_sales_cumm,
    count(sales) over(order by quarter) as n_cumm        
from df;

SELECT 
  *,
  row_number() over(partition by am order by hp) as row_num
FROM df;

