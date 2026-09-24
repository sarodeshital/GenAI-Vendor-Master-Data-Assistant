-- Vendor Master Data Quality Analysis
-- Compatible with SQLite-style syntax.

SELECT
    vendor_id,
    vendor_name,
    country,
    status,
    quality_score,
    missing_critical_fields
FROM vendor_master
WHERE quality_score < 80
ORDER BY quality_score ASC;

-- Missing critical fields
SELECT
    COUNT(*) AS vendors_with_missing_tax_id
FROM vendor_master
WHERE tax_id IS NULL OR TRIM(tax_id) = '';

SELECT
    COUNT(*) AS vendors_with_missing_bank_account
FROM vendor_master
WHERE bank_account IS NULL OR TRIM(bank_account) = '';

-- Active vendors requiring review
SELECT
    vendor_id,
    vendor_name,
    quality_score
FROM vendor_master
WHERE status = 'Active'
  AND quality_score < 80
ORDER BY quality_score ASC;
