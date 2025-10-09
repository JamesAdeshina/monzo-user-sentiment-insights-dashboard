SELECT *
FROM `monzo-data-uploader.monzo_reviews.FactReviews`
LIMIT 5;




-- FACT + DimVersion Validation
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.version_id) AS linked_versions,
  COUNT(DISTINCT d.version_id) AS total_versions,
  COUNTIF(d.version_id IS NULL) AS orphan_versions
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimVersion` AS d
ON
  f.version_id = d.version_id;





-- FACT + DimPlatform Validation
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.platform_id) AS linked_platforms,
  COUNT(DISTINCT p.platform_id) AS total_platforms,
  COUNTIF(p.platform_id IS NULL) AS orphan_platforms
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimPlatform` AS p
ON
  f.platform_id = p.platform_id;




-- FACT + DimDate Validation
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.date_id) AS linked_dates,
  COUNT(DISTINCT d.date_id) AS total_dates,
  COUNTIF(d.date_id IS NULL) AS orphan_dates
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimDate` AS d
ON
  f.date_id = d.date_id;



-- FACT + DimSentiment Validation
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.sentiment_id) AS linked_sentiments,
  COUNT(DISTINCT s.sentiment_id) AS total_sentiments,
  COUNTIF(s.sentiment_id IS NULL) AS orphan_sentiments
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimSentiment` AS s
ON
  f.sentiment_id = s.sentiment_id;




-- FACT + DIMVERSION JOIN VALIDATION
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.version_id) AS linked_versions,
  COUNT(DISTINCT d.version_id) AS total_versions,
  COUNTIF(d.version_id IS NULL) AS orphan_versions
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimVersion` AS d
ON
  f.version_id = d.version_id;




-- FACT + DIMPLATFORM JOIN VALIDATION
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.platform_id) AS linked_platforms,
  COUNT(DISTINCT p.platform_id) AS total_platforms,
  COUNTIF(p.platform_id IS NULL) AS orphan_platforms
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimPlatform` AS p
ON
  f.platform_id = p.platform_id;




-- FACT + DIMDATE JOIN VALIDATION
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.date_id) AS linked_dates,
  COUNT(DISTINCT d.date_id) AS total_dates,
  COUNTIF(d.date_id IS NULL) AS orphan_dates
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimDate` AS d
ON
  f.date_id = d.date_id;




-- FACT + DIMSENTIMENT JOIN VALIDATION
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT f.sentiment_id) AS linked_sentiments,
  COUNT(DISTINCT s.sentiment_id) AS total_sentiments,
  COUNTIF(s.sentiment_id IS NULL) AS orphan_sentiments
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
LEFT JOIN
  `monzo-data-uploader.monzo_reviews.DimSentiment` AS s
ON
  f.sentiment_id = s.sentiment_id;








-- Sentiment distribution and mean score per platform
SELECT
  p.platform AS Platform,
  f.sentiment_label AS Sentiment,
  COUNT(*) AS Review_Count,
  ROUND(AVG(f.sentiment_score), 3) AS Avg_Sentiment
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
JOIN
  `monzo-data-uploader.monzo_reviews.DimPlatform` AS p
  ON f.platform_id = p.platform_id
GROUP BY
  p.platform, f.sentiment_label
ORDER BY
  p.platform, Avg_Sentiment DESC;










-- Monthly trend of review counts, average rating, and sentiment
SELECT
  FORMAT_DATE('%Y-%m', d.review_date) AS YearMonth,
  COUNT(f.rating) AS Review_Count,
  ROUND(AVG(f.rating), 2) AS Avg_Rating,
  ROUND(AVG(f.sentiment_score), 3) AS Avg_Sentiment
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
JOIN
  `monzo-data-uploader.monzo_reviews.DimDate` AS d
  ON f.date_id = d.date_id
GROUP BY
  YearMonth
ORDER BY
  YearMonth;




-- Top 20 versions by review volume
SELECT
  v.app_version AS App_Version,
  ROUND(AVG(f.rating), 2) AS Avg_Rating,
  COUNT(*) AS Total_Reviews
FROM
  `monzo-data-uploader.monzo_reviews.FactReviews` AS f
JOIN
  `monzo-data-uploader.monzo_reviews.DimVersion` AS v
  ON f.version_id = v.version_id
GROUP BY
  v.app_version
ORDER BY
  Total_Reviews DESC
LIMIT 20;
