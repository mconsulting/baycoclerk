SELECT replace(replace(description," ASSIGNED",""),"PROSECUTOR: ","") AS attorney_name, 
substr(eventdate,1,4) as year,
COUNT(line) as cases FROM all_dockets WHERE description LIKE "PROSECUTOR: %" 
group by attorney_name,year
order by attorney_name,year 