#TASK 1:

1.1 
a) Basic approach I would take is use a separate config file and use the builtin parser or use my own parser
This although quite simple and elegant, still has the problem that the config  file has to be checked in somewhere.
One way to achieve it is to have multiple levels of configs (dev, prod etc) and check in only the dev configs

b) Use pickled objects. This however can be read by anyone willing to put in the effort to unpickle it.

b) Use SECRET stored in layered configs and adn combine it with environment variables to retrieve sensitive information depending on the environment
  
1.2 a) I would log and raise when there are database/connections errors, and perhaps log a success message when the insert function returns.
Perhaps an interactive message such as print statement incase of a script or a UI based message also would be useful.
b) log and raise would be my first approach. Do not let it fail silently.
c) Simplest tool i would use is Cron. which can only do Timer Driven scheduling
If I want Event Driven scheduling, I would look at Airflow/Nifi

1.3 a) It would be better to use OOP principles and inheritance instead of copying the script.

1.4)a) To make it suitable for CI, separating configs from code would be the first thing to do. I would also create/separate different parts of the code and make it modular.
Also, I would create an entry point to the application with some way to parameterize environment related configuration so that the CI knows what configs have to be used in the
target environment. 
Additionally I would also Dockerize the application and release a base Image to a company-wide repository.
The CI can use the latest git tag in the pulled the base image with the right configs.
If Docker is not a viable solution (due to reasons), I would use packaging solutions such as minoconda/venv/conda.
b)The CI environment should have some way of checking out source code with the latest tags/master, build a test/runner environment
from the said source code or from the docker image mentioned in the specification file(.yml).
I have used Jenkins in the past and I currently use gitlab CI, which I think is the better solution.


#TASK 2:

Pre-requisites:

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

Disclaimer: The task is not complete because of a lack of time.

What is missing:
1. Test Cases missing
2. Sanitized inputs (dates can be tricky and need careful sanitization)
3. For large date ranges, there is no parallel request implementation
4. Chunk based persistence not available
5. Configs management
6. Use abc meta to create/enforce an interface for the database service

Given more time I would address the above in the mentioned order.
