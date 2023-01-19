import socket
import errno
import time

def benchmark_request(callable, count_cycles=10_000):
    start_time = time.time()
    failures = 0
    transmits = 0

    for _ in range(count_cycles):
        try:
            callable()
            transmits += 1
        except:
            failures += 1
    duration = time.time() - start_time
    failures_p = failures * 100.0 / (transmits + failures)
    latency = (duration * 1_000_000 / transmits) if transmits else float('inf')
    speed = transmits / duration

    print(f'- Took {duration:.1f} seconds')
    print(f'- Performed {transmits:,} transmissions')
    print(f'- Recorded {failures_p:.3%} failures')
    print(f'- Mean latency is {latency:.1f} microseconds')
    print(f'- Mean speed is {speed:.1f} requests/s')


async def benchmark_request_async(callable, *args, count_cycles=10_000):
    start_time = time.time()
    failures = 0
    transmits = 0

    for _ in range(count_cycles):
        try:
            await callable(*args)
            transmits += 1
        except Exception as e:
            failures += 1
    duration = time.time() - start_time
    failures_p = failures * 100.0 / (transmits + failures)
    latency = (duration * 1_000_000 / transmits) if transmits else float('inf')
    speed = transmits / duration

    print(f'- Took {duration:.1f} seconds')
    print(f'- Performed {transmits:,} transmissions')
    print(f'- Recorded {failures_p:.3%} failures')
    print(f'- Mean latency is {latency:.1f} microseconds')
    print(f'- Mean speed is {speed:.1f} requests/s')

def socket_is_closed(sock: socket.socket) -> bool:
    """
    Returns True if the remote side did close the connection

    """
    try:
        buf = sock.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
        if buf == b'':
            return True
    except BlockingIOError as exc:
        if exc.errno != errno.EAGAIN:
            # Raise on unknown exception
            raise
    return False