from rolepermissions.roles import AbstractUserRole

class Organizer(AbstractUserRole):
    available_permissions = {
    'is_organizer': True,
    }
