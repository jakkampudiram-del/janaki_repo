CREATE OR REPLACE EXTERNAL TABLE `waybackhome-8nw4qqaw543g6sm9h5`.`membership_ds`.`user_profiles_new_staging` (
  raw_content STRING
) OPTIONS (
  format = 'CSV',
  field_delimiter = '\x10',
  quote = '',
  uris = ['gs://janaki_ai/exports/raw_logs/nested_user_profiles.json']
);