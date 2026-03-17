# Liskov-Substitution-and-Interface-Segregation-Violation-Study-Case

# 📋 Ringkasan Perubahan LSP & ISP
### Studi Kasus: Sistem Transportasi Online (Python)

---

## 🗂️ File yang Terlibat

| File | Status | Keterangan |
|------|--------|------------|
| `transport.py` | ❌ Bermasalah | Mengandung 3 pelanggaran LSP + 3 pelanggaran ISP |
| `transport_rev.py` | ✅ Diperbaiki | Semua pelanggaran diselesaikan |

---

## 🔴 LSP — Perubahan pada Kelas Kendaraan

### L1 — `Bicycle`

**Sebelum (`transport.py`):**
```python
class Bicycle(IVehicleOps):
    def refuel(self):
        raise NotImplementedError("Sepeda tidak pakai bahan bakar!")  # ❌
    def charge_battery(self):
        raise NotImplementedError("Sepeda tidak pakai baterai!")      # ❌
    def navigate_road(self):
        return "Sepeda mengikuti jalur sepeda"
    def fly(self):
        raise NotImplementedError("Sepeda tidak bisa terbang!")       # ❌
    def get_fare(self, km):
        return km * 2000
```

**Sesudah (`transport_rev.py`):**
```python
class Bicycle(IFareCalculable, IGroundNavigable):  # hanya interface yang relevan
    def navigate_road(self):
        return "Sepeda mengikuti jalur sepeda"
    def get_fare(self, km) -> float:
        return km * 2000    # kontrak terpenuhi: km > 0 → hasil > 0 ✓
```

**Perubahan:**
- Tidak lagi extend `IVehicleOps` (interface gemuk)
- Hanya implement `IFareCalculable` + `IGroundNavigable` yang sesuai kemampuan sepeda
- Tidak ada lagi `NotImplementedError` — setiap method yang ada benar-benar bisa dijalankan

---

### L2 — `DroneDelivery`

**Sebelum (`transport.py`):**
```python
class DroneDelivery(IVehicleOps):
    def refuel(self):
        raise NotImplementedError("Drone pakai baterai, bukan bensin!")  # ❌
    def charge_battery(self):
        return "Drone mengisi daya baterai"
    def navigate_road(self):
        raise NotImplementedError("Drone terbang, tidak lewat jalan!")   # ❌
    def fly(self):
        return "Drone terbang menuju tujuan pengiriman"
    def get_fare(self, km):
        return km * 8000
```

**Sesudah (`transport_rev.py`):**
```python
class DroneDelivery(IFareCalculable, IChargeable, IFlyable):  # hanya yang relevan
    def charge_battery(self):
        return "Drone mengisi daya baterai"
    def fly(self):
        return "Drone terbang menuju tujuan pengiriman"
    def get_fare(self, km) -> float:
        return km * 8000    # kontrak terpenuhi ✓
```

**Perubahan:**
- Tidak lagi extend `IVehicleOps`
- Hanya implement `IFareCalculable` + `IChargeable` + `IFlyable`
- `refuel()` dan `navigate_road()` dihapus total — bukan dikosongkan, melainkan memang tidak ada

---

### L3 — `ElectricScooter`

**Sebelum (`transport.py`):**
```python
class ElectricScooter(IVehicleOps):
    def refuel(self):
        raise NotImplementedError("Skuter listrik tidak pakai bensin!")  # ❌
    def fly(self):
        raise NotImplementedError("Skuter listrik tidak bisa terbang!")  # ❌
    def get_fare(self, km):
        if km < 1: return 0    # ❌ SILENT BUG — kontrak dilanggar
        return km * 3500
```

**Sesudah (`transport_rev.py`):**
```python
class ElectricScooter(IFareCalculable, IChargeable, IGroundNavigable):
    def charge_battery(self):
        return "Skuter listrik mengisi daya"
    def navigate_road(self):
        return "Skuter listrik melewati jalur khusus"
    def get_fare(self, km) -> float:
        base = 1000                  # biaya minimum
        return base + (km * 3500)   # selalu > 0 untuk km >= 0 ✓
```

