import network
import sys
import uasyncio as asyncio
from micrologger import MicroLogger
from event_handler import EventHandler

logger = MicroLogger("WiFiTCPServer")

network_status_codes = {
    0 : "idle",
    1 : "connecting..",
    -3 : "wrong password",
    -2 : "no access point found",
    -1 : "connnection failed",
    3 : "IP assigned",
    }

class WiFiTCPServer(object):
    def __init__(self, ssid: str, password: str, port: int = 42440, static_ip: str = None, gateway: str = None):
        self.ssid: str = ssid
        self.password: str = password
        self.bytes_received: EventHandler = EventHandler()
        self.connection_changed: EventHandler = EventHandler()
        self.wifi_connected: bool = False
        self.clients_connected: bool = False
        self.port: int = port
        self.static_ip: str = static_ip
        self.gateway: str = gateway
        self.use_uint32_length_header: bool = False
        self.termination_byte = None
        self.retry_interval: float = 3.
        self._wlan = network.WLAN(network.STA_IF)
        self._server = None
        self._client_write_stream = None
        self._client_read_stream = None
        self._input_buffer_len: int = 2048
        self._client_read_timeout: float = 5


    def network_status(self) -> str:
        return network_status_codes.get(self._wlan.status()) or "unknown"


    def start(self):
        asyncio.create_task(self._connection_loop())


    async def _connection_loop(self):
        logger.debug(f"TCP listener task started")

        while True:
            try:
                # logger.verb(f"WLAN status: \"{self.network_status()}\", connected: {self._wlan.isconnected()}")
                if not self._wlan.isconnected():
                    await self._connect_to_access_point()
                    
                if self._server is None:
                    logger.info(f"starting listener on {self.current_ip()}:{self.port}")
                    await asyncio.create_task(self._start_client_loop())

                await asyncio.sleep(self.retry_interval)

            except Exception as ex:
                logger.exception(ex)
                await self._dispose_and_sleep()


    async def _dispose_and_sleep(self):
        try:
            if self._client_write_stream is not None:
                logger.debug("_client_write_stream.close()")
                self._client_write_stream.close()

            if self._client_read_stream is not None:
                logger.debug("_client_read_stream.close()")
                self._client_read_stream.close()

            if self._server is not None:
                logger.debug("_server.close()")
                self._server.close()
                
        except Exception as ex:
            logger.exception(ex)

        self._client_write_stream = None
        self._client_read_stream = None
        self._server = None
        self.clients_connected = False

        logger.debug("WLAN.disconnect()")
        self._wlan.disconnect()
        self._wlan.active(False) 
        self.wifi_connected = False

        self._on_connection_changed()

        logger.debug(f"wait {self.retry_interval:.0f} seconds to retry")
        await asyncio.sleep(self.retry_interval)


    def _on_connection_changed(self):
        try:
            self.connection_changed.invoke(self, {
                "wifi_connected" : self.wifi_connected,
                "clients_connected" : self.clients_connected
            })
        except Exception as ex:
            logger.exception(ex)


    async def _start_client_loop(self):
        logger.verb(f"_start_client_loop()")
        self._server = await asyncio.start_server(self._client_loop, "0.0.0.0", self.port)
    
        
    async def _client_loop(self, reader, writer):
        logger.info(f"client connected")
        self._client_write_stream = writer
        self._client_read_stream = reader

        self.clients_connected = False
        self._on_connection_changed()

        try:
            while self._client_read_stream is not None:
                if self.use_uint32_length_header:
                    header = await reader.read(self._input_buffer_len)
                    size = int.from_bytes(header, byteorder='little', signed=False)
                    payload = await reader.read(size)

                    if len(payload) != size:
                        raise Exception(f"message header was {size} but Rx {len(payload)} bytes")

                elif self.termination_byte is not None:
                    payload = b''

                    while True:
                        byte = await reader.read(1)
                        if byte == self.termination_byte:
                            break
                        else:
                            payload += byte

                else:
                    payload = await reader.read(self._input_buffer_len)

                logger.verb(f"Rx {len(payload)} bytes")
                self.bytes_received.invoke(self, payload)

        except Exception as ex:
            logger.error(f"exception: {ex}")
            sys.print_exception(ex)

        logger.debug(f"client disconnected")
        await self._dispose_and_sleep()


    async def _connect_to_access_point(self):
        logger.debug("connect_to_access_point()")
        self._wlan.active(True)
        self._wlan.config(pm = 0xa11140) # Disable power-save mode

        if self.static_ip is not None and self.gateway is not None:
            ifconfig = self.static_ip, '255.255.255.0', self.gateway, '1.1.1.1'
            logger.debug(f"set ifconfig {ifconfig}")
            self._wlan.ifconfig(ifconfig)

        logger.debug(f"WLAN.connect(): {self.ssid}")
        self._wlan.connect(self.ssid, self.password)

        wait_seconds = 10
        while wait_seconds > 0:
            logger.debug(f"{self.network_status()} for {wait_seconds}s")
            if self._wlan.status() < 0 or self._wlan.status() >= 3:
                break
            wait_seconds -= 1
            await asyncio.sleep(1)

        if self._wlan.status() != 3:
            raise RuntimeError('AP connection failed')
        else:
            logger.info(f"connected to AP with {self.current_ip()}")
            self.wifi_connected = True
            self._on_connection_changed()


    def current_ip(self) -> str:
        return self._wlan.ifconfig()[0]


    def send_message(self, payload: bytes):
        if self._client_write_stream is not None:
            try:
                if self.use_uint32_length_header:
                    header = len(payload).to_bytes(4, byteorder='little', signed=False)
                    message = header + payload

                elif self.termination_byte is not None:
                    message = payload + self.termination_byte

                else:
                    message = payload

                logger.verb(f"Tx {len(message)} bytes")
                self._client_write_stream.write(message)
                self._client_write_stream.drain()

            except Exception as ex:
                logger.error(f"send_message() exception: {ex}")
                sys.print_exception(ex)
        else:
            logger.debug('no connection, cannot send message')
