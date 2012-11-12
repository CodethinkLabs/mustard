# Copyright (C) 2012 Codethink Limited


import cliapp


class Repository(object):

    def __init__(self, app, dirname):
        self.app = app
        self.dirname = dirname
        try:
            self.app.runcmd(['git', 'status'], cwd=self.dirname)
            self.checked_out = True
        except cliapp.AppException:
            self.checked_out = False
