# Movies & Ratings Analysis (SQLite + Pandas + Matplotlib)

A small, commented Python script that explores a local SQLite database (`mubi_movies_ratings.db`) containing two tables:

- **movies**: `movie_id`, `movie_title`, `director_name`, `movie_release_year`, `movie_popularity`, `rating`, ...
- **ratings**: `movie_id`, `critique`, `critique_likes`, ...

## What it does

- Connects to SQLite and runs **sanity checks** and **cardinality** counts.
- Flags **movies with missing release years** (data quality).
- Bins movies by **rating** into *High / Medium / Low*.
- Finds **high-rated recent movies** (2016+, rating 4.5–4.9) and shows a **stacked bar** of counts per rating per year.
- Extracts **"director's cut"** titles; reports top 2 directors by volume and average rating.
- Computes **yearly aggregates** (average rating and max popularity) and draws **two line charts** (1 per figure).
- Joins **movies + ratings** to list the **top critiques by likes**, and prints counts by year for those.
- Uses a **LEFT JOIN** to find how many **movies have no ratings**, and prints the percentage of catalog affected.

> All charts use default Matplotlib styling (no custom colors) and **each chart is in its own figure**.

## Requirements

- Python 3.8+
- `pandas`, `matplotlib`

Install:
```bash
pip install pandas matplotlib
```
