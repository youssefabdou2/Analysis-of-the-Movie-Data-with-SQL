# -------------------------------------------------------------
# Import required libraries
# -------------------------------------------------------------
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# Connect to SQLite database
# -------------------------------------------------------------
connection = sqlite3.connect("mubi_movies_ratings.db")

# -------------------------------------------------------------
# Sanity check: fetch one record from movies table
# -------------------------------------------------------------
query = """
SELECT movie_id, movie_title 
FROM movies 
LIMIT 1
"""
pd.read_sql_query(query, connection)

# -------------------------------------------------------------
# Count unique movies and total rows in the movies table
# -------------------------------------------------------------
query_unique_movies = """
SELECT COUNT(DISTINCT movie_id) AS num_unique_movies
FROM movies;
"""
query_num_rows = """
SELECT COUNT(movie_id) AS num_rows
FROM movies;
"""
df_unique_movies = pd.read_sql_query(query_unique_movies, connection)
df_num_rows = pd.read_sql_query(query_num_rows, connection)
print(df_unique_movies)
print(df_num_rows)

# -------------------------------------------------------------
# Get movies with missing release years
# -------------------------------------------------------------
query_missing_year = """
SELECT movie_id, movie_title, director_name, movie_popularity
FROM movies
WHERE movie_release_year IS NULL;
"""
df_missing_years = pd.read_sql_query(query_missing_year, connection)
df_missing_years

# -------------------------------------------------------------
# Categorize movies by rating: High, Medium, Low
# -------------------------------------------------------------
query_rating_binning = """
SELECT
    CASE
        WHEN rating > 3.5 THEN 'High'
        WHEN rating BETWEEN 2.5 AND 3.5 THEN 'Medium'
        ELSE 'Low'
    END AS rating_category,
    COUNT(*) AS movie_count
FROM movies
GROUP BY rating_category;
"""
df_rating_binning = pd.read_sql_query(query_rating_binning, connection)
df_rating_binning

# -------------------------------------------------------------
# Movies released after 2015 with rating 4.5 to 4.9
# -------------------------------------------------------------
query_high_rated_recent = """
SELECT movie_title, rating, movie_release_year
FROM movies
WHERE movie_release_year > 2015
  AND rating BETWEEN 4.5 AND 4.9
ORDER BY rating DESC, movie_release_year DESC;
"""
df_high_rated_recent = pd.read_sql_query(query_high_rated_recent, connection)
df_high_rated_recent

# -------------------------------------------------------------
# Create pivot table for stacked bar chart
# -------------------------------------------------------------
pivot_data = df_high_rated_recent.pivot_table(
    index="movie_release_year", 
    columns="rating", 
    values="movie_title", 
    aggfunc="count", 
    fill_value=0
)

# Plot stacked bar chart
pivot_data.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="viridis")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies")
plt.title("Number of Movies with Each Rating per Year")
plt.legend(title="Rating", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# Find "Director's Cut" movies and rank directors
# -------------------------------------------------------------
query_director_cut = """
SELECT movie_title, director_name, rating
FROM movies
WHERE LOWER(movie_title) LIKE '%director''s cut%'
  AND rating IS NOT NULL
ORDER BY rating DESC;
"""
df_director_cut = pd.read_sql_query(query_director_cut, connection)

director_stats = df_director_cut.groupby("director_name").agg(
    movie_count=("movie_title", "count"),
    avg_rating=("rating", "mean")
).reset_index()
director_stats = director_stats.sort_values(by="movie_count", ascending=False)
top_two_directors = director_stats.head(2)
print(top_two_directors)

# -------------------------------------------------------------
# Average rating and max popularity by year (last 10 years)
# -------------------------------------------------------------
query_avg_rating_year = """
SELECT 
    movie_release_year AS year,
    AVG(rating) AS avg_rating,
    MAX(movie_popularity) AS max_popularity
FROM movies
GROUP BY movie_release_year
ORDER BY year DESC
LIMIT 10;
"""
df_avg_rating_year = pd.read_sql_query(query_avg_rating_year, connection)

# Plot average rating per year
plt.figure(figsize=(8, 4))
ax_rating = plt.subplot(2, 1, 1)
ax_rating.plot(df_avg_rating_year["year"], df_avg_rating_year["avg_rating"], marker="o", color="steelblue")
ax_rating.set_title("Average Movie Rating per Year")
ax_rating.set_ylabel("Avg Rating")
ax_rating.grid(True)

# Plot max popularity per year
ax_popularity = plt.subplot(2, 1, 2)
ax_popularity.plot(df_avg_rating_year["year"], df_avg_rating_year["max_popularity"], marker="o", color="darkorange")
ax_popularity.set_title("Max Movie Popularity per Year")
ax_popularity.set_xlabel("Year")
ax_popularity.set_ylabel("Max Popularity")
ax_popularity.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# Get top critiques by likes
# -------------------------------------------------------------
query_top_critiques = """
SELECT 
    movies.movie_title, 
    movies.movie_release_year, 
    ratings.critique, 
    ratings.critique_likes
FROM movies
INNER JOIN ratings
    ON movies.movie_id = ratings.movie_id
ORDER BY ratings.critique_likes DESC
LIMIT 10;
"""
df_top_critiques = pd.read_sql_query(query_top_critiques, connection)
df_top_critiques
df_top_critiques.groupby("movie_release_year")["movie_title"].count()

# -------------------------------------------------------------
# Count movies with no ratings and calculate percentage
# -------------------------------------------------------------
query_no_ratings = """
SELECT COUNT(*) AS num_no_reviews
FROM movies
LEFT JOIN ratings
    ON movies.movie_id = ratings.movie_id
WHERE ratings.movie_id IS NULL;
"""
df_no_ratings = pd.read_sql_query(query_no_ratings, connection)
print("Movies with no reviews comprise", 
      (df_no_ratings["num_no_reviews"] / df_unique_movies["num_unique_movies"] * 100).values[0],
      "% of the movies in the database.")

# -------------------------------------------------------------
# Close database connection
# -------------------------------------------------------------
connection.close()
