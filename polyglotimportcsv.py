import json
import click
import logging
import pandas as pd
from EnumDatabaseParsers import EnumDatabaseParsers
import BusinessException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OrderedParamsCommand(click.Command):
    _options = []

    def parse_args(self, ctx, args):
        # run the parser for ourselves to preserve the passed order
        parser = self.make_parser(ctx)
        opts, _, param_order = parser.parse_args(args=list(args))
        for param in param_order:
            if not isinstance(opts[param.name], list):
                self._options.append((param, opts[param.name]))
            else:
                self._options.append((param, opts[param.name].pop(0)))

        # return "normal" parse results
        result = super().parse_args(ctx, args)
        return result

    @property
    def options(self):
        return self._options


parsers = EnumDatabaseParsers.enum_database_parsers


@click.command(cls=OrderedParamsCommand)
@click.argument('csvfile', type=click.File('r'))
@click.option('--dbconfig', type=click.File('r'), required=False, default='',
              help='JSON database configuration file. If omitted, '
                   'there will be needed to pass database credentials through command line.')
@click.option('--database', '-d', type=click.Choice(parsers.keys()),
              multiple=True)
@click.option('--entity', type=str, multiple=True)
@click.option('--rel', type=str, multiple=True, required=False, default=[])
def __init__(csvfile, dbconfig, database, entity, rel):
    """CSVFILE: CSV file to be imported"""
    df = pd.read_csv(csvfile)
    print(df)
    if dbconfig:
        print("Has dbconfig file")
        config = json.load(dbconfig)
        print(config)

    current_parser = None
    current_entities = []
    current_relationships = None

    for option, value in __init__.options:
        if option.name == 'database':
            if current_parser:
                # Execute the current parser with its entities
                result = current_parser(current_entities) if current_relationships is None \
                    else current_parser(current_entities, current_relationships)
                print(result)
            # Switch to the new parser
            current_parser = parsers[value]
            current_entities = []
            current_relationships = [] if value == 'postgres' or value == 'neo4j' else None
        elif option.name == 'entity':
            current_entities.append(value)
        elif option.name == 'rel':
            try:
                current_relationships.append(value)
            except Exception as e:
                raise BusinessException(current_parser.__name__ + " does not support relationships.")
    if current_parser:
        # Execute the last parser with its entities
        result = current_parser(current_entities) if current_relationships is None \
            else current_parser(current_entities, current_relationships)
        print(result)


if __name__ == '__main__':
    __init__()
