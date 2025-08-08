# network.py
"""
network.py

Network module for Pong Client. Handles TCP connection and newline-delimited JSON communication with the server.
"""

import socket
import json
from typing import TextIO, Tuple
from .config import SERVER_PORT


def connect(ip: str, port: int = None) -> Tuple[socket.socket, TextIO, TextIO]:
    """
    Connect to the Pong server via TCP and return socket plus file-based reader/writer.

    :param ip: Server IP address as string.
    :param port: Server port as integer; defaults to SERVER_PORT if None.
    :return: Tuple of (socket, reader, writer).
    """
    port = port or SERVER_PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    reader = sock.makefile('r', encoding='utf-8', newline='\n')
    writer = sock.makefile('w', encoding='utf-8', newline='\n')
    return sock, reader, writer


def send_command(writer: TextIO, command: str):
    """
    Send a control command line to the server.

    :param writer: File-like writer obtained from connect().
    :param command: One of "MOVE_UP", "MOVE_DOWN", or "STOP".
    :raises ValueError: If command is invalid.
    """
    if command not in ("MOVE_UP", "MOVE_DOWN", "STOP"):
        raise ValueError(f"Invalid command: {command}")
    writer.write(command + '\n')
    writer.flush()


def receive_state(reader: TextIO) -> dict:
    """
    Read one line of JSON from the server and parse into a dictionary.

    Blocks until a full line is received, or returns empty dict if connection closes.

    :param reader: File-like reader obtained from connect().
    :return: Dictionary with game state.
    """
    line = reader.readline()
    if not line:
        return {}
    return json.loads(line.strip())
