from online_restaurant_db import Users, engine, Menu
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

with Session(engine) as session:
    try:
        session.execute(text("ALTER TABLE menu ADD COLUMN IF NOT EXISTS category VARCHAR(50);"))
        session.commit()
        print("Columna 'category' verificada y creada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al intentar crear la columna: {e}")

# 2. Continúa con tu lógica de inserción o actualización
with Session(engine) as session:
    dishes = [
        Menu(
            id=6,
            name="Retro Burger",
            weight="450",
            ingredients="Beef Patty, Cheddar Cheese, Lettuce & Tomato, Secret Sauce, Brioche Bun",
            description="Classic double patty with melted cheese, lettuce, and secret diner sauce.",
            price=12.99,
            active=True,
            file_name="burger.jpg",
            category="burgers"
        ),
        Menu(
            id=7,
            name="Arcade Nachos",
            weight="300",
            ingredients="Corn Tortilla Chips, Nacho Cheese Sauce, Pickled Jalapeños, Fresh Salsa, Sour Cream",
            description="Loaded corn chips with jalapeños, melted cheese, and salsa.",
            price=10.99,
            active=True,
            file_name="nachos.jpg",
            category="combos"
        ),
        Menu(
            id=8,
            name="Chicken Wrap",
            weight="300",
            ingredients="Grilled Chicken, Flour Tortilla, Mixed Greens, Tomatoes, Garlic Sauce",
            description="Tender grilled chicken with fresh veggies and garlic yogurt sauce.",
            price=11.50,
            active=True,
            file_name="wrap.jpg",
            category="burgers"
        ),
        Menu(
            id=9,
            name="Crispy Fries",
            weight="200",
            ingredients="Crinkle-cut Potatoes, Vegetable Oil, Retro Salt Blend, Paprika, Garlic Powder",
            description="Crispy crinkle-cut fries seasoned with our special retro spice blend.",
            price=4.99,
            active=True,
            file_name="fries.jpg",
            category="combos"
        ),
        Menu(
            id=10,
            name="Vintage Milkshake",
            weight="400",
            ingredients="Whole Milk, Vanilla Ice Cream, Fresh Strawberries, Whipped Cream, Maraschino Cherry",
            description="Thick vanilla strawberry shake topped with whipped cream and a cherry.",
            price=6.50,
            active=True,
            file_name="milkshake.jpg",
            category="drinks"
        ),
        Menu(
            id=11,
            name="Classic Pizza",
            weight="250",
            ingredients="Pizza Dough, Tomato Sauce, Mozzarella Cheese, Premium Pepperoni, Italian Herbs",
            description="Cheesy pepperoni slice baked in our classic brick oven.",
            price=14.99,
            active=True,
            file_name="pizza.jpg",
            category="combos"
        ),
        Menu(
            id=12,
            name="Classic Lemonade",
            weight="400",
            ingredients="Water, Freshly Squeezed Lemon, Sugar, Ice",
            description="Natural freshly squeezed lemonade, served with ice and a fresh lemon slice.",
            price=3.50,
            active=True,
            file_name="limonada.jpg",
            category="drinks"
        ),
        Menu(
            id=13,
            name="Natural Orange Juice",
            weight="350",
            ingredients="Fresh Oranges",
            description="100% natural orange juice, freshly squeezed, with no added sugars.",
            price=3.80,
            active=True,
            file_name="naranja.jpg",
            category="drinks"
        ),
        Menu(
            id=14,
            name="Iced Tea",
            weight="450",
            ingredients="Black Tea, Lemon or Peach, Mint",
            description="Black iced tea with a touch of lemon or peach and fresh mint leaves.",
            price=3.20,
            active=True,
            file_name="iced_tea.jpg",
            category="drinks"
        ),
        Menu(
            id=15,
            name="Strawberry Milkshake",
            weight="400",
            ingredients="Whole Milk, Fresh Strawberries",
            description="Delicious creamy milkshake made with fresh strawberries and whole milk.",
            price=4.50,
            active=True,
            file_name="batido.jpg",
            category="drinks"
        ),
        Menu(
            id=16,
            name="Americano Coffee",
            weight="250",
            ingredients="Ground Coffee, Water",
            description="Freshly roasted and ground coffee, served hot or on the rocks.",
            price=2.80,
            active=True,
            file_name="cafe.jpg",
            category="drinks"
        ),
        Menu(
            id=17,
            name="Sparkling Mineral Water",
            weight="400",
            ingredients="Sparkling Water, Lemon Slice",
            description="Sparkling mineral water served with a touch of lemon.",
            price=2.50,
            active=True,
            file_name="agua_gas.jpg",
            category="drinks"
        ),
        Menu(
            id=18,
            name="Chicken Noodle Soup",
            weight="350",
            ingredients="Chicken Broth, Noodles, Carrot, Celery",
            description="Comforting chicken broth with noodles, carrots, and celery.",
            price=5.90,
            active=True,
            file_name="sopa_pollo.jpg",
            category="soups"
        ),
        Menu(
            id=19,
            name="Vegetable Cream Soup",
            weight="350",
            ingredients="Zucchini, Carrot, Potato, Heavy Cream",
            description="Smooth cream soup made with zucchini, carrots, and potatoes, with a touch of heavy cream.",
            price=6.20,
            active=True,
            file_name="crema_verduras.jpg",
            category="soups"
        ),
        Menu(
            id=20,
            name="Minestrone Soup",
            weight="400",
            ingredients="Pasta, Tomatoes, Beans, Fresh Vegetables",
            description="Traditional soup with pasta, tomatoes, beans, and a mix of fresh vegetables.",
            price=6.50,
            active=True,
            file_name="minestrone.jpg",
            category="soups"
        ),
        Menu(
            id=21,
            name="Beef Consommé",
            weight="300",
            ingredients="Beef Broth, Diced Vegetables",
            description="Traditional beef broth accompanied by small diced vegetables.",
            price=5.50,
            active=True,
            file_name="consome.jpg",
            category="soups"
        ),
        Menu(
            id=22,
            name="Tomato and Basil Soup",
            weight="350",
            ingredients="Ripe Tomatoes, Fresh Basil, Croutons",
            description="Soup made with ripe tomatoes and fresh basil, served with croutons.",
            price=5.80,
            active=True,
            file_name="sopa_tomate.jpg",
            category="soups"
        ),
        Menu(
            id=23,
            name="Homemade Lentil Soup",
            weight="400",
            ingredients="Lentils, Carrot, Potato, Spices",
            description="Slow-cooked lentil soup with carrots, potatoes, and a touch of spices.",
            price=6.00,
            active=True,
            file_name="lentejas.jpg",
            category="soups"
        ),
        Menu(
            id=24,
            name="Classic Burger Combo",
            weight="600",
            ingredients="Beef Patty, Cheddar Cheese, Lettuce, Tomato, French Fries, Soft Drink",
            description="Beef burger with lettuce, tomato, and cheddar cheese, accompanied by french fries and a soft drink.",
            price=14.90,
            active=True,
            file_name="combo_burger.jpg",
            category="combos"
        ),
        Menu(
            id=25,
            name="Chicken Wings Box",
            weight="450",
            ingredients="Chicken Wings, BBQ Sauce, French Fries",
            description="6 crispy chicken wings accompanied by BBQ sauce and french fries.",
            price=13.50,
            active=True,
            file_name="alitas.jpg",
            category="combos"
        ),
        Menu(
            id=26,
            name="Chicken Sandwich Combo",
            weight="450",
            ingredients="Chicken Breast, Lettuce, Mayonnaise, French Fries",
            description="Grilled chicken breast sandwich with lettuce and mayonnaise, with a side of french fries.",
            price=12.50,
            active=True,
            file_name="combo_sand_pollo.jpg",
            category="combos"
        ),
        Menu(
            id=27,
            name="Vegetarian Box",
            weight="400",
            ingredients="Wheat Tortilla, Hummus, Avocado, Vegetables",
            description="Fresh vegetable wrap with hummus and avocado, accompanied by a fresh salad.",
            price=12.90,
            active=True,
            file_name="box_veggie.jpg",
            category="combos"
        ),
        Menu(
            id=28,
            name="Chicken Tenders Combo",
            weight="400",
            ingredients="Breaded Chicken Breast, French Fries, Ranch Dressing",
            description="4 breaded chicken breast strips with french fries and ranch dressing.",
            price=11.90,
            active=True,
            file_name="tenders.jpg",
            category="combos"
        ),
        Menu(
            id=29,
            name="Club Sandwich Combo",
            weight="500",
            ingredients="Chicken, Bacon, Cheese, Lettuce, Tomato, French Fries",
            description="Three-layer sandwich with chicken, bacon, cheese, lettuce, tomato, and french fries.",
            price=13.90,
            active=True,
            file_name="club_sandwich.jpg",
            category="combos"
        ),
        Menu(
            id=30,
            name="Apple Tart",
            weight="150",
            ingredients="Apple, Cinnamon, Puff Pastry",
            description="Slice of baked apple tart with a hint of cinnamon.",
            price=5.50,
            active=True,
            file_name="tarta_manzana.jpg",
            category="desserts"
        ),
        Menu(
            id=31,
            name="Cheesecake",
            weight="140",
            ingredients="Cream Cheese, Biscuit, Strawberry Jam",
            description="Creamy cheesecake with a biscuit base and strawberry jam.",
            price=5.80,
            active=True,
            file_name="cheesecake.jpg",
            category="desserts"
        ),
        Menu(
            id=32,
            name="Brownie with Walnuts",
            weight="100",
            ingredients="Chocolate, Walnuts, Sugar, Egg",
            description="Portion of rich, intense chocolate brownie with walnuts.",
            price=4.50,
            active=True,
            file_name="brownie.jpg",
            category="desserts"
        ),
        Menu(
            id=33,
            name="Fresh Fruit Salad",
            weight="200",
            ingredients="Melon, Pineapple, Grape, Banana, Yogurt",
            description="Bowl of seasonal fresh fruits (melon, pineapple, grape, and banana) with yogurt.",
            price=4.80,
            active=True,
            file_name="ensalada_frutas.jpg",
            category="desserts"
        ),
        Menu(
            id=34,
            name="Vanilla Flan",
            weight="120",
            ingredients="Egg, Milk, Vanilla, Caramel",
            description="Classic caramel egg custard, smooth and creamy.",
            price=4.20,
            active=True,
            file_name="flan.jpg",
            category="desserts"
        ),
        Menu(
            id=35,
            name="Waffle with Fruits",
            weight="220",
            ingredients="Flour, Syrup, Strawberries, Banana",
            description="Crispy waffle served with syrup and strawberries or banner.",
            price=6.50,
            active=True,
            file_name="waffle.jpg",
            category="desserts"
        ),
        Menu(
            id=36,
            name="Mediterranean Salad",
            weight="300",
            ingredients="Lettuce, Cherry Tomato, Cucumber, Olives, Feta Cheese, Olive Oil",
            description="Mix of fresh lettuce, cherry tomatoes, cucumber, black olives, feta cheese, and a touch of extra virgin olive oil.",
            price=8.90,
            active=True,
            file_name="mediterranea.jpg",
            category="salads"
        ),
        Menu(
            id=37,
            name="Chickpea Veggie Burger",
            weight="450",
            ingredients="Chickpeas, Spices, Brioche Bun, Avocado, Vegan Mayonnaise, French Fries",
            description="Chickpea and spice-based burger, served on a brioche bun with avocado, lettuce, tomato, and vegan mayonnaise. Accompanied by french fries.",
            price=10.50,
            active=True,
            file_name="hamb_veggie.jpg",
            category="burgers"
        ),
        Menu(
            id=38,
            name="Halloumi Cheese Wrap",
            weight="380",
            ingredients="Wheat Tortilla, Halloumi Cheese, Peppers, Arugula, Yogurt Sauce",
            description="Wheat tortilla filled with grilled halloumi cheese, roasted peppers, arugula, and herbal yogurt sauce.",
            price=9.50,
            active=True,
            file_name="wrap_veggie.jpg",
            category="burgers"
        ),
        Menu(
            id=39,
            name="Caprese Sandwich",
            weight="300",
            ingredients="Sourdough Bread, Tomato, Fresh Mozzarella, Basil, Balsamic Vinegar",
            description="Toasted sourdough bread with fresh tomato slices, fresh mozzarella, basil leaves, and a drizzle of balsamic vinegar glaze.",
            price=8.50,
            active=True,
            file_name="caprese.jpg",
            category="burgers"
        ),
        Menu(
            id=40,
            name="Quinoa Bowl with Vegetables",
            weight="400",
            ingredients="Quinoa, Avocado, Zucchini, Eggplant, Peppers, Sesame Seeds",
            description="Quinoa base served with avocado, zucchini, eggplant, and roasted peppers, seasoned with sesame seeds and lemon.",
            price=10.90,
            active=True,
            file_name="quinoa_bowl.jpg",
            category="salads"
        ),
        Menu(
            id=41,
            name="Pesto Pasta with Cherry Tomatoes",
            weight="350",
            ingredients="Pasta, Basil, Pine Nuts, Parmesan, Cherry Tomatoes",
            description="Al dente pasta tossed in fresh basil pesto sauce, pine nuts, parmesan cheese, and confit cherry tomatoes.",
            price=9.80,
            active=True,
            file_name="pesto.jpg",
            category="salads"
        ),
        Menu(
            id=42,
            name="Pumpkin and Ginger Cream Soup",
            weight="350",
            ingredients="Pumpkin, Ginger, Pumpkin Seeds",
            description="Comforting and smooth cream soup made of baked pumpkin, with a subtle spicy touch of ginger and toasted pumpkin seeds.",
            price=6.50,
            active=True,
            file_name="crema_calabaza.jpg",
            category="soups"
        )
    ]

    added_count = 0

    for dish in dishes:
        existing_dish = session.query(Menu).filter_by(id=dish.id).first()
        if existing_dish:
            existing_dish.name = dish.name
            existing_dish.weight = dish.weight
            existing_dish.ingredients = dish.ingredients
            existing_dish.description = dish.description
            existing_dish.price = dish.price
            existing_dish.active = dish.active
            existing_dish.file_name = dish.file_name
            existing_dish.category = dish.category
        else:
            session.add(dish)
            added_count += 1

    try:
        session.commit()
        print(f"Base de datos actualizada correctamente. Platos añadidos: {added_count}")
    except IntegrityError:
        session.rollback()
        print("Error: Integridad violada, transacción revertida.")