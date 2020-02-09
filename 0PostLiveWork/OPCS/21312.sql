CREATE TEMPORARY TABLE tt
SELECT x.SourceId source_x, x.DestinationId dest_x, y.SourceId source_y, y.DestinationId dest_y
FROM (SELECT SourceId, DestinationId FROM sct_relationship_output_tree LIMIT 0,1) AS x
INNER JOIN  sct_relationship_output_tree AS y
ON x.DestinationId=y.SourceId;

CREATE TEMPORARY TABLE tt
SELECT x.SourceId source_x, x.DestinationId dest_x, y.SourceId source_y, y.DestinationId dest_y
FROM (SELECT SourceId, DestinationId FROM sct_relationship_output_tree LIMIT 0,1) AS x
INNER JOIN  sct_relationship_output_tree AS y
ON x.DestinationId=y.SourceId;
