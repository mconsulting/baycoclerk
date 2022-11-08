SELECT S.judge, substr(eventdate,1,7) as month , count(D.casenumber) as cases FROM all_dockets AS D join all_summaries AS S ON D.casenumber=S.casenumber
where D.description REGEXP 'CHELSEA STEWART|STEWART, CHELSEA|CHELSEA RENEE|CHELSEA SEATON|SEATON, CHELSEA'
--where D.description REGEXP 'SCOTT, LEE|LEE SCOTT|LEE MCARTHUR'
--where D.description REGEXP 'LISA JACKSON|JACKSON, LISA|LISA RENEE'
--where D.description REGEXP 'ROBERT DOUGLAS|ROBERT SALE|SALE, ROBERT'
--where D.description REGEXP 'PIAZZA'
--where D.description REGEXP 'PELL'
--where D.description REGEXP 'DAFFIN'

group by S.Judge, month
order by month
--ORDER BY D.casenumber,eventdate,line DESC