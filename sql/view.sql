SELECT 
    a.name,
    h.price 
    FROM history h
    JOIN assets a  ON h.asset_id = a.id
    ORDER BY h.timestamp DESC
    LIMIT 3
