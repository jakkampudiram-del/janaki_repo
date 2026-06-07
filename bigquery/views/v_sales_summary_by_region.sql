CREATE OR REPLACE VIEW `waybackhome-8nw4qqaw543g6sm9h5.way_back_home.v_sales_summary_by_region` AS
SELECT 
    loc.region AS sales_region,
    COUNT(*) AS total_transactions,
    SUM(fact.amount) AS total_revenue
FROM 
    `waybackhome-8nw4qqaw543g6sm9h5.way_back_home.sales_fact` AS fact
INNER JOIN 
    `waybackhome-8nw4qqaw543g6sm9h5.way_back_home.location_dim` AS loc
    ON fact.location_id = loc.location_id
GROUP BY 
    sales_region;