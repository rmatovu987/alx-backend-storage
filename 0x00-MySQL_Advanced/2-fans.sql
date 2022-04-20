-- RANK COUNTRY ORIGINS BY NUMBER OF FANS
SELECT origin as origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
