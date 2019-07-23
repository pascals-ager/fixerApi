Recreate miniconda environment from env.yml file
create sqlite3 database 'currencyRates.db' at $HOME/sqlite
Add the api key (use professsional account to get access to the /timeseries resource for date range queries) into ApiConfiguration(configuration.py)
Usage: python fixerApi.py -h

```buildoutcfg
{slurp,query,seed}  sub command help 
slurp               slurp historical data 
query               query historical data 
seed                seed the database with the table
```
##### Seed the database with the `HISTORICAL_CURRENCY_RATES` table
```
python fixerApi.py seed

```
##### Slurp the FixerApi /timeseries endpoint with a base code and date range
```buildoutcfg
python fixerApi.py slurp --base_code Eur --start_date 2019-02-01 --end_date 2019-03-01
```
##### Query the `HISTORICAL_CURRENCY_RATES`  table to get the average currency rates with a base code and date range for any currency
```buildoutcfg
python fixerApi.py query --base_code EUR --currency_code USD --start_date 2019-02-01 --end_date 2019-03-01
```
**Logs are available at resources/fixerApi.log

TODO
1. Test Cases missing
2. Sanitized inputs (dates can be tricky and need careful sanitization)
3. For large date ranges, there is no parallel request implementation
4. Chunk based persistence not available
5. Configs management
6. Use abc meta to create/enforce an interface for the database service
