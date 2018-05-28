use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated = 1;

-- 3. Посчитать общую сумму в деньгах всех продаж
 select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store.store_id from store join sale ON sale.store_id = store.store_id;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store.store_id  from store left join sale on sale.store_id = store.store_id where sale.store_id is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select product.name, avg(total/quantity) from sale, product where sale.product_id = product.product_id  group by sale.product_id;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select name from (select product.name, count(distinct store_id) as sc from sale join product on sale.product_id = product.product_id group by sale.product_id having sc = 1) as T;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select name from (select store.name, count(distinct(sale.product_id)) as pc from sale join store on sale.store_id = store.store_id group by sale.store_id having pc = 1) as T;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where total in (select max(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from (select date, sum(total) as a from sale group by date order by a desc, date limit 1) as T;
