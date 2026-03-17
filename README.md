# Liskov-Substitution-and-Interface-Segregation-Violation-Study-Case

# 🔍 Analisis Pelanggaran LSP & ISP
### Studi Kasus: Sistem Transportasi Online (Python)

---

## 📋 Deskripsi Program

File `transport_bad.py` adalah simulasi sistem transportasi online (ride-hailing) yang mengandung **3 pelanggaran Liskov Substitution Principle (LSP)** dan **3 pelanggaran Interface Segregation Principle (ISP)** secara bersamaan dalam satu file utuh.

Program ini memiliki class-class untuk:
- Kendaraan → `Bicycle`, `DroneDelivery`, `ElectricScooter`
- Driver → `CarDriver`, `MotorcycleDriver`
- Pengguna → `RegularUser`
- Interface → `IVehicleOps`, `IDriverOps`, `IBookingOps`

---

## ⚠️ Peta Pelanggaran

| Kode | Prinsip | Class / Interface | Baris | Inti Masalah |
|------|---------|-------------------|-------|--------------|
| L1 | LSP | `Bicycle` | 59–69 | Throw exception di `refuel()`, `charge_battery()`, `fly()` |
| L2 | LSP | `DroneDelivery` | 76–86 | Throw exception di `refuel()` dan `navigate_road()` |
| L3 | LSP | `ElectricScooter` | 94–106 | `get_fare()` return `0` untuk jarak < 1 km — melanggar kontrak |
| I1 | ISP | `IVehicleOps` | 12–22 | Interface terlalu gemuk — gabungkan operasi semua jenis kendaraan |
| I2 | ISP | `IDriverOps` | 29–37 | Paksa semua driver implement kemampuan driver jenis lain |
| I3 | ISP | `IBookingOps` | 44–52 | Campur operasi user biasa, premium, dan admin dalam satu interface |

---

## 🔴 Analisis Pelanggaran LSP

> **Prinsip:** Subclass harus bisa menggantikan parent class di mana pun tanpa merusak perilaku program.

---

### L1 — `Bicycle` tidak bisa menggantikan `IVehicleOps`

**📍 Lokasi:** `class Bicycle` — baris 59–69

**Kode bermasalah:**
```python
class Bicycle(IVehicleOps):      # Terpaksa implement semua method IVehicleOps
    def refuel(self):
        raise NotImplementedError("Sepeda tidak pakai bahan bakar!")  # ❌ crash

    def charge_battery(self):
        raise NotImplementedError("Sepeda tidak pakai baterai!")      # ❌ crash

    def navigate_road(self):
        return "Sepeda mengikuti jalur sepeda"                        # ✓ relevan

    def fly(self):
        raise NotImplementedError("Sepeda tidak bisa terbang!")       # ❌ crash

    def get_fare(self, km):
        return km * 2000
```

**❌ Letak Kesalahan:**
- `Bicycle` adalah subclass dari `IVehicleOps`, sehingga bisa dioper ke fungsi yang menerima `IVehicleOps`
- Namun saat fungsi memanggil `v.refuel()`, `v.charge_battery()`, atau `v.fly()` → langsung **crash** dengan `NotImplementedError`
- LSP dilanggar karena `Bicycle` tidak bisa sepenuhnya menggantikan `IVehicleOps` — kode klien tidak bisa mempercayai polimorfisme

**Demonstrasi crash:**
```python
def prepare_vehicle(v: IVehicleOps):
    v.refuel()         # ❌ Bicycle → NotImplementedError
    v.navigate_road()
    return v.get_fare(3)

prepare_vehicle(Bicycle())   # CRASH di baris pertama!
```

---

### L2 — `DroneDelivery` tidak bisa menggantikan `IVehicleOps`

**📍 Lokasi:** `class DroneDelivery` — baris 76–86

**Kode bermasalah:**
```python
class DroneDelivery(IVehicleOps):
    def refuel(self):
        raise NotImplementedError("Drone pakai baterai, bukan bensin!")  # ❌ crash

    def charge_battery(self):
        return "Drone mengisi daya baterai"                              # ✓ relevan

    def navigate_road(self):
        raise NotImplementedError("Drone terbang, tidak lewat jalan!")   # ❌ crash

    def fly(self):
        return "Drone terbang menuju tujuan pengiriman"                  # ✓ relevan

    def get_fare(self, km):
        return km * 8000
```

