import sys
import os

packageFolder = os.path.dirname(__file__)
if packageFolder not in sys.path:
    sys.path.append(packageFolder)

import FlightSimManager.ViewportCustomizer

FlightSimManager.ViewportCustomizer.installCustomizations()

print("FlightSim python tools installed")