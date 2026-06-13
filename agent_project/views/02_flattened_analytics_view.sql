CREATE OR REPLACE VIEW `waybackhome-8nw4qqaw543g6sm9h5`.`membership_ds`.`user_profiles_new` AS
SELECT
  JSON_VALUE(PARSE_JSON(t.raw_content), '$.user_id') AS user_id,
  JSON_VALUE(PARSE_JSON(t.raw_content), '$.username') AS username,
  JSON_VALUE(PARSE_JSON(t.raw_content), '$.email') AS email,
  JSON_VALUE(log_event, '$.event_id') AS event_id,
  JSON_VALUE(log_event, '$.timestamp') AS event_timestamp,
  JSON_VALUE(log_event, '$.type') AS event_type
FROM
  `waybackhome-8nw4qqaw543g6sm9h5`.`membership_ds`.`user_profiles_new_staging` AS t,
  UNNEST(JSON_QUERY_ARRAY(PARSE_JSON(t.raw_content), '$.log_events')) AS log_event;