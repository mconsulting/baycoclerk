

select  d.casenumber,d.line, d.eventdate, d.description,s.statusdate from all_summaries as S join all_dockets as d on s.casenumber=d.casenumber

WHERE d.casenumber in (select casenumber from all_dockets where description REGEXP 'CHELSEA STEWART|STEWART, CHELSEA|CHELSEA RENEE|SEATON, CHELSEA' )

order by d.casenumber, d.line desc




