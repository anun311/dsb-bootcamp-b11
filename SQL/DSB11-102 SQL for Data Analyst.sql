-- # 102 SQL for Data Analyst
-- # 1. CASE WHEN
SELECT
	company,
  CASE 
  	WHEN company IS NOT NULL THEN 'Coporate'
    ELSE 'End Customer' 
  END AS segment
FROM customers;

SELECT 
	c.FirstName,
--	c.Company,
--	COALESCE(c.Company, "No data") as comp_1,
	CASE WHEN c.Company IS NULL THEN 'B2C' ELSE c.Company END AS comp_2,
	CASE 
		WHEN c.Country in ('USA', 'Canada') THEN 'America' 
		WHEN c.Country in ('Italy', 'Belgium') THEN 'Europe' 
	ELSE 'Others' END AS regions
FROM customers c;

-- # 2. Date Time
SELECT 
	invoicedate,
  CAST(STRFTIME('%Y', invoicedate) AS INT) AS year_,
  STRFTIME('%m', invoicedate) AS month_,
  STRFTIME('%d', invoicedate) AS day_,
  STRFTIME('%Y-%m', invoicedate) AS monyear_
FROM invoices
WHERE year_ = 2010;

-- # 3. Select Data From Multiple Tables
SELECT *
FROM artists
JOIN albums ON albums.ArtistId = artists.ArtistId
WHERE artists.ArtistId = 50;

SELECT 
	a.ArtistId,
  a.Name,
  al.Title,
	t.Name,
  t.composer
FROM artists as a
INNER JOIN albums AS al ON al.ArtistId = a.ArtistId
INNER JOIN tracks AS t ON t.AlbumId = al.AlbumId
WHERE a.Name = 'Aerosmith';

SELECT 
	e1.name AS emp_name,
	e2.name AS manager
FROM employee e1, employee e2
WHERE e1.report_to = e2.id;

SELECT 
  a.ArtistId,
  a.Name AS artist_name,
  al.Title AS album_name,
  t.Name AS song_name
FROM artists a, albums al, tracks t
WHERE al.ArtistId = a.ArtistId -- PK = FK
AND al.AlbumId = t.AlbumId
AND a.ArtistId IN (8, 100);

select 
	g.Name as genre_name,
	count(*) as songs
from artists at
inner join albums al on al.ArtistId = at.ArtistId
inner join tracks t on t.AlbumId = al.AlbumId 
inner join genres g on g.GenreId = t.GenreId 
where g.Name in ('Jazz', 'Rock', 'Pop')
group by g.Name;

-- # 4. Random
SELECT
	name 
--    ,RANDOM() as ran
FROM tracks
ORDER BY RANDOM() DESC
LIMIT 5;

-- # 5. Aggregate Functions
SELECT 
  AVG(t.Milliseconds) AS avg_time,
  SUM(t.Milliseconds) AS sum_time,
  MIN(t.Milliseconds) AS min_time,
  MAX(t.Milliseconds) AS max_time,
  COUNT(t.Milliseconds) AS acnt_time
FROM tracks t;

SELECT 
  COUNT(DISTINCT c.Country) AS cnt_country, 
  COUNT(*) AS cnt_record
FROM customers c;

select 
	count(*) as cnt_cust,
	c.Country
from customers c 
group by c.Country
HAVING count(*) >= 5
order by count(*) DESC;

select 
	i.BillingCountry,
	count(i.Total) as cnt_,
	sum(i.Total) as sum_,
	round(avg(i.Total), 2) as avg_,
	min(i.Total) as min_,
	max(i.Total) as max_
from invoices i 
group by i.BillingCountry;

-- # 6. GROUP BY
SELECT 
  g.Name as genre_name,
  COUNT(t.Name) AS cnt_song 
FROM genres g, tracks t
WHERE g.GenreId = t.GenreId
GROUP BY g.Name;

-- # 7. HAVING
SELECT 
  g.Name as genre_name,
  COUNT(t.Name) AS cnt_song 
FROM genres g, tracks t
WHERE g.GenreId = t.GenreId AND g.Name <> 'Rock'
GROUP BY g.Name
HAVING COUNT(t.Name) > 100;

-- # 8. ORDER BY
SELECT 
  g.Name as genre_name,
  COUNT(t.Name) AS cnt_song 
FROM genres g, tracks t
WHERE g.GenreId = t.GenreId
GROUP BY g.Name
ORDER BY COUNT(t.Name) DESC
LIMIT 5;

-- # 9. WHERE Clause
SELECT *
FROM customers
WHERE firstname = 'John';

SELECT *
FROM customers
WHERE LOWER(country) = 'usa';

SELECT *
FROM customers
WHERE LOWER(country) = 'usa' AND state = 'CA';

SELECT *
FROM customers
WHERE LOWER(country) = 'usa' OR state = 'Canada';

SELECT *
FROM customers
WHERE NOT LOWER(country) = 'usa' OR state = 'Canada';

SELECT *
FROM customers
-- WHERE country = 'Brazil' OR country = 'Germany' OR country = 'Norway'
WHERE country IN ('Brazil', 'Germany', 'Norway');

SELECT * FROM invoices
WHERE invoicedate BETWEEN '2009-01-01 00:00:00' AND '2009-01-19 23:59:59';

SELECT * FROM customers
WHERE company IS NULL;

SELECT firstname, lastname, country, email 
FROM customers
WHERE email LIKE '%gmail.com' AND country = 'USA';

SELECT firstname, lastname, country, email, phone 
FROM customers
WHERE phone LIKE '%99%';

SELECT firstname, lastname, country, email, phone 
FROM customers
WHERE firstname LIKE 'J_hn';

-- # 10. COALESCE deal with NULL
SELECT 
	firstname, lastname, company,
  COALESCE(company, 'End Customer') AS company_cl
FROM customers;

