"""
pihat.py – BerryGPS-IMUv4 helper
────────────────────────────────

• Reads latitude/longitude from the on-board u-blox GPS over the Pi’s
  UART (/dev/serial0).

• Reads the 3-axis magnetometer inside the LSM9DS1 IMU over I²C
  (address 0x1C) and converts it to a tilt-uncompensated compass heading
  in degrees.

Only the pieces you asked for (lat, lon, heading) are implemented; you
can extend this class to add accelerometer, gyro, pressure, etc.

Dependencies
────────────
sudo apt install -y python3-serial python3-smbus2
pip3 install pynmea2

Wiring
──────
BerryGPS-IMUv4 defaults to:
  • UART TX/RX for GPS (Pi pins 8 TXD, 10 RXD)
  • I²C bus 1 for IMU/pressure sensor (Pi pins 3/5)  :contentReference[oaicite:0]{index=0}
"""

from __future__ import annotations
from dataclasses import dataclass
import math
import time
import serial
import smbus2
import pynmea2    # sudo pip3 install pynmea2

# --------------------------------------------------------------------------
#  I²C register map  (magnetometer section of ST LSM9DS1)
# --------------------------------------------------------------------------
_LSM9DS1_MAG_ADDR     = 0x1C            # SA1 pulled low on BerryGPS-IMU
_CTRL_REG1_M          = 0x20            # XY axes operating mode & data-rate
_CTRL_REG2_M          = 0x21            # full-scale range
_CTRL_REG3_M          = 0x22            # power / conversion mode
_OUT_X_L_M            = 0x28            # first of 6 data registers (auto-inc)

# --------------------------------------------------------------------------
#  Data container
# --------------------------------------------------------------------------
@dataclass
class Attitude:
    lat_deg: float | None       # +N   (None if no GPS fix yet)
    lon_deg: float | None       # +E   (None if no GPS fix yet)
    heading_deg: float          # 0–360°, 0 = north

# --------------------------------------------------------------------------
class BerryGPSIMU:
    """Light-weight interface to BerryGPS-IMUv4 (GPS + LSM9DS1 mag)."""

    def __init__(
        self,
        i2c_bus: int = 1,
        serial_port: str = "/dev/serial0",
        baudrate: int = 9600,
    ) -> None:
        # I²C
        self.bus = smbus2.SMBus(i2c_bus)
        self._init_magnetometer()

        # UART
        self.ser = serial.Serial(
            port=serial_port,
            baudrate=baudrate,
            timeout=1.0,
            exclusive=True,
        )

    # ------------------------------------------------------------------
    #  Public helpers
    # ------------------------------------------------------------------
    def get_latlon(self, timeout: float = 2.0) -> tuple[float | None, float | None]:
        """
        Return (lat, lon) in decimal degrees or (None, None) if no valid
        sentence arrives within *timeout* seconds.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                line: str = self.ser.readline().decode(errors="ignore").strip()
                if not line.startswith("$"):
                    continue
                # Accept RMC (recommended minimum) or GGA (fix data)
                if ("RMC" in line or "GGA" in line):
                    msg = pynmea2.parse(line)
                    lat = getattr(msg, "latitude",  None)
                    lon = getattr(msg, "longitude", None)
                    if lat and lon:
                        return lat, lon
            except (pynmea2.ParseError, UnicodeDecodeError):
                pass
        return None, None

    def get_heading(self) -> float:
        """
        Return magnetic heading [0-360°] relative to sensor axes
        (no tilt-compensation; calibrate for hard/soft-iron error yourself).
        """
        x, y, _ = self._read_magnetometer()
        heading = math.degrees(math.atan2(y, x))
        if heading < 0:
            heading += 360.0
        return heading

    def get_attitude(self) -> Attitude:
        lat, lon = self.get_latlon()
        return Attitude(lat, lon, self.get_heading())

    # ------------------------------------------------------------------
    #  Low-level magnetometer
    # ------------------------------------------------------------------
    def _init_magnetometer(self) -> None:
        # Ultra-high-performance XY, 10 Hz ODR
        self.bus.write_byte_data(_LSM9DS1_MAG_ADDR, _CTRL_REG1_M, 0b01110000)
        # ±4 gauss full-scale
        self.bus.write_byte_data(_LSM9DS1_MAG_ADDR, _CTRL_REG2_M, 0b00000000)
        # Continuous-conversion
        self.bus.write_byte_data(_LSM9DS1_MAG_ADDR, _CTRL_REG3_M, 0b00000000)

    def _read_magnetometer(self) -> tuple[int, int, int]:
        # Read 6 bytes starting at OUT_X_L_M with auto-increment
        raw = self.bus.read_i2c_block_data(_LSM9DS1_MAG_ADDR,
                                           _OUT_X_L_M | 0x80, 6)
        x = self._twos_comp(raw[1] << 8 | raw[0], 16)
        y = self._twos_comp(raw[3] << 8 | raw[2], 16)
        z = self._twos_comp(raw[5] << 8 | raw[4], 16)
        return x, y, z

    @staticmethod
    def _twos_comp(val: int, bits: int) -> int:
        if val & (1 << bits - 1):
            val -= 1 << bits
        return val

# --------------------------------------------------------------------------
#  Convenience module-level helpers (drop-in for your previous stubs)
# --------------------------------------------------------------------------
_device: BerryGPSIMU | None = None   # lazy singleton

def _dev() -> BerryGPSIMU:
    global _device
    if _device is None:
        _device = BerryGPSIMU()
    return _device

def get_latlon() -> tuple[float | None, float | None]:
    return _dev().get_latlon()

def get_heading() -> float:
    return _dev().get_heading()

def get_attitude() -> Attitude:
    return _dev().get_attitude()
