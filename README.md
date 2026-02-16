# Gallery Sales Data Cleaning Project

**Cleaned_Gallery_Sales_Data** – A cleaned, analysis-ready version of messy gallery sales records.

Current date context: February 2026

## Project Overview

This project takes a dirty CSV export (`Dirty_Gallery_Sales_Data.csv`) from an art gallery's sales system and transforms it into one clean, consistent, reliable table suitable for reporting, dashboards, financial analysis, or machine learning.

**Original data issues included:**
- Duplicate sale records (marked with `_dup` suffix)
- Inconsistent artist name spelling
- Mixed age group formats (e.g. "35 - 44", "45to54", "55 plus", "UNK")
- Missing or suspicious `Total_GBP` values
- Occasional invalid unit prices (`Price_GBP` ≤ 0)
- Minor string inconsistencies (leading/trailing spaces)

**Goal achieved:**
- Single clean table: `Cleaned_Gallery_Sales_Data`
- ~420 unique transactions (from original 460 rows)
- Unique `Sale_ID` primary key
- Full `YYYY-MM-DD` dates preserved
- Repaired monetary values
- Standardized categories

## Key Cleaning Steps Performed

- **Deduplication**  
  Removed logical duplicates by preferring non-`_dup` versions (using window function + `rn = 1` filter)

- **Date Handling**  
  Ensured `SaleDate` is consistently stored as full `YYYY-MM-DD` text (explicit string validation & preservation)

- **Monetary Repairs**  
  - Recalculated `Total_GBP` when missing, empty, or suspiciously near zero  
  - Back-calculated `Price_GBP` when invalid (≤ 0 but money moved)  
  - Rounded consistently to 2 decimal places

- **Standardization & Cleaning**  
  - Trimmed all text fields  
  - Light artist name fixes (e.g. "Andrei P" → "Andrei Protsouk")  
  - Simplified age group normalization (35-44, 45-54, 55+, Unknown, etc.)  
  - Filtered out clearly invalid rows

- **Kept intentionally**  
  Negative quantities (real returns/refunds)  
  Future dates (2025–2026 entries appear valid in context)

## Files in this Repository

| File                                   | Description                                      |
|----------------------------------------|--------------------------------------------------|
| `Dirty_Gallery_Sales_Data.csv`         | Original messy input file                        |
| `Cleaned_Gallery_Sales_Data.sql`       | Full SQL script to create the clean table        |
| `README.md`                            | This file                                        |

## How to Use

1. Load the original CSV into your database as table `Dirty_Gallery_Sales_Data`  
   (SQLite, PostgreSQL, MySQL, DuckDB, etc.)

2. Run the cleaning script:
   ```bash
   sqlite3 gallery.db < Cleaned_Gallery_Sales_Data.sql
