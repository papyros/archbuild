from builder.continuous import ContinuousIntegration
from builder.utils import load_yaml


class Builder(object):
    def __init__(self, filename):
        self.config = load_yaml(filename)
        self.continuous = ContinuousIntegration(self.config.get('continuous', []))
