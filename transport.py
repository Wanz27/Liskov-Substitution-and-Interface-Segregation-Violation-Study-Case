from abc import ABC, abstractmethod

# ════════════════════════════════════════════════════════════════
# SOLUSI ISP-1
# ════════════════════════════════════════════════════════════════
class IFareCalculable(ABC):
    @abstractmethod
    def get_fare(self, km) -> float: pass

class IRefuelable(ABC):
    @abstractmethod
    def refuel(self): pass

class IChargeable(ABC):
    @abstractmethod
    def charge_battery(self): pass

class IGroundNavigable(ABC):
    @abstractmethod
    def navigate_road(self): pass

class IFlyable(ABC):     
    @abstractmethod
    def fly(self): pass

# ════════════════════════════════════════════════════════════════
# SOLUSI ISP-2
# ═══════════════════════════════════════════════=════════════════
class IDriverRating(ABC):
    @abstractmethod
    def get_rating(self) -> float: pass

class ICarDrivable(ABC):
    @abstractmethod
    def drive_car(self): pass

class IMotorcycleRidable(ABC):
    @abstractmethod
    def ride_motorcycle(self): pass

class IDronePilotable(ABC):
    @abstractmethod
    def pilot_drone(self): pass

# ════════════════════════════════════════════════════════════════
# SOLUSI ISP-3
# ════════════════════════════════════════════════════════════════
class IRideBooking(ABC):
    @abstractmethod
    def book_ride(self, dest): pass

class IDeliveryBooking(ABC):
    @abstractmethod
    def book_delivery(self): pass

class IFlightBooking(ABC):
    @abstractmethod
    def book_flight(self): pass

class IMaintenance(ABC):
    @abstractmethod
    def schedule_maintenance(self): pass

# ════════════════════════════════════════════════════════════════
# SOLUSI LSP-1
# ════════════════════════════════════════════════════════════════
class Bicycle(IFareCalculable, IGroundNavigable):
    def navigate_road(self):
        return "Sepeda mengikuti jalur sepeda"

    def get_fare(self, km) -> float:
        return km * 2000

# ════════════════════════════════════════════════════════════════
# SOLUSI LSP-2
# ════════════════════════════════════════════════════════════════
class DroneDelivery(IFareCalculable, IChargeable, IFlyable):
    def charge_battery(self):
        return "Drone mengisi daya baterai"
        
    def fly(self):
        return "Drone terbang menuju tujuan pengiriman"
        
    def get_fare(self, km: float) -> float:
        return km * 8000
        
# ════════════════════════════════════════════════════════════════
# SOLUSI LSP-3
# ════════════════════════════════════════════════════════════════
class ElectricScooter(IFareCalculable, IChargeable, IGroundNavigable):
    def charge_battery(self):
        return "Skuter listrik mengisi daya"

    def navigate_road(self):
        return "Skuter listrik melewati jalur khusus"

    def get_fare(self, km: float) -> float:
        return max(km * 3500, 1000)
        
# ════════════════════════════════════════════════════════════════
# SOLUSI ISP-2
# ════════════════════════════════════════════════════════════════
class CarDriver(ICarDriver):
    def drive_car(self):
        return "Driver mengemudikan mobil"

    def get_rating(self): return 4.8

# ════════════════════════════════════════════════════════════════
# SOLUSI ISP-3
# ════════════════════════════════════════════════════════════════
class RegularUser(IRideBooking, IDeliveryBooking):
    def book_ride(self, dest):
        return f"Memesan perjalanan ke {dest}"

    def book_delivery(self):
        return "Memesan layanan pengiriman"


class PremiumUser(IRideBooking, IDeliveryBooking, IFlightBooking):
    def book_ride(self, dest):
        return f"Memesan perjalanan ke {dest}"

    def book_delivery(self):
        return "Memesan layanan pengiriman"

    def book_flight(self):
        return "Memesan layanan drone flight"


class FleetAdmin(IMaintenance):
    def schedule_maintenance(self):
        return "Menjadwalkan perawatan armada"

def calculate_fare(v: IFareCalculable, km: float) -> float:
    return v.get_fare(km)

def prepare_ground_vehicle(v: IGroundNavigable):
    return v.navigate_road()

def charge_up(v: IChargeable):
    return v.charge_battery()

bike    = Bicycle()
drone   = DroneDelivery()
scooter = ElectricScooter()
user    = RegularUser()
premium = PremiumUser()
admin   = FleetAdmin()

calculate_fare(bike, 3.0)   
calculate_fare(drone, 3.0)     
calculate_fare(scooter, 0.5)   
prepare_ground_vehicle(bike)  

charge_up(drone)             
user.book_ride("Bandara")     
premium.book_flight()          
admin.schedule_maintenance()    
