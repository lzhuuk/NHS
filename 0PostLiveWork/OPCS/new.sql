SELECT y.Id, y.EffectiveTime, y.ActiveStatus, y.ConceptId, y.LanguageCode, TypeId, Term, CaseSignificanceId FROM 
(SELECT Id FROM sct_concept_output) AS x
INNER JOIN sct_description_term AS y
ON x.Id=y.ConceptId
WHERE y.ConceptId='1064961000000107'
ORDER BY ConceptId
