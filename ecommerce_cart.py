from abc import ABC, abstractmethod
import copy

# Discount Strategy (Strategy Pattern)
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price, quantity):
        pass

# Percentage off discount strategy
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, price, quantity):
        return price * quantity * (1 - self.percentage / 100)

# Buy one get one free discount strategy
class BuyOneGetOneFree(DiscountStrategy):
    def apply_discount(self, price, quantity):
        return (quantity // 2) * price + (quantity % 2) * price

# Product (Prototype Pattern)
class Product(ABC):
    def __init__(self, name, price, availability):
        self.name = name
        self.price = price
        self.availability = availability

    @abstractmethod
    def clone(self):
        pass

# Concrete Product Subclasses
class Laptop(Product):
    def clone(self):
        return copy.copy(self)

class Headphones(Product):
    def clone(self):
        return copy.copy(self)

class ShoppingCart:
    def __init__(self):
        self.cart = []

    def add_to_cart(self, product, quantity, discount_strategy=None):
        if product.availability >= quantity:
            if discount_strategy:
                price_with_discount = discount_strategy.apply_discount(product.price, quantity)
            else:
                price_with_discount = product.price * quantity

            product_copy = product.clone()
            product_copy.availability = quantity

            self.cart.append({"product": product_copy, "price": price_with_discount})
            product.availability -= quantity
            return True
        else:
            print(f"{product.name} is not available in the desired quantity.")
            return False

    def remove_from_cart(self, product_name):
        for item in self.cart:
            if item["product"].name == product_name:
                self.cart.remove(item)
                item["product"].availability += 1  # Release the product back to availability
                return True
        return False

    def calculate_total(self):
        total = sum(item["price"] for item in self.cart)
        return total

    def view_cart(self):
        if not self.cart:
            print("Your cart is empty.")
        else:
            cart_summary = []
            for item in self.cart:
                product_name = item['product'].name
                quantity = item['product'].availability
                cart_summary.append(f"{quantity} {product_name}")
            cart_summary = ", ".join(cart_summary)
            print(f"You have {cart_summary} in your cart.")

def display_product_list(products):
    print("Available Products:")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.name} - Price: ${product.price} - Availability: {product.availability} units")

def main():
    # Create some sample products
    laptop = Laptop("Laptop", 1000, True)
    headphones = Headphones("Headphones", 50, True)

    products = [laptop, headphones]

    # Create a shopping cart
    cart = ShoppingCart()

    while True:
        print("\nMenu:")
        print("1. Display Products")
        print("2. Add Product to Cart")
        print("3. View Cart")
        print("4. Remove Product from Cart")
        print("5. Calculate Total Bill")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_product_list(products)
        elif choice == '2':
            display_product_list(products)
            product_index = int(input("Enter the product number to add to cart: ")) - 1
            if 0 <= product_index < len(products):
                product = products[product_index]
                quantity = int(input("Enter the quantity to add to cart: "))
                discount_choice = input("Apply discount strategy? (Y/N): ").strip().lower()
                if discount_choice == 'y':
                    print("Available discount strategies:")
                    print("1. Percentage off")
                    print("2. Buy one get one free")
                    discount_type = input("Select a discount strategy (1/2): ")
                    if discount_type == '1':
                        discount_strategy = PercentageDiscount(float(input("Enter discount percentage: ")))
                    elif discount_type == '2':
                        discount_strategy = BuyOneGetOneFree()
                    else:
                        discount_strategy = None
                else:
                    discount_strategy = None
                cart.add_to_cart(product, quantity, discount_strategy)
        elif choice == '3':
            cart.view_cart()
        elif choice == '4':
            cart.view_cart()
            product_name = input("Enter the product name to remove from cart: ")
            cart.remove_from_cart(product_name)
        elif choice == '5':
            total_bill = cart.calculate_total()
            print(f"Your total bill is ${total_bill}.")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