**❌ Letak Kesalahan:**
- `DroneDelivery` mewarisi `IVehicleOps` yang mengasumsikan semua kendaraan bisa diisi bahan bakar (`refuel`) dan melewati jalan (`navigate_road`) — keduanya tidak berlaku untuk drone
- `refuel()` → crash, karena drone menggunakan baterai bukan bensin
- `navigate_road()` → crash, karena drone bergerak melalui udara bukan jalan darat
- Fungsi `prepare_vehicle(DroneDelivery())` akan langsung crash di pemanggilan `v.refuel()`

---

### L3 — `ElectricScooter` melanggar kontrak `get_fare()`

**📍 Lokasi:** `class ElectricScooter` — baris 94–106

**Kode bermasalah:**
```python
class ElectricScooter(IVehicleOps):
    def refuel(self):
        raise NotImplementedError("Skuter listrik tidak pakai bensin!")  # ❌ crash

    def charge_battery(self):
        return "Skuter listrik mengisi daya"

    def navigate_road(self):
        return "Skuter listrik melewati jalur khusus"

    def fly(self):
        raise NotImplementedError("Skuter listrik tidak bisa terbang!")  # ❌ crash

    def get_fare(self, km):
        if km < 1: return 0    # ❌ SILENT BUG — melanggar kontrak!
        return km * 3500
```

**❌ Letak Kesalahan:**
- **Kontrak** yang dibuat `IVehicleOps.get_fare()` secara implisit: *"jika `km > 0`, maka hasil harus `> 0`"* — ini masuk akal karena setiap perjalanan pasti memiliki biaya
- `ElectricScooter` melanggar kontrak ini dengan mengembalikan `0` saat `km < 1`, sehingga perjalanan sejauh 0,5 km dihitung **gratis (Rp0)**
- Ini adalah **silent bug** — tidak crash, tidak ada error, tapi sistem penagihan akan menagih Rp0 untuk perjalanan yang seharusnya berbayar
- Jauh lebih berbahaya dibanding L1 dan L2 karena tidak terdeteksi saat runtime, hanya terlihat saat ada audit keuangan

**Demonstrasi silent bug:**
```python
def calculate_trip(v: IVehicleOps, km: float):
    fare = v.get_fare(km)
    print(f"Tagihan: Rp{fare:,}")   # Rp0 untuk scooter 0.5 km — padahal harusnya Rp1.750!

calculate_trip(ElectricScooter(), 0.5)   # Output: Tagihan: Rp0  ← salah!
```

---

## 🔵 Analisis Pelanggaran ISP

> **Prinsip:** Class tidak boleh dipaksa mengimplementasi method yang tidak dibutuhkan. Lebih baik banyak interface kecil daripada satu interface gemuk.

---

### I1 — `IVehicleOps` menggabungkan operasi semua jenis kendaraan

**📍 Lokasi:** `class IVehicleOps` — baris 12–22

**Kode bermasalah:**
```python
class IVehicleOps(ABC):              # ❌ Fat interface
    @abstractmethod
    def refuel(self): pass           # hanya untuk kendaraan berbahan bakar
    @abstractmethod
    def charge_battery(self): pass   # hanya untuk kendaraan listrik
    @abstractmethod
    def navigate_road(self): pass    # hanya untuk kendaraan darat
    @abstractmethod
    def fly(self): pass              # hanya untuk kendaraan udara
    @abstractmethod
    def get_fare(self, km): pass     # semua kendaraan butuh ini
```

**❌ Letak Kesalahan:**
- Tidak ada satu pun kendaraan yang membutuhkan keempat kemampuan ini sekaligus
  - Sepeda: hanya `navigate_road` + `get_fare`
  - Drone: hanya `charge_battery` + `fly` + `get_fare`
  - Skuter listrik: hanya `charge_battery` + `navigate_road` + `get_fare`
