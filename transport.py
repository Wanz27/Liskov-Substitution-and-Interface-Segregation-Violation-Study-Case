from abc import ABC, abstractmethod

# ────────────────────────────────────────────────────────────────

# [ISP-1] Interface VehicleOps terlalu gemuk — menggabungkan

#         method untuk semua jenis kendaraan dalam 1 interface

# ────────────────────────────────────────────────────────────────

class IVehicleOps(ABC):  # [ISP-1] Fat interface — semua method digabung
    @abstractmethod
    def refuel(self): pass            # hanya untuk bensin/solar

    @abstractmethod
    def charge_battery(self): pass    # hanya untuk kendaraan listrik

    @abstractmethod
    def navigate_road(self): pass     # hanya untuk kendaraan darat

    @abstractmethod
    def fly(self): pass               # hanya untuk drone/helikopter

    @abstractmethod
    def get_fare(self, km): pass      # semua kendaraan punya ini

# ────────────────────────────────────────────────────────────────

# [ISP-2] Interface IDriverOps menggabungkan kemampuan semua

#         jenis driver — padahal tiap driver hanya bisa 1 jenis

# ────────────────────────────────────────────────────────────────

class IDriverOps(ABC):  # [ISP-2] Driver tidak perlu semua kemampuan ini
    @abstractmethod
    def drive_car(self): pass         # hanya untuk driver mobil

    @abstractmethod
    def ride_motorcycle(self): pass   # hanya untuk driver motor

    @abstractmethod
    def pilot_drone(self): pass       # hanya untuk operator drone

    @abstractmethod
    def get_rating(self): pass        # semua driver punya ini

# ────────────────────────────────────────────────────────────────

# [ISP-3] Interface IBookingOps menggabungkan semua operasi

#         booking — user biasa tidak butuh semua ini

# ────────────────────────────────────────────────────────────────

class IBookingOps(ABC):  # [ISP-3] Terlalu banyak operasi untuk satu interface
    @abstractmethod
    def book_ride(self, dest): pass    # untuk user biasa

    @abstractmethod
    def book_delivery(self): pass     # untuk user biasa

    @abstractmethod
    def book_flight(self): pass       # hanya untuk user premium

    @abstractmethod
    def schedule_maintenance(self): pass # hanya untuk admin armada

# ────────────────────────────────────────────────────────────────

# [LSP-1] Bicycle extends IVehicleOps tapi tidak bisa refuel,

#         charge_battery, maupun fly — crash saat dipanggil!

# ────────────────────────────────────────────────────────────────

class Bicycle(IVehicleOps):  # [LSP-1] Sepeda tidak bisa refuel/charge/fly

    def refuel(self):
        raise NotImplementedError("Sepeda tidak pakai bahan bakar!")

    def charge_battery(self):
        raise NotImplementedError("Sepeda tidak pakai baterai!")

    def navigate_road(self):
        return "Sepeda mengikuti jalur sepeda"

    def fly(self):
        raise NotImplementedError("Sepeda tidak bisa terbang!")

    def get_fare(self, km):
        return km * 2000
      
# ────────────────────────────────────────────────────────────────

# [LSP-2] DroneDelivery extends IVehicleOps tapi tidak bisa

#         navigate_road dan refuel — drone terbang & pakai baterai

# ────────────────────────────────────────────────────────────────

class DroneDelivery(IVehicleOps):  # [LSP-2] Drone tidak lewat jalan & tidak isi bensin

    def refuel(self):
        raise NotImplementedError("Drone pakai baterai, bukan bensin!")

    def charge_battery(self):
        return "Drone mengisi daya baterai"

    def navigate_road(self):
        raise NotImplementedError("Drone terbang, tidak lewat jalan!")

    def fly(self):
        return "Drone terbang menuju tujuan pengiriman"

    def get_fare(self, km):
        return km * 8000

# ────────────────────────────────────────────────────────────────

# [LSP-3] ElectricScooter override get_fare() mengembalikan 0

