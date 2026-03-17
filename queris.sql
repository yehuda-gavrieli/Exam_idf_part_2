
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


--@block
select distinct entity_id from intel_signals
where (timestamp >= '2026-03-15 08:00:00' and timestamp <= '2026-03-15 20:00:00')
and  distance_from_last = 0
and entity_id in (select distinct entity_id from intel_signals
where (timestamp <= '2026-03-15 08:00:00' and timestamp >= '2026-03-15 20:00:00')
and  distance_from_last >= 10)



select reported_lat , reported_lon , timestamp from intel_signals
                WHERE entity_id ='{entity_id}' 
                order by timestamp desc