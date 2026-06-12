CREATE VIEW `waybackhome-8nw4qqaw543g6sm9h5`.`way_back_home`.`v_sales_item_vw` AS
SELECT
  t1.date_id,
  t4.item_num AS item_id, -- Corrected from t4.item_id to t4.item_num, aliased to item_id as per request
  t1.member_id,
  t1.location_id,
  t1.item_num,
  t1.qty,
  t1.amount,
  t2.card_num,
  t2.first_nm,
  t2.last_nm,
  t3.`location name`, -- Column name from schema has a space, so it needs backticks
  t3.region -- Corrected typo from 'reion' to 'region'
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
  `waybackhome-8nw4qqaw543g6sm9h5`.`way_back_home`.`item_dim` AS t4 -- Corrected table name from 'item_id' to 'item_dim', added alias t4
ON
  t1.item_num = t4.item_num -- Corrected join condition from t1.item_id to t1.item_num (based on sales_fact schema) and t4.item_id to t4.item_num (based on item_dim schema)
