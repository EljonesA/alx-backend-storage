-- Calculate lifespan for bands with Glam rock as main style and rank them

SELECT band_name,
CASE
	WHEN split IS NULL THEN 2022 - formed
	ELSE split - formed
END AS lifespan 
FROM metal_bands
WHERE style like '%Glam rock%'
ORDER BY lifespan DESC;
