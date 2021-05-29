SELECT id,
    auction_description
FROM auction
    JOIN (
        SELECT auction_id,
            auction_description
        FROM information
            JOIN (
                SELECT MAX(reference) as ref,
                    auction_id as aid
                FROM information
                GROUP BY aid
            ) AS ref_id ON reference = ref_id.ref
    ) AS info ON id = info.auction_id
WHERE end_date > TIMESTAMP '2021-01-01 22:11:00'
    AND auction_description LIKE '%u%';