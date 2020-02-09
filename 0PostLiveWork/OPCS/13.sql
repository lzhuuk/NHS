-- CREATE TABLE Loop1
-- SELECT x.SourceId, y.DestinationId DestinationId FROM
-- (SELECT SourceId, DestinationId FROM sct_relationship_output_tree) AS x
-- INNER JOIN sct_relationship_output_tree AS y
-- ON x.DestinationId=y.SourceId
-- ORDER BY x.SourceId

SELECT x.SourceId, x.DestinationId, y.sourceId, y.DestinationId DestinationId FROM
(SELECT SourceId, DestinationId FROM loop1) AS x
INNER JOIN sct_relationship_output_tree AS y
ON x.DestinationId=y.SourceId
ORDER BY x.SourceId
