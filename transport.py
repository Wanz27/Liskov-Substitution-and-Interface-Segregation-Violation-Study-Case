from abc import ABC, abstractmethod

class IVehicleOps(ABC): 
    @abstractmethod
    def refuel(self): pass            

    @abstractmethod
    def charge_battery(self): pass    

    @abstractmethod
    def navigate_road(self): pass     

    @abstractmethod
    def fly(self): pass               

    @abstractmethod
    def get_fare(self, km): pass     

class IDriverOps(ABC):  
    @abstractmethod
    def drive_car(self): pass        

    @abstractmethod
    def ride_motorcycle(self): pass   

    @abstractmethod
    def pilot_drone(self): pass       
    @abstractmethod
    def get_rating(self): pass        

class IBookingOps(ABC): 
    @abstractmethod
    def book_ride(self, dest): pass    

    @abstractmethod
    def book_delivery(self): pass     
    @abstractmethod
    def book_flight(self): pass       

    @abstractmethod
    def schedule_maintenance(self): pass 

class Bicycle(IVehicleOps):  

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

class DroneDelivery(IVehicleOps):  

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

class ElectricScooter(IVehicleOps): 

    def refuel(self):
        raise NotImplementedError("Skuter listrik tidak pakai bensin!")

    def charge_battery(self):
        return "Skuter listrik mengisi daya"

    def navigate_road(self):
        return "Skuter listrik melewati jalur khusus"

    def fly(self):
        raise NotImplementedError("Skuter listrik tidak bisa terbang!")

    def get_fare(self, km):
        if km < 1: return 0  
        return km * 3500

class CarDriver(IDriverOps):  
    def drive_car(self):
        return "Driver mengemudikan mobil"

    def ride_motorcycle(self):
        raise NotImplementedError("Driver mobil tidak mengendarai motor!")

    def pilot_drone(self):
        raise NotImplementedError("Driver mobil tidak pilot drone!")

    def get_rating(self): return 4.8

class MotorcycleDriver(IDriverOps):  
    def drive_car(self):
        raise NotImplementedError("Driver motor tidak mengemudikan mobil!")

    def ride_motorcycle(self):
        return "Driver mengendarai motor"

    def pilot_drone(self):
        raise NotImplementedError("Driver motor tidak pilot drone!")

    def get_rating(self): return 4.6

class RegularUser(IBookingOps):  
    def book_ride(self, dest):
        return f"Memesan perjalanan ke {dest}"

    def book_delivery(self):
        return "Memesan layanan pengiriman"

    def book_flight(self):
        raise NotImplementedError("User biasa tidak bisa pesan drone flight!")

    def schedule_maintenance(self):
        raise NotImplementedError("User bukan admin armada!")


def prepare_vehicle(v: IVehicleOps):  
    v.refuel()          
    v.navigate_road()   
    return v.get_fare(0.5)  

bike   = Bicycle()
drone  = DroneDelivery()
scooter= ElectricScooter()
user   = RegularUser()

prepare_vehicle(bike)     
prepare_vehicle(drone)    
prepare_vehicle(scooter)  

user.book_flight()        
user.schedule_maintenance() 