#         untuk jarak < 1km → melanggar kontrak parent yang

#         menjamin return selalu > 0 untuk km > 0

# ────────────────────────────────────────────────────────────────

class ElectricScooter(IVehicleOps):  # [LSP-3] Melanggar kontrak get_fare()

    def refuel(self):
        raise NotImplementedError("Skuter listrik tidak pakai bensin!")

    def charge_battery(self):
        return "Skuter listrik mengisi daya"

    def navigate_road(self):
        return "Skuter listrik melewati jalur khusus"

    def fly(self):
        raise NotImplementedError("Skuter listrik tidak bisa terbang!")

    def get_fare(self, km):

        # ❌ Melanggar kontrak: mengembalikan 0 saat km < 1

        if km < 1: return 0   # kontrak: get_fare(km>0) harus selalu > 0!
        return km * 3500

# ────────────────────────────────────────────────────────────────

# [ISP-2 dampak] CarDriver dipaksa implement ride_motorcycle

#               dan pilot_drone yang tidak relevan

# ────────────────────────────────────────────────────────────────

class CarDriver(IDriverOps):  # [ISP-2 dampak] Dipaksa implement semua method driver
    def drive_car(self):
        return "Driver mengemudikan mobil"

    def ride_motorcycle(self):
        raise NotImplementedError("Driver mobil tidak mengendarai motor!")

    def pilot_drone(self):
        raise NotImplementedError("Driver mobil tidak pilot drone!")

    def get_rating(self): return 4.8

class MotorcycleDriver(IDriverOps):  # [ISP-2 dampak] Sama, dipaksa implement semuanya
    def drive_car(self):
        raise NotImplementedError("Driver motor tidak mengemudikan mobil!")

    def ride_motorcycle(self):
        return "Driver mengendarai motor"

    def pilot_drone(self):
        raise NotImplementedError("Driver motor tidak pilot drone!")

    def get_rating(self): return 4.6

# ────────────────────────────────────────────────────────────────

# [ISP-3 dampak] RegularUser dipaksa implement book_flight

#               dan schedule_maintenance yang tidak relevan

# ────────────────────────────────────────────────────────────────

class RegularUser(IBookingOps):  # [ISP-3 dampak] User biasa dipaksa punya semua fitur
    def book_ride(self, dest):
        return f"Memesan perjalanan ke {dest}"

    def book_delivery(self):
        return "Memesan layanan pengiriman"

    def book_flight(self):
        raise NotImplementedError("User biasa tidak bisa pesan drone flight!")

    def schedule_maintenance(self):
        raise NotImplementedError("User bukan admin armada!")

# ────────────────────────────────────────────────────────────────

# Penggunaan yang menunjukkan masalah LSP:
# Fungsi ini harusnya aman untuk semua IVehicleOps —
# tapi akan CRASH saat menerima Bicycle, Drone, atau Scooter!

# ────────────────────────────────────────────────────────────────

def prepare_vehicle(v: IVehicleOps):  # [LSP] Crash untuk Bicycle/Drone/Scooter
    v.refuel()          # ❌ Bicycle → crash, DroneDelivery → crash
    v.navigate_road()   # ❌ DroneDelivery → crash
    return v.get_fare(0.5)  # ❌ ElectricScooter → return 0 (melanggar kontrak)

# ────────────────────────────────────────────────────────────────

# PENGGUNAAN — semua masalah terlihat saat runtime

# ────────────────────────────────────────────────────────────────

bike   = Bicycle()
drone  = DroneDelivery()
scooter= ElectricScooter()
user   = RegularUser()

prepare_vehicle(bike)     # ❌ CRASH: NotImplementedError refuel()
prepare_vehicle(drone)    # ❌ CRASH: NotImplementedError refuel()
prepare_vehicle(scooter)  # ❌ SILENT BUG: get_fare(0.5) → 0, bukan 1750

user.book_flight()        # ❌ CRASH: user biasa tidak bisa book flight
user.schedule_maintenance() # ❌ CRASH: user bukan admin
