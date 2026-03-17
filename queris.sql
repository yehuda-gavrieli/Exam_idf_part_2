select * from attacks limit 10



--@block
select entity_id ,target_name,priority_level from targets
where priority_level in (1 , 2) and  movement_distance_km > 5

--@block
select signal_type , count(*) AS COUNT from intel_signals
group by signal_type
order by count desc


--@block

select entity_id , count(*) AS unknoen_count from intel_signals
WHERE priority_level = 99
group by entity_id 
order by unknoen_count desc
limit 3

