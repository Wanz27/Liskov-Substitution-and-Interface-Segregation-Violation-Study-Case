from abc import ABC, abstractmethod

# ════════════════════════════════════════════════════════════════

# SOLUSI ISP-1: Pecah IVehicleOps menjadi interface kecil

# ════════════════════════════════════════════════════════════════




# ════════════════════════════════════════════════════════════════

# SOLUSI ISP-2: Pecah IDriverOps menjadi interface per kemampuan

# ════════════════════════════════════════════════════════════════
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

# SOLUSI ISP-3: Pecah IBookingOps per level akses

# ════════════════════════════════════════════════════════════════





# ════════════════════════════════════════════════════════════════

# SOLUSI LSP-1: Bicycle hanya implement interface yang relevan

# ════════════════════════════════════════════════════════════════




# ════════════════════════════════════════════════════════════════

# SOLUSI LSP-2: DroneDelivery hanya implement IChargeable + IFlyable

# ════════════════════════════════════════════════════════════════
class DroneDelivery(IFareCalculable, IChargeable, IFlyable):
    def charge_battery(self):
        return "Drone mengisi daya baterai"
        
    def fly(self):
        return "Drone terbang menuju tujuan pengiriman"
        
    def get_fare(self, km: float) -> float:
        return km * 8000
# ════════════════════════════════════════════════════════════════

# SOLUSI LSP-3: ElectricScooter get_fare() hormati kontrak parent

# ════════════════════════════════════════════════════════════════





# ════════════════════════════════════════════════════════════════

# SOLUSI ISP-2: Driver hanya implement interface sesuai jenisnya

# ════════════════════════════════════════════════════════════════




# ════════════════════════════════════════════════════════════════

# SOLUSI ISP-3: User sesuai level akses masing-masing

# ════════════════════════════════════════════════════════════════




# ════════════════════════════════════════════════════════════════

# Fungsi sekarang aman — hanya terima kontrak yang tepat

# ════════════════════════════════════════════════════════════════

def calculate_fare(v: IFareCalculable, km: float) -> float:
    return v.get_fare(km) # Aman untuk SEMUA kendaraan — hanya butuh get_fare()

def prepare_ground_vehicle(v: IGroundNavigable):
    return v.navigate_road() # Aman — hanya kendaraan darat yang masuk ke sini

def charge_up(v: IChargeable):
    return v.charge_battery() # Aman — hanya kendaraan listrik yang masuk ke sini

# ════════════════════════════════════════════════════════════════

# Penggunaan — semua aman, tidak ada yang crash

# ════════════════════════════════════════════════════════════════

bike    = Bicycle()
drone   = DroneDelivery()
scooter = ElectricScooter()
user    = RegularUser()
premium = PremiumUser()
admin   = FleetAdmin()

calculate_fare(bike, 3.0)      # ✅ 6000
calculate_fare(drone, 3.0)     # ✅ 24000
calculate_fare(scooter, 0.5)   # ✅ 2750 (bukan 0!)
prepare_ground_vehicle(bike)   # ✅ aman, bike adalah IGroundNavigable

charge_up(drone)               # ✅ aman, drone adalah IChargeable
user.book_ride("Bandara")      # ✅ aman
premium.book_flight()           # ✅ aman, hanya PremiumUser yang punya ini
admin.schedule_maintenance()    # ✅ aman, hanya FleetAdmin yang punya ini
