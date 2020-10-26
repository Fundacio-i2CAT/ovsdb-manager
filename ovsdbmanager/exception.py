class OvsdbQueryException(Exception):
    pass


class OvsdbResourceNotFoundException(OvsdbQueryException):
    pass


class OvsdbCommitException(OvsdbQueryException):
    pass


class OvsdbReferentialIntegrityViolation(OvsdbCommitException):
    pass


class OvsdbConstraintViolation(OvsdbCommitException):
    pass


class OvsdbResourcesExhausted(OvsdbCommitException):
    pass


class OvsdbIOError(OvsdbCommitException):
    pass


class OvsdbSyntaxError(Exception):
    pass


class OvsdbUnknownDatabase(Exception):
    pass
