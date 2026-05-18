SELECT 
    last_price
    FROM history
    WHERE chat_id = ? 
    AND asset_id = ? 