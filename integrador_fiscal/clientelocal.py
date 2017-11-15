

from satcfe import ClienteSATLocal


class ClienteIntegradorLocal(ClienteSATLocal):

    def __init__(self, *args, **kwargs):
        super(ClienteIntegradorLocal, self).__init__(*args, **kwargs)
