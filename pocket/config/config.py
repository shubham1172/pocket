import yamale
from pocket.utils import console


class Config:
    """
    Configuration for a container
    """
    def __init__(self, filename: str):
        schema = yamale.make_schema('pocket/config/config_schema.yaml')
        data = yamale.make_data(filename)
        try:
            yamale.validate(schema, data, strict=True)
        except ValueError:
            console.error('Bad configuration file')
            raise

        self.args = data[0][0]

        # ensure that there is a tag
        if ":" not in self.args['image']:
            self.args['image'] = f'{self.args["image"]}:latest'
