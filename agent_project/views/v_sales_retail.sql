CREATE OR REPLACE VIEW `waybackhome-8nw4qqaw543g6sm9h5`.`way_back_home`.`v_sales_retail` AS
SELECT
  t1.date_id,
  t4.item_num AS item_id, -- Corrected from t4.item_id as 'item_dim' has 'item_num'. Aliased to match requested column name.
  t1.member_id,
  t1.location_id,
  t1.item_num,
  t1.qty,
  t1.amount,
  t2.card_num,
  t2.first_nm,
  t2.last_nm,
  t3.`location name`, -- Backticks required for column names with spaces
  t3.region -- Corrected from 'reion' based on schema
FROM
  `waybackhome-8nw4qqaw543g6sm9h5`.`way_back_home`.`sales_fact` AS t1
INNER JOIN
  `waybackhome-8nw4qqaw543g6sm9h5`.`membership_ds`.`membership_dim` AS t2
ON
  t1.member_id = t2.member_id
INNER JOIN
  `waybackhome-8nw4qqaw543g6sm9h5`.`way_back_home`.`location_dim` AS t3 -- Added alias t3
ON
  t1.location_id = t3.location_id
INNER JOIN
  `waybackhome-8nw4qqaw543g6sm9h5`.`way_back_home`.`item_dim` AS t4 -- Corrected table name from 'item_id' to 'item_dim' and added alias t4
ON
  t1.item_num = t4.item_num -- Corrected join key from t1.item_id and t4.item_id to use 'item_num' from respective schemas
