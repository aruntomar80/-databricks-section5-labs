-- Run after all three targets have successfully executed. Adjust namespace/catalog if changed.
SELECT environment, release, COUNT(*) AS row_count,
       SUM(CASE WHEN performance_status = 'SLOW' THEN 1 ELSE 0 END) AS slow_count
FROM workspace.s5_arun_dev.gold_results GROUP BY environment, release
UNION ALL
SELECT environment, release, COUNT(*),
       SUM(CASE WHEN performance_status = 'SLOW' THEN 1 ELSE 0 END)
FROM workspace.s5_arun_test.gold_results GROUP BY environment, release
UNION ALL
SELECT environment, release, COUNT(*),
       SUM(CASE WHEN performance_status = 'SLOW' THEN 1 ELSE 0 END)
FROM workspace.s5_arun_prod.gold_results GROUP BY environment, release;
