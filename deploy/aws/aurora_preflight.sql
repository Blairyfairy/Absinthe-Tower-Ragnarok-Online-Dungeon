-- Aurora is normally the rAthena account/character/log database layer.
-- The current rAthena YAML item DB remains file-based unless your checkout is
-- specifically configured for SQL item/mob databases. Do NOT blindly insert into
-- item_db: first compare your exact schema against the current rAthena sql-files.
SELECT DATABASE() AS current_database;
SELECT 32100 AS custom_id UNION ALL SELECT 32101 UNION ALL SELECT 32102 UNION ALL
SELECT 32103 UNION ALL SELECT 32104 UNION ALL SELECT 32105 UNION ALL SELECT 32106 UNION ALL
SELECT 32107 UNION ALL SELECT 32108;
