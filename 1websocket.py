import struct
import hashlib
import binascii
import socket

MAGIC = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

OP_CONT  = 0x0
OP_TEXT  = 0x1
OP_BIN   = 0x2
OP_CLOSE = 0x8
OP_PING  = 0x9
OP_PONG  = 0xA


class WebSocketError(Exception):
    pass


class WebSocket:
    def __init__(self, conn):
        self.conn = conn

    def read(self):
        header = self._recv_exactly(2)
        if header is None:
            return None

        byte0, byte1 = header[0], header[1]

        opcode = byte0 & 0x0F

        if opcode == OP_CLOSE:
            return None

        if opcode == OP_PING:
            payload = self._read_payload(byte1)
            self._send_frame(OP_PONG, payload)
            return self.read()

        if opcode not in (OP_TEXT, OP_BIN, OP_CONT):
            raise WebSocketError(f"Unknown opcode: {opcode}")

        return self._read_payload(byte1)

    def _read_payload(self, byte1):
        masked  = (byte1 & 0x80) != 0
        length  = byte1 & 0x7F

        if length == 126:
            ext = self._recv_exactly(2)
            length = struct.unpack(">H", ext)[0]
        elif length == 127:
            ext = self._recv_exactly(8)
            length = struct.unpack(">Q", ext)[0]

        mask_key = self._recv_exactly(4) if masked else None

        data = self._recv_exactly(length)
        if data is None:
            return None

        if masked and mask_key:
            data = bytes(b ^ mask_key[i % 4] for i, b in enumerate(data))

        return data

    def write(self, data):
        if isinstance(data, str):
            data = data.encode()
        self._send_frame(OP_TEXT, data)

    def _send_frame(self, opcode, payload=b""):
        length = len(payload)
        header = bytearray([0x80 | opcode])
        if length < 126:
            header.append(length)
        elif length < 65536:
            header.append(126)
            header += struct.pack(">H", length)
        else:
            header.append(127)
            header += struct.pack(">Q", length)
        self.conn.sendall(bytes(header) + payload)

    def _recv_exactly(self, n):
        buf = b""
        while len(buf) < n:
            try:
                chunk = self.conn.recv(n - len(buf))
            except OSError:
                return None
            if not chunk:
                return None
            buf += chunk
        return buf

    def close(self):
        try:
            self._send_frame(OP_CLOSE)
        except Exception:
            pass
        try:
            self.conn.close()
        except Exception:
            pass


def websocket_handshake(conn):
    request = b""
    while b"\r\n\r\n" not in request:
        chunk = conn.recv(256)
        if not chunk:
            return None
        request += chunk

    key = None
    for line in request.split(b"\r\n"):
        if line.lower().startswith(b"sec-websocket-key"):
            key = line.split(b":", 1)[1].strip()
            break

    if key is None:
        return None

    accept = binascii.b2a_base64(
        hashlib.sha1(key + MAGIC).digest()
    ).strip()

    response = (
        b"HTTP/1.1 101 Switching Protocols\r\n"
        b"Upgrade: websocket\r\n"
        b"Connection: Upgrade\r\n"
        b"Sec-WebSocket-Accept: " + accept + b"\r\n\r\n"
    )
    conn.sendall(response)

    return WebSocket(conn)