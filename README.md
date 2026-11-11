# A3Q1 — Student Management CLI

Interactive Python CLI for managing students in a PostgreSQL database.

## Features

- View all students
- Add a student
- Update a student's email
- Delete a student

## Setup

1. Create the database in PostgreSQL:

   ```sql
   CREATE DATABASE "A3Q1";
   ```

2. Run the schema (creates the `students` table and seed data):

   ```bash
   psql -U postgres -d A3Q1 -f schema.sql
   ```

3. Install the Python dependency:

   ```bash
   pip install psycopg2-binary
   ```

4. Update `DB_CONFIG` in `app.py` if your Postgres credentials differ.

## Run

```bash
python app.py
```

Then choose an option from the menu (1–5).

Video Link:
https://youtu.be/Z80NY3UmE3A
