select game_channel, count(*)
from test
where game_url is not NULL
group by 1
order by 2 desc