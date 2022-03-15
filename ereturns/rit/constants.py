class RitStatus:
    INACTIVE = 0
    ACTIVE = 1

    Status = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )


class RitFrequency:
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    QUARTERLY = 4
    SEMI_ANNUAL = 5
    YEARLY = 6

    Frequency = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly'),
        (SEMI_ANNUAL, 'Semi Annual'),
        (YEARLY, 'Yearly'),
    )


class RitSupervisionStatus:
    UPLOADED = 1
    ERROR_UPLOAD_FIRST_ROW = 2

    Status = (
        (UPLOADED, 'Uploaded'),
        (ERROR_UPLOAD_FIRST_ROW, 'Failed to upload for error at first row'),
    )


class FileType:
    RIT = 1
    REFERENCE = 2
    USER_MANUAL = 3
    USER_REGISTRATION_FORM = 4

    Types = (
        (RIT, 'RIT'),
        (REFERENCE, 'Reference File'),
        (USER_MANUAL, 'User Manual'),
        (USER_REGISTRATION_FORM, 'User Registration Form'),
    )
