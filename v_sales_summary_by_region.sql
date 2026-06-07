-- New database view object to summarize local refined sales dimensions
SELECT 
    loc.region AS sales_region,
    COUNT(fact.sales_id) AS total_transactions,
    SUM(fact.sales_amount) AS total_revenue
FROM 
    `waybackhome-8nw4qqaw543g6sm9h5.way_back_home.sales_fact` AS fact
INNER JOIN 
    `waybackhome-8nw4qqaw543g6sm9h5.way_back_home.location_dim` AS loc
    ON fact.location_id = loc.location_id
GROUP BY 
    sales_region;