**Perubahan:**
- `refuel()` dan `fly()` dihapus total (tidak relevan)
- `get_fare()` diperbaiki: tambah `base = 1000` sehingga tidak pernah return `0`
- Kontrak `km > 0 → hasil > 0` kini terpenuhi untuk semua nilai `km`

---

## 🔵 ISP — Perubahan pada Interface

### I1 — `IVehicleOps` → Dipecah menjadi 5 Interface Kecil

**Sebelum (`transport.py`):**
```python
class IVehicleOps(ABC):          # ❌ 1 interface untuk semua kendaraan
    @abstractmethod
    def refuel(self): pass        # hanya kendaraan berbahan bakar
    @abstractmethod
    def charge_battery(self): pass # hanya kendaraan listrik
    @abstractmethod
    def navigate_road(self): pass  # hanya kendaraan darat
    @abstractmethod
    def fly(self): pass            # hanya kendaraan udara
    @abstractmethod
    def get_fare(self, km): pass   # semua kendaraan
```

**Sesudah (`transport_rev.py`):**
```python
class IFareCalculable(ABC):      # semua kendaraan punya tarif
    @abstractmethod
    def get_fare(self, km) -> float: pass

class IRefuelable(ABC):          # hanya kendaraan berbahan bakar
    @abstractmethod
    def refuel(self): pass

class IChargeable(ABC):          # hanya kendaraan listrik
    @abstractmethod
    def charge_battery(self): pass

class IGroundNavigable(ABC):     # hanya kendaraan darat
    @abstractmethod
    def navigate_road(self): pass

class IFlyable(ABC):             # hanya kendaraan udara
    @abstractmethod
    def fly(self): pass
```

**Perubahan:**
- 1 interface gemuk → 5 interface kecil dengan tanggung jawab tunggal
- Setiap kendaraan bebas memilih hanya interface yang sesuai kemampuannya
- Penambahan method baru hanya berdampak pada interface dan kelas yang relevan

---

### I2 — `IDriverOps` → Dipecah menjadi Interface per Jenis Driver

**Sebelum (`transport.py`):**
```python
class IDriverOps(ABC):              # ❌ semua kemampuan digabung
    @abstractmethod
    def drive_car(self): pass        # hanya driver mobil
    @abstractmethod
    def ride_motorcycle(self): pass  # hanya driver motor
    @abstractmethod
    def pilot_drone(self): pass      # hanya operator drone
    @abstractmethod
    def get_rating(self): pass       # semua driver
```

**Sesudah (`transport_rev.py`):**
```python
class IDriver(ABC):                  # kontrak dasar semua driver
    @abstractmethod
    def get_rating(self): pass

class ICarDriver(IDriver):           # khusus driver mobil
    @abstractmethod
    def drive_car(self): pass

class IMotorcycleDriver(IDriver):    # khusus driver motor
    @abstractmethod
    def ride_motorcycle(self): pass

class IDroneOperator(IDriver):       # khusus operator drone
    @abstractmethod
    def pilot_drone(self): pass
```

**Perubahan:**
- 1 interface gemuk → hierarki interface: `IDriver` sebagai base, lalu tiap jenis driver punya interface sendiri
- `CarDriver` hanya implement `ICarDriver` — tidak ada exception untuk `ride_motorcycle` atau `pilot_drone`
- Penambahan jenis driver baru (misal `IBoatDriver`) tidak mempengaruhi kelas driver yang sudah ada

**Dampak pada implementasi driver:**
```python
# Sebelum: 2 method selalu throw exception
class CarDriver(IDriverOps):
    def drive_car(self): return "..."
    def ride_motorcycle(self): raise NotImplementedError(...)  # ❌
    def pilot_drone(self): raise NotImplementedError(...)      # ❌
    def get_rating(self): return 4.8

# Sesudah: hanya method yang relevan
class CarDriver(ICarDriver):
    def drive_car(self): return "Driver mengemudikan mobil"    # ✓
    def get_rating(self): return 4.8                           # ✓
```

