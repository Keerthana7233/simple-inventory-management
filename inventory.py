import csv


class Product:
    def __init__(self, product_id, name, price, quantity):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__quantity = int(quantity)

        if self.__price < 0:
            raise ValueError("Price cannot be negative")

        if self.__quantity < 0:
            raise ValueError("Quantity cannot be negative")

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def quantity(self):
        return self.__quantity

    def value(self):
        return self.__price * self.__quantity


class Inventory:
    def __init__(self):
        self.__products = {}

    def add_product(self, product: Product):
        if product.product_id in self.__products:
            raise ValueError(
                f"Product ID '{product.product_id}' already exists."
            )

        self.__products[product.product_id] = product

    def remove_product(self, product_id: str):
        if product_id not in self.__products:
            raise KeyError(
                f"Product ID '{product_id}' not found."
            )

        del self.__products[product_id]

    def update_quantity(self, product_id: str, new_quantity: int):
        if product_id not in self.__products:
            raise KeyError(
                f"Product ID '{product_id}' not found."
            )

        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        # Update the private quantity attribute
        self.__products[product_id]._Product__quantity = new_quantity

    def search_by_name(self, name_substring: str) -> list[Product]:
        search_text = name_substring.lower()

        return [
            product
            for product in self.__products.values()
            if search_text in product.name.lower()
        ]

    def total_inventory_value(self) -> float:
        return sum(
            product.value()
            for product in self.__products.values()
        )


def load_inventory_from_csv(file_path: str) -> Inventory:
    inventory = Inventory()

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            product_id, name, price, quantity = row

            product = Product(
                product_id,
                name,
                float(price),
                int(quantity)
            )

            inventory.add_product(product)

    return inventory


if __name__ == "__main__":

    # Load inventory from CSV
    inventory = load_inventory_from_csv("sample_inventory.csv")

    print("Initial inventory loaded successfully.")

    # Addition
    new_product = Product(
        "P006",
        "Keyboard",
        1500.00,
        10
    )

    inventory.add_product(new_product)
    print("Added product: Keyboard")

    # Quantity update
    inventory.update_quantity("P001", 25)
    print("Updated quantity of P001 to 25")

    # Name search
    search_results = inventory.search_by_name("phone")

    print("\nSearch results for 'phone':")

    for product in search_results:
        print(
            f"{product.product_id} | "
            f"{product.name} | "
            f"₹{product.price:.2f} | "
            f"Quantity: {product.quantity}"
        )

    # Removal
    inventory.remove_product("P004")
    print("\nRemoved product: P004")

    # Total inventory value
    total = inventory.total_inventory_value()

    print(f"\nTotal Inventory Value: ₹{total:.2f}")