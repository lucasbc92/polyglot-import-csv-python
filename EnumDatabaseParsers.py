import click
from database_parsers import postgres, mongodb, cassandra, redis, neo4j


class EnumDatabaseParsers(click.ParamType):
    name = 'enum'

    enum_database_parsers = {
        'postgres': postgres,
        'mongodb': mongodb,
        'cassandra': cassandra,
        'redis': redis,
        'neo4j': neo4j,
    }

    def convert(self, value, param, ctx):
        if value not in self.enum_database_parsers:
            self.fail(f'Invalid value "{value}". Choose from: {", ".join(self.enum_database_parsers.keys())}', param, ctx)
        return self.enum_database_parsers[value]
