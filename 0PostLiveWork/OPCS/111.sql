CREATE
SELECT Id, max(EffectiveTime) AS EffectiveTime, min(ActiveStatus) AS ActiveStatus, ModuleId,DefinitionStatusID FROM sct_concept GROUP BY Id HAVING ActiveStatus='1' ORDER BY Id