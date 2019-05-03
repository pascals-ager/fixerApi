from service.serviceImpl import ServiceImpl
import argparse
import logging

logging.basicConfig(level=logging.INFO, filename="resources/fixerApi.log")


def main(args):
    log = logging.getLogger()
    service = ServiceImpl()
    if args.command == 'slurp':
        params = (('start_date', args.start_date), ('end_date', args.end_date), ('base', args.base_code.upper()))
        log.info("Received {} command with {}".format(args.command, params))
        response = service.get_timeseries_data(params)
        service.persist_response(response)
    elif args.command == 'query':
        base_code = args.base_code.upper()
        currency_code = args.currency_code.upper()
        start_date = args.start_date
        end_date = args.end_date
        params = (('start_date', start_date), ('end_date', end_date ), ('base', base_code),
                  ('currency_code', currency_code))
        log.info("Received {} command with {}".format(args.command, params))
        results = service.get_average_rate(base_code, currency_code, start_date, end_date)
        for res in results:
            print("Average rate of {} against {} from {} to {} is {}".format(res[1], res[2], start_date, end_date, res[2]))

    elif args.command == 'seed':
        log.info("Received {} command".format(args.command))
        service.seed_database()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Historical currency rate slurper")
    subparsers = parser.add_subparsers(help="sub command help", dest='command')
    parser_slurp = subparsers.add_parser('slurp', help="slurp historical data")
    parser_slurp.add_argument('--base_code', help="Base currency code to slurp",
                              required=True, default="EUR")
    parser_slurp.add_argument('--start_date', help="Start Date to slurp in YYYY-MM-DD",
                              required=True, default=None)
    parser_slurp.add_argument('--end_date', help="End Date to slurp in YYYY-MM-DD",
                              required=True, default=None)
    parser_query = subparsers.add_parser('query', help="query historical data")
    parser_query.add_argument('--base_code', help="Base currency code to query",
                              required=True, default="EUR")
    parser_query.add_argument('--currency_code', help="Target currency code to query",
                              required=True, default="EUR")
    parser_query.add_argument('--start_date', help="Start Date to query in YYYY-MM-DD",
                              required=True, default=None)
    parser_query.add_argument('--end_date', help="End Date to query in YYYY-MM-DD",
                              required=True, default=None)
    parser_slurp = subparsers.add_parser('seed', help="seed the database with the table")
    main(parser.parse_args())
