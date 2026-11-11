from sqlalchemy import text

hybrid_query = text("""
    WITH vector_search AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> :embedding) AS rank
        FROM main_index
        WHERE (
            CAST(:company AS VARCHAR) IS NULL 
            OR CAST(:company AS VARCHAR) = '' 
            OR company = CAST(:company AS VARCHAR)
        )
        LIMIT 20
    ),
    text_search AS (
        SELECT id, ROW_NUMBER() OVER (
            ORDER BY ts_rank_cd(to_tsvector('english', raw_string), plainto_tsquery('english', :query)) DESC
        ) AS rank
        FROM main_index
        WHERE to_tsvector('english', raw_string) @@ plainto_tsquery('english', :query)
        AND (
            CAST(:company AS VARCHAR) IS NULL 
            OR CAST(:company AS VARCHAR) = '' 
            OR company = CAST(:company AS VARCHAR)
        )
        LIMIT 20
    )
    SELECT 
        m.id,
        m.company,
        m.section,
        m.index,
        m.raw_string,
        m.definitions,
        COALESCE(1.0 / (60 + v.rank), 0.0) + COALESCE(1.0 / (60 + t.rank), 0.0) AS rrf_score
    FROM vector_search v
    FULL OUTER JOIN text_search t ON v.id = t.id
    JOIN main_index m ON COALESCE(v.id, t.id) = m.id
    ORDER BY rrf_score DESC
    LIMIT :limit;
""")


definitions_query = text("""
    SELECT company, index, raw_string 
    FROM definitions_index 
    WHERE (
        CAST(:company AS VARCHAR) IS NULL 
        OR CAST(:company AS VARCHAR) = '' 
        OR company = CAST(:company AS VARCHAR)
    )
    ORDER BY (string_to_array(index, '.'))::int[] ASC;
""")