---

### I3 — `IBookingOps` → Dipecah per Level Akses

**Sebelum (`transport.py`):**
```python
class IBookingOps(ABC):              # ❌ semua level akses dicampur
    @abstractmethod
    def book_ride(self, dest): pass       # user biasa
    @abstractmethod
    def book_delivery(self): pass         # user biasa
    @abstractmethod
    def book_flight(self): pass           # user premium
    @abstractmethod
    def schedule_maintenance(self): pass  # admin armada
```

**Sesudah (`transport_rev.py`):**
```python
class IUserBooking(ABC):             # fitur untuk semua user
    @abstractmethod
    def book_ride(self, dest): pass
    @abstractmethod
    def book_delivery(self): pass

class IPremiumBooking(IUserBooking): # extends user biasa + tambah book_flight
    @abstractmethod
    def book_flight(self): pass

class IFleetAdmin(ABC):              # terpisah total, khusus admin
    @abstractmethod
    def schedule_maintenance(self): pass
```

**Perubahan:**
- 1 interface dengan 4 aksi → 3 interface yang mencerminkan level akses nyata
- `RegularUser` hanya implement `IUserBooking` — tidak lagi tahu bahwa `book_flight` atau `schedule_maintenance` ada
- `PremiumUser` extend `IUserBooking` sehingga otomatis punya semua fitur user biasa + tambahan `book_flight`
- `FleetAdmin` berdiri sendiri dengan `IFleetAdmin` — perubahan operasional armada tidak menyentuh kelas user sama sekali

**Dampak pada implementasi user:**
```python
# Sebelum: 2 method throw exception
class RegularUser(IBookingOps):
    def book_ride(self, dest): return "..."
    def book_delivery(self): return "..."
    def book_flight(self): raise NotImplementedError(...)           # ❌
    def schedule_maintenance(self): raise NotImplementedError(...)  # ❌

# Sesudah: hanya method yang haknya
class RegularUser(IUserBooking):
    def book_ride(self, dest): return f"Memesan perjalanan ke {dest}"  # ✓
    def book_delivery(self): return "Memesan layanan pengiriman"        # ✓
```

---

## ✅ Tabel Ringkasan Seluruh Perubahan

| Kode | Prinsip | Perubahan Utama | Hasil |
|------|---------|-----------------|-------|
| L1 | LSP | `Bicycle` tidak lagi extend `IVehicleOps`; hanya implement `IFareCalculable` + `IGroundNavigable` | Tidak ada `NotImplementedError` |
| L2 | LSP | `DroneDelivery` hanya implement `IFareCalculable` + `IChargeable` + `IFlyable` | Tidak ada `NotImplementedError` |
| L3 | LSP | `get_fare()` di `ElectricScooter` tambah `base = 1000` | Kontrak `km > 0 → hasil > 0` terpenuhi |
| I1 | ISP | `IVehicleOps` dipecah → `IFareCalculable`, `IRefuelable`, `IChargeable`, `IGroundNavigable`, `IFlyable` | Setiap kendaraan hanya implement yang relevan |
| I2 | ISP | `IDriverOps` dipecah → `IDriver` (base), `ICarDriver`, `IMotorcycleDriver`, `IDroneOperator` | Setiap driver hanya implement kemampuannya |
| I3 | ISP | `IBookingOps` dipecah → `IUserBooking`, `IPremiumBooking`, `IFleetAdmin` | Akses sesuai level, tidak ada method yang dipaksakan |

---

## Kesimpulan

Memperbaiki **ISP terlebih dahulu** secara otomatis menyelesaikan **LSP**:

- Saat interface dipecah kecil-kecil, subclass tidak lagi dipaksa implement method yang tidak relevan
- Karena tidak dipaksa, tidak ada alasan untuk `raise NotImplementedError`
- Karena tidak ada `NotImplementedError`, subclass bisa sepenuhnya menggantikan parent → LSP terpenuhi

> Interface yang tepat ukurannya adalah fondasi dari desain kelas yang sehat.
