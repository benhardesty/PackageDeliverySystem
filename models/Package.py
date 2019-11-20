"""Object to represent a package"""

class Package:

    def __init__(self, package_id, address, city, state, zip, delivery_deadline, mass, special_notes, status="Not Delivered", delivered_time=None):
        """Initialize a package object.

        Keyword arguments:
        package_id -- the id of the package.
        address -- the street address of the delivery location.
        city -- the city of the delivery location.
        state -- the state of the delivery location.
        zip -- the zip code of the delivery location.
        delivery_deadline -- the delivery deadline of the package.
        mass -- the mass of the package.
        special_notes -- any special notes associated with the package.
        state -- the status of the package in regard to delivery.
        delivered_time -- the time the package was delivered.
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.special_notes = special_notes
        self.status = status
        self.delivered_time = delivered_time
        self.address_and_zip = address + " (" + zip + ")"
