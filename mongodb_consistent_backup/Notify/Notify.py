import logging

from mongodb_consistent_backup.Notify.Nsca import Nsca
from mongodb_consistent_backup.Pipeline import Stage


class Notify(Stage):
    def __init__(self, manager, config, timer, base_dir, backup_dir):
        super(Notify, self).__init__(self.__class__.__name__, manager, config, timer, base_dir, backup_dir)
        self.method = self.config.notify.method

        self.notifications = []
        self.init()

    def notify(self, message, success=False):
        notification = (success, message)
        self.notifications.append(notification)

    def run(self, *args):
        if self._method and len(self.notifications) > 0:
            logging.info("Sending %i notification(s) to: %s" % (len(self.notifications), self._method.server))
            self.timers.start(self.stage)
            while len(self.notifications) > 0:
                try:
                    (success, message) = self.notifications.pop()
                    state = self._method.failed
                    if success:
                        state = self._method.success
                    self._method.notify(success, message)
                except:
                    continue
            self.timers.stop(self.stage)

    def close(self):
        if self._method:
            return self._method.close()