- Akibatnya, setiap kelas yang mengimplementasi interface ini terpaksa "pura-pura bisa" dengan melempar exception
- Jika method baru ditambahkan ke `IVehicleOps` (misal `activate_autopilot()`), **semua** class implementasi harus dimodifikasi meskipun tidak relevan

---

### I2 — `IDriverOps` memaksa semua driver menguasai segalanya

**📍 Lokasi:** `class IDriverOps` — baris 29–37

**Kode bermasalah:**
```python
class IDriverOps(ABC):                  # ❌ Semua kemampuan driver digabung
    @abstractmethod
    def drive_car(self): pass           # hanya untuk driver mobil
    @abstractmethod
    def ride_motorcycle(self): pass     # hanya untuk driver motor
    @abstractmethod
    def pilot_drone(self): pass         # hanya untuk operator drone
    @abstractmethod
    def get_rating(self): pass          # semua driver butuh ini
```

**❌ Letak Kesalahan:**
- `CarDriver` dipaksa implement `ride_motorcycle()` dan `pilot_drone()` → keduanya diisi exception
- `MotorcycleDriver` dipaksa implement `drive_car()` dan `pilot_drone()` → keduanya diisi exception
- Perubahan pada kemampuan driver drone (misal tambah method `check_airspace()`) akan memaksa `CarDriver` dan `MotorcycleDriver` ikut dimodifikasi meski tidak ada kaitannya

**Dampak pada implementasi:**
```python
class CarDriver(IDriverOps):
    def drive_car(self):
        return "Driver mengemudikan mobil"      # ✓ relevan

    def ride_motorcycle(self):
        raise NotImplementedError(...)          # ❌ dipaksa, tidak relevan

    def pilot_drone(self):
        raise NotImplementedError(...)          # ❌ dipaksa, tidak relevan

    def get_rating(self): return 4.8
```

---

### I3 — `IBookingOps` mencampur semua level akses pengguna

**📍 Lokasi:** `class IBookingOps` — baris 44–52

**Kode bermasalah:**
```python
class IBookingOps(ABC):
    @abstractmethod
    def book_ride(self, dest): pass         # untuk semua user
    @abstractmethod
    def book_delivery(self): pass           # untuk semua user
    @abstractmethod
    def book_flight(self): pass             # ❌ hanya untuk user premium
    @abstractmethod
    def schedule_maintenance(self): pass    # ❌ hanya untuk admin armada
```

**❌ Letak Kesalahan:**
- `RegularUser` dipaksa implement `book_flight()` (fitur berbayar/premium) dan `schedule_maintenance()` (operasional internal) → keduanya diisi exception
- Interface ini mencampur tiga level akses berbeda: **user biasa**, **user premium**, dan **admin armada** — semuanya masuk ke satu interface
- Melanggar *principle of least privilege* — user biasa seharusnya tidak pernah "tahu" bahwa `schedule_maintenance` ada
- Perubahan kebutuhan admin armada akan memaksa modifikasi `RegularUser` yang tidak ada kaitannya

**Dampak pada implementasi:**
```python
class RegularUser(IBookingOps):
    def book_ride(self, dest):
        return f"Memesan perjalanan ke {dest}"   # ✓ relevan

    def book_delivery(self):
        return "Memesan layanan pengiriman"       # ✓ relevan

    def book_flight(self):
        raise NotImplementedError(...)            # ❌ dipaksa, bukan haknya

    def schedule_maintenance(self):
        raise NotImplementedError(...)            # ❌ dipaksa, bukan haknya
```

---

## 🔗 Keterkaitan LSP dan ISP

Dalam kode ini, **ISP adalah akar masalah** yang kemudian menyebabkan pelanggaran LSP:

```
IVehicleOps terlalu gemuk (ISP)
        │
        ▼
Bicycle/DroneDelivery/ElectricScooter dipaksa implement method yang tidak relevan
        │
        ▼
Terpaksa throw NotImplementedError atau return nilai salah (LSP)
        │
        ▼
Fungsi yang menerima IVehicleOps bisa crash atau memberi hasil salah
```

> **Kesimpulan:** Memperbaiki ISP dengan memecah interface secara otomatis menyelesaikan pelanggaran LSP — karena subclass tidak lagi dipaksa implement method yang tidak relevan.
