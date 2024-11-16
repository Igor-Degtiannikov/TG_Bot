class Command:
    def __init__(self, bot):
        """
        The base class for all bot commands.
        All specific commands should inherit from this class and override the `execute` method.
        """
        self.bot = bot

    def execute(self, message):
        """A method that will be overridden in each subclass of the command."""
        pass

