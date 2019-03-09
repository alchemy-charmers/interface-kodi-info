from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import log


class KodiInfoProvides(RelationBase):
    scope = scopes.GLOBAL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state('{relation_name}.triggered'))

    @hook('{provides:kodi-info}-relation-{joined,changed}')
    def changed(self):
        log('kodi-info.triggered', 'INFO')
        self.set_state('{relation_name}.available')
        self.set_state('{relation_name}.triggered')

    @hook('{provides:kodi-info}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.configured')
        log('Removed kodi-info.configured', 'INFO')

    def configure(self, hostname, port, user, passwd):
        relation_info = {
            'hostname': hostname,
            'port': port,
            'user': user,
            'passwd': passwd
             }
        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')
        log('kodi-info.configured', 'INFO')
