class ConfigurationError(Exception):
    pass

class MissingConfigError(ConfigurationError):
    pass

class MissingCFGSectionPropertyError(MissingConfigError):
	pass

class InvalidConfigValueError(ConfigurationError):
    pass