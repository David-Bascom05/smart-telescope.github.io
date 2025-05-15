# motors.py
import asyncio
import math
from typing import Dict, Tuple

from skyfield.api import load, N, W, wgs84
from skyfield.framelib import ecliptic_frame
import moteus

from pihat import get_latlon

# -------------- Constants ----------------------------------------------------
VEL_LIMIT    = 0.5      # rev / s
ACCEL_LIMIT  = 0.5      # rev / s²
ALT_REDUCTION = 4       # gearbox ratios
AZ_REDUCTION  = 4

TS       = load.timescale()
JPL_DATA = load('de421.bsp')

# Build a clean list of targets ---------------------------------------------
raw = JPL_DATA.names()
targets = {name for names in raw.values() for name in names}
targets = [n for n in targets
           if '_' not in n
           and n not in ('EARTH','EMB','SSB','SOLAR SYSTEM BARYCENTER')
           and ('BARYCENTER' not in n or n == 'PLUTO BARYCENTER')]
# Remove duplicates where shorter is subset of longer
unique = targets.copy()
for a in targets:
    for b in targets:
        if a != b and set(a.split()) <= set(b.split()) and len(a) < len(b):
            unique.remove(a)
TARGETS = sorted(unique)

# ---------------------- helper functions -----------------------------------
def _calc_alt_az(target: str, lat: float, lon: float) -> Tuple[float, float, float]:
    """Return (altitude° [deg], azimuth° [deg], distance [AU])."""
    # read GPS coords
    #lat, lon = get_latlon()
    if lat is None or lon is None:
        raise RuntimeError("No GPS fix: cannot compute pointing")

    earth = JPL_DATA['earth'] + wgs84.latlon(lat * N, lon * W)
    ast = earth.at(TS.now()).observe(JPL_DATA[target])
    alt, az, dist = ast.apparent().altaz()
    return alt.degrees, az.degrees, dist.au


def _angles_to_servo(alt_deg: float, az_deg: float, curr_az_rev: float
                    ) -> Tuple[float, float]:
    """Convert alt/az angles (deg) to servo revolutions (rev)."""
    alt_rev = (alt_deg / 360.0) * ALT_REDUCTION
    az_rev  = (az_deg  / 360.0) * AZ_REDUCTION
    delta   = az_rev - curr_az_rev
    if delta >  0.5 * AZ_REDUCTION: az_rev -= AZ_REDUCTION
    if delta < -0.5 * AZ_REDUCTION: az_rev += AZ_REDUCTION
    return alt_rev, az_rev

# ---------------------- TelescopeMount class -------------------------------
class TelescopeMount:
    """Controls two moteus servos to point at the selected celestial target."""
    def __init__(self, default: str = 'MOON') -> None:
        # initial target
        self._target = default
        # setup CAN transport and controllers

        self.lat = 42.4441448
        self.lon = -76.4831129
        
        # transport & servo will be created in run_loop() under event loop
        self._transport: moteus.Fdcanusb | None = None
        self._servo: Dict[int, moteus.Controller] | None = None
        # track current positions in revolutions
        self._current_pos = {1: 0.0, 2: 0.0}

    @property
    def target(self) -> str:
        return self._target

    @target.setter
    def target(self, name: str) -> None:
        if name not in TARGETS:
            raise ValueError(f"Unknown target: {name}")
        self._target = name

    async def run_loop(self) -> None:
        """Async task: initialize servos then run 50 Hz pointing loop."""
        # Create transport and controllers within running event loop
        self._transport = moteus.Fdcanusb()
        self._servo = {
            sid: moteus.Controller(id=sid, transport=self._transport)
            for sid in (1, 2)
        }
        # Stop and rezero once at startup
        await self._transport.cycle([s.make_stop() for s in self._servo.values()])
        await self._transport.cycle([s.make_rezero() for s in self._servo.values()])

        while True:
            try:
                alt, az, _ = _calc_alt_az(self._target, self.lat, self.lon)
            except RuntimeError:
                # no GPS fix; retry later
                await asyncio.sleep(1.0)
                continue

            #if alt <= 0:
                # target below horizon
            #    await asyncio.sleep(1.0)
            #    continue

            alt_rev, az_rev = _angles_to_servo(alt, az, self._current_pos[2])
            print(alt_rev, az_rev)
            cmds = [
                self._servo[1].make_position(
                    position=alt_rev,
                    velocity_limit=VEL_LIMIT,
                    accel_limit=ACCEL_LIMIT,
                    query=True
                ),
                self._servo[2].make_position(
                    position=az_rev,
                    velocity_limit=VEL_LIMIT,
                    accel_limit=ACCEL_LIMIT,
                    query=True
                ),
            ]
            res = await self._transport.cycle(cmds)
            self._current_pos[1] = res[0].values[moteus.Register.POSITION]
            self._current_pos[2] = res[1].values[moteus.Register.POSITION]

            await asyncio.sleep(0.02)
            #await self._transport.cycle([s.make_stop() for s in self._servo.values()])

    def snapshot(self) -> Dict[str, str]:
        """Return data dictionary for GUI display."""
        try:
            alt, az, dist = _calc_alt_az(self._target, self.lat, self.lon)
            vis = 'Above' if alt > 0 else 'Below'
        except RuntimeError:
            alt, az, dist, vis = 0.0, 0.0, 0.0, 'No GPS Fix'

        miles = f"{dist * 92_955_807.3:,.0f} miles"
        return {
            'target': self._target.replace(' BARYCENTER','').title(),
            'altaz': f"Alt {alt:.2f}°, Az {az:.2f}°",
            'vis': f"{vis} the horizon",
            'dist': miles,
            'phase': ''
        }
