from xmpp.transports import TLS
import socket, ssl, select, base64, sys


class CustomTLS(TLS):
    def _startSSL(self):
        """ Immidiatedly switch socket to TLS mode. Used internally."""
        """ Here we should switch pending_data to hint mode."""
        new_ssl = ssl.SSLContext()
        tcpsock = self._owner.Connection
        tcpsock._sslObj = new_ssl.wrap_socket(tcpsock._sock, None, None)
        tcpsock._sslIssuer = tcpsock._sslObj.getpeercert().get('issuer')
        tcpsock._sslServer = tcpsock._sslObj.getpeercert().get('server')
        tcpsock._recv = tcpsock._sslObj.read
        tcpsock._send = tcpsock._sslObj.write

        tcpsock._seen_data = 1
        self._tcpsock = tcpsock
        tcpsock.pending_data = self.pending_data
        tcpsock._sslObj.setblocking(False)

        self.starttls = 'success'
