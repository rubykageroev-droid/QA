-- все пользователи
SELECT * FROM users;

-- пользователи и заказы
SELECT users.name, orders.id, orders.total
FROM users
JOIN orders ON users.id = orders.user_id;

-- количество заказов
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id;

-- пользователи с более чем 2 заказами
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 2;

-- товары дороже 1000
SELECT * FROM products
WHERE price > 1000;

-- сортировка по цене
SELECT * FROM products
ORDER BY price DESC;

-- средний заказ
SELECT AVG(total) FROM orders;

-- максимальный заказ
SELECT MAX(total) FROM orders;

-- минимальный заказ
SELECT MIN(total) FROM orders;

-- пользователи без заказов
SELECT users.name, COUNT(orders.id) AS order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name
HAVING COUNT(orders.id) = 0;

-- поиск по имени
SELECT * FROM users
WHERE name LIKE '%alex%';

-- статистика по пользователям
SELECT users.name, COUNT(orders.id), SUM(orders.total)
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.name;


SQL практика

Написал 10+ запросов с использованием:
- JOIN
- GROUP BY
- HAVING
- агрегатных функций (COUNT, SUM, AVG)
- фильтрации и сортировки
