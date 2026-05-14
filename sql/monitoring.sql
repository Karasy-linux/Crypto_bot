WITH stats AS(
    SELECT 
        DISTINCT h_out.asset_id,
        (SELECT h.price FROM history h 
        WHERE asset_id = h_out.asset_id AND timestamp >= DATETIME('now','-1 day')
        ORDER BY timestamp DESC LIMIT 1)
        AS new_price,

        (SELECT h.price FROM history h 
        WHERE asset_id = h_out.asset_id AND timestamp >= DATETIME('now','-1 day')
        ORDER BY timestamp ASC LIMIT 1)
        AS old_price
        FROM history h_out
        ) 
SELECT
    ((stats.new_price - stats.old_price) / stats.old_price * 100.0),
    s.chat_id,
    stats.asset_id,
    stats.old_price,
    stats.new_price
    FROM subscribers s
JOIN stats ON s.asset_id = stats.asset_id
WHERE stats.old_price > 0 
AND ((stats.new_price - stats.old_price) / stats.old_price * 100.0) >= s.percent

