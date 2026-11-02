class CandidateNotFoundError(Exception):
    pass

class JobNotFoundError(Exception):
    pass

class ApplicationNotFoundError(Exception):
    pass

class DuplicateApplicationError(Exception):
    pass

class CandidateNotEligibleError(Exception):
    pass

class ValidationError(Exception):
    pass

class InvalidStatusTransitionError(Exception):
    pass
