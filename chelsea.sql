select * from all_dockets
where description REGEXP 'JUDGE|CHELSEA STEWART|STEWART, CHELSEA|CHELSEA RENEE|CHELSEA SEATON|SEATON, CHELSEA'
AND casenumber in (SELECT casenumber from CHELSEA)
ORDER BY casenumber,eventdate