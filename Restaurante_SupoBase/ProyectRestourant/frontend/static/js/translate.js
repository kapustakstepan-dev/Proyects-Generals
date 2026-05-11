// Diccionario de traducciones
const translations = {
    en: {
        nav_home: "Home", nav_menu: "Menu", nav_login: "Login", nav_register: "Register", nav_orders: "My Orders", nav_reserved: "Reservation", nav_logout: "Logout", nav_admin: "Admin",
        nav_salads: "🥗 Salads", nav_drinks: "🥤 Drinks", nav_combos: "🍔 Combos", nav_desserts: "🍰 Desserts", nav_burgers: "🥘 Main Dishes", nav_theme: "Change Theme",
        hero_title: "Welcome to RetroBite", hero_subtitle: "Taste the nostalgic flavors of the past, served with a modern twist.", hero_cta: "View Menu",
        menu_title: "Food From The Past", add_to_cart: "Add to Cart", order_now: "Order Now",
        login_title: "Welcome Back", login_btn: "Login", register_title: "Join the Club", register_btn: "Register",
        username_label: "Username", email_label: "Email", password_label: "Password", name_label: "Full Name",
        invoice_title: "RetroBite Receipt", invoice_send: "Send to Email", close: "Close",
        orders_title: "My Orders", my_orders_title: "My Orders", orders_empty: "No active orders found.", recent_orders_title: "Recent Orders",
        total: "Total", res_title: "Book a Table", res_subtitle: "Experience nostalgic dining at its best. Secure your spot today!",
        res_success: "Reservation submitted successfully! See you soon.", label_name: "Name", label_email: "Email", label_phone: "Phone", label_guests: "Guests",
        label_date: "Date", label_time: "Time", label_table_type: "Table Type", table_regular: "Regular Table", table_booth: "Cozy Booth", table_window: "Window Seat", table_outdoor: "Outdoor Terrace",
        btn_reserve: "Confirm Reservation", btn_reserve_more: "Book More Tables", btn_delete: "Delete", confirm_delete_res: "Are you sure you want to delete this reservation?",
        order_id: "Order #", status_delivered: "Delivered", status_preparing: "Preparing", status_onway: "On the Way", weight_label: "Weight", ingredients_label: "Ingredients",
        description_label: "Description:", back_to_menu: "Back to Menu", checkout_title: "Checkout", btn_confirm_order: "Confirm & Order", empty_basket_checkout: "Your basket is empty.",
        add_more_items: "Add more items &larr;", login_footer: "Don't have an account? ", register_footer: "Already have an account? ", login_link: "Login", register_link: "Register",
        error_404_subtitle: "Page Not Found", error_404_description1: "It seems you've lost yourself in time.", error_404_description2: "Return to the present for the best retro flavor!", error_404_btn: "BACK TO HOME",
        my_reservations_title: "My Reservations", no_active_reservations: "You have no active reservations.", go_to_reserve: "Go to reservations", recent_orders: "Recent Orders",
        no_recent_orders: "You have no recent orders.",
        admin_menu_crud: "Menu CRUD", admin_global_orders: "Global Orders", admin_reservations: "Reservations", admin_users: "Users", admin_exit: "Exit Admin",
        admin_gest_menu: "Menu Management", admin_add_plate: "+ Add Item", admin_img: "IMG", admin_name: "Name", admin_price: "Price", admin_status: "Status", admin_actions: "Actions",
        admin_active: "Active", admin_inactive: "Inactive", admin_edit: "Edit", admin_delete: "Delete", admin_new_plate: "New Item", admin_desc: "Description", admin_img_file: "Image (filename)",
        admin_add: "Add", admin_close: "Close", admin_ref: "Ref", admin_client: "Client", admin_total: "Total", admin_date: "Date", admin_action: "Action", admin_user: "User",
        admin_nickname: "Nickname", admin_role: "Role", admin_save: "Save Changes", admin_cancel: "Cancel", admin_active_menu: "Active in menu?",
        err_past_date: "Error: You cannot reserve a table for a past date.", label_id: "ID", view_details: "View Details &rarr;", checkout_btn: "Place Order Now",
        current_basket: "Current Basket", quantity_label: "Quantity", explore_menu: "Explore Menu", empty_basket: "Your basket is currently empty.",
        receipt_order_id: "Order #", receipt_total: "Total:", receipt_date: "Date:", receipt_items: "Items:", receipt_thanks: "Thank you for your visit!", receipt_keep_retro: "Keep it Retro.",
        item_retro_burger: "Retro Burger", desc_retro_burger: "Classic double patty with melted cheese, lettuce, and secret diner sauce.",
        item_arcade_nachos: "Arcade Nachos", desc_arcade_nachos: "Loaded corn chips with jalapeños, melted cheese, and salsa.",
        item_chicken_wrap: "Chicken Wrap", desc_chicken_wrap: "Tender grilled chicken with fresh veggies and garlic yogurt sauce.",
        item_crispy_fries: "Crispy Fries", desc_crispy_fries: "Crispy crinkle-cut fries seasoned with our special retro spice blend.",
        item_vintage_milkshake: "Vintage Milkshake", desc_vintage_milkshake: "Thick vanilla strawberry shake topped with whipped cream and a cherry.",
        item_classic_pizza: "Classic Pizza", desc_classic_pizza: "Cheesy pepperoni slice baked in our classic brick oven.",
        item_classic_lemonade: "Classic Lemonade", desc_classic_lemonade: "Natural freshly squeezed lemonade, served with ice and a fresh lemon slice.",
        item_natural_orange_juice: "Natural Orange Juice", desc_natural_orange_juice: "100% natural orange juice, freshly squeezed, with no added sugars.",
        item_iced_tea: "Iced Tea", desc_iced_tea: "Black iced tea with a touch of lemon or peach and fresh mint leaves.",
        item_strawberry_milkshake: "Strawberry Milkshake", desc_strawberry_milkshake: "Delicious creamy milkshake made with fresh strawberries and whole milk.",
        item_americano_coffee: "Americano Coffee", desc_americano_coffee: "Freshly roasted and ground coffee, served hot or on the rocks.",
        item_sparkling_mineral_water: "Sparkling Mineral Water", desc_sparkling_mineral_water: "Sparkling mineral water served with a touch of lemon.",
        item_chicken_noodle_soup: "Chicken Noodle Soup", desc_chicken_noodle_soup: "Comforting chicken broth with noodles, carrots, and celery.",
        item_vegetable_cream_soup: "Vegetable Cream Soup", desc_vegetable_cream_soup: "Smooth cream soup made with zucchini, carrots, and potatoes.",
        item_minestrone_soup: "Minestrone Soup", desc_minestrone_soup: "Traditional soup with pasta, tomatoes, beans, and fresh vegetables.",
        item_beef_consomm_é: "Beef Consommé", desc_beef_consomm_é: "Traditional beef broth accompanied by small diced vegetables.",
        item_tomato_and_basil_soup: "Tomato and Basil Soup", desc_tomato_and_basil_soup: "Soup made with ripe tomatoes and fresh basil, served with croutons.",
        item_homemade_lentil_soup: "Homemade Lentil Soup", desc_homemade_lentil_soup: "Slow-cooked lentil soup with carrots, potatoes, and a touch of spices.",
        item_classic_burger_combo: "Classic Burger Combo", desc_classic_burger_combo: "Beef burger with lettuce, tomato, and cheese, with fries and drink.",
        item_chicken_wings_box: "Chicken Wings Box", desc_chicken_wings_box: "6 crispy chicken wings accompanied by BBQ sauce and french fries.",
        item_chicken_sandwich_combo: "Chicken Sandwich Combo", desc_chicken_sandwich_combo: "Grilled chicken breast sandwich with lettuce and mayonnaise with fries.",
        item_vegetarian_box: "Vegetarian Box", desc_vegetarian_box: "Fresh vegetable wrap with hummus and avocado with a fresh salad.",
        item_chicken_tenders_combo: "Chicken Tenders Combo", desc_chicken_tenders_combo: "4 breaded chicken breast strips with french fries and ranch dressing.",
        item_club_sandwich_combo: "Club Sandwich Combo", desc_club_sandwich_combo: "Three-layer sandwich with chicken, bacon, cheese, tomato, and fries.",
        item_apple_tart: "Apple Tart", desc_apple_tart: "Slice of baked apple tart with a hint of cinnamon.",
        item_cheesecake: "Cheesecake", desc_cheesecake: "Creamy cheesecake with a biscuit base and strawberry jam.",
        item_brownie_with_walnuts: "Brownie with Walnuts", desc_brownie_with_walnuts: "Portion of rich, intense chocolate brownie with walnuts.",
        item_fresh_fruit_salad: "Fresh Fruit Salad", desc_fresh_fruit_salad: "Bowl of seasonal fresh fruits with yogurt.",
        item_vanilla_flan: "Vanilla Flan", desc_vanilla_flan: "Classic caramel egg custard, smooth and creamy.",
        item_waffle_with_fruits: "Waffle with Fruits", desc_waffle_with_fruits: "Crispy waffle served with syrup and strawberries or banana.",
        item_mediterranean_salad: "Mediterranean Salad", desc_mediterranean_salad: "Mix of fresh lettuce, cherry tomatoes, cucumber, olives, and feta.",
        item_chickpea_veggie_burger: "Chickpea Veggie Burger", desc_chickpea_veggie_burger: "Chickpea burger on brioche bun with avocado and vegan mayo.",
        item_halloumi_cheese_wrap: "Halloumi Cheese Wrap", desc_halloumi_cheese_wrap: "Wheat tortilla filled with grilled halloumi cheese and peppers.",
        item_caprese_sandwich: "Caprese Sandwich", desc_caprese_sandwich: "Toasted sourdough bread with fresh tomato, mozzarella, and basil.",
        item_quinoa_bowl_with_vegetables: "Quinoa Bowl with Vegetables", desc_quinoa_bowl_with_vegetables: "Quinoa base served with avocado, zucchini, and roasted peppers.",
        item_pesto_pasta_with_cherry_tomatoes: "Pesto Pasta", desc_pesto_pasta_with_cherry_tomatoes: "Al dente pasta tossed in fresh basil pesto and cherry tomatoes.",
        item_pumpkin_and_ginger_cream_soup: "Pumpkin Cream Soup", desc_pumpkin_and_ginger_cream_soup: "Smooth cream soup of baked pumpkin with a spicy touch of ginger."
    },
    es: {
        nav_home: "Inicio", nav_menu: "Menú", nav_login: "Iniciar sesión", nav_register: "Registrarse", nav_orders: "Pedidos", nav_reserved: "Reserva", nav_logout: "Cerrar sesión", nav_admin: "Admin",
        nav_salads: "🥗 Ensaladas", nav_drinks: "🥤 Bebidas", nav_combos: "🍔 Combos", nav_desserts: "🍰 Postres", nav_burgers: "🥘 Platos Principales", nav_theme: "Cambiar Tema",
        hero_title: "Bienvenido a RetroBite", hero_subtitle: "Prueba los sabores nostálgicos del pasado, servidos con un toque moderno.", hero_cta: "Ver Menú",
        menu_title: "Comida del Pasado", add_to_cart: "Añadir al carrito", order_now: "Pedir Ahora",
        login_title: "Bienvenido de nuevo", login_btn: "Entrar", register_title: "Únete al Club", register_btn: "Regístrate",
        username_label: "Usuario", email_label: "Correo", password_label: "Contraseña", name_label: "Nombre completo",
        invoice_title: "Recibo de RetroBite", invoice_send: "Enviar por correo", close: "Cerrar",
        orders_title: "Mis Pedidos", my_orders_title: "Mis Pedidos", orders_empty: "No tienes pedidos activos.", recent_orders_title: "Pedidos Recientes",
        total: "Total", res_title: "Reservar Mesa", res_subtitle: "Vive una experiencia gastronómica nostálgica. ¡Asegura tu lugar hoy!",
        res_success: "¡Reserva enviada con éxito! Nos vemos pronto.", label_name: "Nombre", label_email: "Correo", label_phone: "Teléfono", label_guests: "Personas",
        label_date: "Fecha", label_time: "Hora", label_table_type: "Tipo de Mesa", table_regular: "Mesa Regular", table_booth: "Box Acogedor", table_window: "Mesa de Ventana", table_outdoor: "Terraza",
        btn_reserve: "Confirmar Reserva", btn_reserve_more: "Reservar más", btn_delete: "Eliminar", confirm_delete_res: "¿Estás seguro de que quieres eliminar esta reserva?",
        order_id: "Pedido #", status_delivered: "Entregado", status_preparing: "Preparando", status_onway: "En camino", weight_label: "Peso", ingredients_label: "Ingredientes",
        description_label: "Descripción:", back_to_menu: "Volver al Menú", checkout_title: "Finalizar Compra", btn_confirm_order: "Confirmar Pedido", empty_basket_checkout: "Tu cesta está vacía.",
        add_more_items: "Añadir más productos", login_footer: "¿No tienes una cuenta? ", register_footer: "¿Ya tienes una cuenta? ", login_link: "Entrar", register_link: "Regístrate",
        error_404_subtitle: "Página no encontrada", error_404_description1: "Parece que te has perdido en el tiempo.", error_404_description2: "¡Vuelve al presente para disfrutar del mejor sabor retro!", error_404_btn: "VOLVER AL INICIO",
        my_reservations_title: "Mis Reservas", no_active_reservations: "No tienes reservas activas.", go_to_reserve: "Ir a reservar", recent_orders: "Pedidos Recientes",
        no_recent_orders: "No tienes pedidos recientes.",
        admin_menu_crud: "Gestión Menú", admin_global_orders: "Pedidos Globales", admin_reservations: "Reservas", admin_users: "Usuarios", admin_exit: "Salir de Admin",
        admin_gest_menu: "Gestión del Menú", admin_add_plate: "+ Añadir Plato", admin_img: "IMG", admin_name: "Nombre", admin_price: "Precio", admin_status: "Estado", admin_actions: "Acciones",
        admin_active: "Activo", admin_inactive: "Inactivo", admin_edit: "Editar", admin_delete: "Eliminar", admin_new_plate: "Nuevo Plato", admin_desc: "Descripción", admin_img_file: "Imagen (archivo)",
        admin_add: "Añadir", admin_close: "Cerrar", admin_ref: "Ref", admin_client: "Cliente", admin_total: "Total", admin_date: "Fecha", admin_action: "Acción", admin_user: "Usuario",
        admin_nickname: "Apodo", admin_role: "Rol", admin_save: "Guardar Cambios", admin_cancel: "Cancelar", admin_active_menu: "¿Activo en el menú?",
        err_past_date: "Error: No puedes reservar para una fecha pasada.", label_id: "ID", view_details: "Ver detalles &rarr;", checkout_btn: "Realizar Pedido",
        current_basket: "Cesta Actual", quantity_label: "Cantidad", explore_menu: "Explorar Menú", empty_basket: "Tu cesta está vacía.",
        receipt_order_id: "Pedido #", receipt_total: "Total:", receipt_date: "Fecha:", receipt_items: "Productos:", receipt_thanks: "¡Gracias por tu visita!", receipt_keep_retro: "Mantente Retro.",
        item_retro_burger: "Hamburguesa Retro", desc_retro_burger: "Doble hamburguesa clásica con queso derretido, lechuga y salsa secreta.",
        item_arcade_nachos: "Nachos Arcade", desc_arcade_nachos: "Nachos cargados con jalapeños, queso derretido y salsa.",
        item_chicken_wrap: "Wrap de Pollo", desc_chicken_wrap: "Pollo a la parrilla tierno con verduras frescas y salsa de yogur.",
        item_crispy_fries: "Papas Crujientes", desc_crispy_fries: "Papas fritas sazonadas con nuestra mezcla especial retro.",
        item_vintage_milkshake: "Batido Vintage", desc_vintage_milkshake: "Batido espeso de fresa y vainilla con crema batida y una cereza.",
        item_classic_pizza: "Pizza Clásica", desc_classic_pizza: "Porción de pizza con pepperoni horneada en horno de piedra.",
        item_classic_lemonade: "Limonada Clásica", desc_classic_lemonade: "Limonada natural recién exprimida, servida con hielo y rodaja de limón.",
        item_natural_orange_juice: "Jugo de Naranja Natural", desc_natural_orange_juice: "Jugo de naranja 100% natural, recién exprimido, sin azúcares añadidos.",
        item_iced_tea: "Té Helado", desc_iced_tea: "Té negro helado con un toque de limón o durazno y menta fresca.",
        item_strawberry_milkshake: "Batido de Fresa", desc_strawberry_milkshake: "Delicioso batido cremoso de fresas frescas y leche entera.",
        item_americano_coffee: "Café Americano", desc_americano_coffee: "Café recién tostado y molido, servido caliente o con hielo.",
        item_sparkling_mineral_water: "Agua Mineral con Gas", desc_sparkling_mineral_water: "Agua mineral con gas servida con un toque de limón.",
        item_chicken_noodle_soup: "Sopa de Pollo con Fideos", desc_chicken_noodle_soup: "Caldo de pollo reconfortante con fideos, zanahoria y apio.",
        item_vegetable_cream_soup: "Crema de Verduras", desc_vegetable_cream_soup: "Crema suave hecha con calabacín, zanahoria y patatas.",
        item_minestrone_soup: "Sopa Minestrone", desc_minestrone_soup: "Sopa tradicional con pasta, tomates, frijoles y verduras frescas.",
        item_beef_consomm_é: "Consomé de Res", desc_beef_consomm_é: "Caldo de res tradicional acompañado de verduras picadas.",
        item_tomato_and_basil_soup: "Sopa de Tomate y Albahaca", desc_tomato_and_basil_soup: "Sopa de tomates maduros y albahaca fresca, servida con crutones.",
        item_homemade_lentil_soup: "Sopa de Lentejas Casera", desc_homemade_lentil_soup: "Sopa de lentejas a fuego lento con zanahoria, patatas y especias.",
        item_classic_burger_combo: "Combo de Hamburguesa Clásica", desc_classic_burger_combo: "Hamburguesa de res con queso, lechuga, papas fritas y refresco.",
        item_chicken_wings_box: "Caja de Alitas de Pollo", desc_chicken_wings_box: "6 alitas crujientes acompañadas de salsa BBQ y papas fritas.",
        item_chicken_sandwich_combo: "Combo Sándwich de Pollo", desc_chicken_sandwich_combo: "Sándwich de pechuga de pollo con lechuga, mayonesa y papas.",
        item_vegetarian_box: "Caja Vegetariana", desc_vegetarian_box: "Wrap de verduras frescas con hummus y aguacate con ensalada.",
        item_chicken_tenders_combo: "Combo de Tenders de Pollo", desc_chicken_tenders_combo: "4 tiras de pollo empanado con papas fritas y aderezo ranch.",
        item_club_sandwich_combo: "Combo Club Sándwich", desc_club_sandwich_combo: "Sándwich de tres capas con pollo, tocino, queso, tomate y papas.",
        item_apple_tart: "Tarta de Manzana", desc_apple_tart: "Porción de tarta de manzana horneada con un toque de canela.",
        item_cheesecake: "Tarta de Queso", desc_cheesecake: "Tarta de queso cremosa con base de galleta y mermelada de fresa.",
        item_brownie_with_walnuts: "Brownie con Nueces", desc_brownie_with_walnuts: "Porción de brownie de chocolate intenso con nueces.",
        item_fresh_fruit_salad: "Ensalada de Frutas Frescas", desc_fresh_fruit_salad: "Bol de frutas frescas de temporada con yogur.",
        item_vanilla_flan: "Flan de Vainilla", desc_vanilla_flan: "Flan de huevo clásico con caramelo, suave y cremoso.",
        item_waffle_with_fruits: "Waffle con Frutas", desc_waffle_with_fruits: "Waffle crujiente servido con sirope y fresas o plátano.",
        item_mediterranean_salad: "Ensalada Mediterránea", desc_mediterranean_salad: "Mezcla de lechuga, tomates cherry, pepino, aceitunas y queso feta.",
        item_chickpea_veggie_burger: "Hamburguesa Vegana de Garbanzos", desc_chickpea_veggie_burger: "Hamburguesa de garbanzos en pan brioche con aguacate y mayo vegana.",
        item_halloumi_cheese_wrap: "Wrap de Queso Halloumi", desc_halloumi_cheese_wrap: "Tortilla de trigo rellena de queso halloumi a la parrilla y pimientos.",
        item_caprese_sandwich: "Sándwich Caprese", desc_caprese_sandwich: "Pan de masa madre tostado con tomate fresco, mozzarella y albahaca.",
        item_quinoa_bowl_with_vegetables: "Bol de Quinoa con Verduras", desc_quinoa_bowl_with_vegetables: "Base de quinoa servida con aguacate, calabacín y pimientos asados.",
        item_pesto_pasta_with_cherry_tomatoes: "Pasta al Pesto", desc_pesto_pasta_with_cherry_tomatoes: "Pasta al dente con salsa pesto de albahaca fresca y tomates cherry.",
        item_pumpkin_and_ginger_cream_soup: "Crema de Calabaza y Jengibre", desc_pumpkin_and_ginger_cream_soup: "Crema suave de calabaza horneada con un toque picante de jengibre."
    },
    ua: {
        nav_home: "Головна", nav_menu: "Меню", nav_login: "Увійти", nav_register: "Реєстрація", nav_orders: "Замовлення", nav_reserved: "Резерв", nav_logout: "Вийти", nav_admin: "Адмін",
        nav_salads: "🥗 Салати", nav_drinks: "🥤 Напої", nav_combos: "🍔 Комбо", nav_desserts: "🍰 Десерти", nav_burgers: "🥘 Основні страви", nav_theme: "Змінити тему",
        hero_title: "Ласкаво просимо до RetroBite", hero_subtitle: "Скуштуйте ностальгічні смаки минулого у сучасному виконанні.", hero_cta: "Переглянути меню",
        menu_title: "Їжа з минулого", add_to_cart: "Додати в кошик", order_now: "Замовити зараз",
        login_title: "З поверненням", login_btn: "Увійти", register_title: "Приєднуйся до клубу", register_btn: "Реєстрація",
        username_label: "Нікнейм", email_label: "Електронна пошта", password_label: "Пароль", name_label: "Повне ім'я",
        invoice_title: "Чек RetroBite", invoice_send: "Відправити на email", close: "Закрити",
        orders_title: "Мої Замовлення", my_orders_title: "Мої Замовлення", orders_empty: "Замовлень не знайдено.", recent_orders_title: "Історія Замовлень",
        total: "Всього", res_title: "Забронювати Столик", res_subtitle: "Відчуйте атмосферу ностальгії. Забронюйте столик вже сьогодні!",
        res_success: "Бронювання успішно надіслано! До зустрічі.", label_name: "Ім'я", label_email: "Email", label_phone: "Телефон", label_guests: "Гості",
        label_date: "Дата", label_time: "Час", label_table_type: "Тип Столика", table_regular: "Звичайний столик", table_booth: "Затишна кабінка", table_window: "Місце біля вікна", table_outdoor: "Тераса",
        btn_reserve: "Підтвердити", btn_reserve_more: "Бронювати ще", btn_delete: "Видалити", confirm_delete_res: "Ви впевнені, що хочете видалити це бронювання?",
        order_id: "Замовлення #", status_delivered: "Доставлено", status_preparing: "Готується", status_onway: "В дорозі", weight_label: "Вага", ingredients_label: "Інгредієнти",
        description_label: "Опис:", back_to_menu: "До Меню", checkout_title: "Оформлення", btn_confirm_order: "Підтвердити", empty_basket_checkout: "Ваш кошик порожній.",
        add_more_items: "Додати ще товари", login_footer: "Немає акаунту? ", register_footer: "Вже є акаунт? ", login_link: "Увійти", register_link: "Реєстрація",
        error_404_subtitle: "Сторінку не знайдено", error_404_description1: "Схоже, ви загубилися в часі.", error_404_description2: "Поверніться в сьогодення за найкращим ретро смаком!", error_404_btn: "НА ГОЛОВНУ",
        my_reservations_title: "Мої Бронювання", no_active_reservations: "У вас немає активних бронювань.", go_to_reserve: "Забронювати", recent_orders: "Останні замовлення",
        no_recent_orders: "У вас немає останніх замовлень.",
        admin_menu_crud: "Управління Меню", admin_global_orders: "Всі Замовлення", admin_reservations: "Бронювання", admin_users: "Користувачі", admin_exit: "Вийти з Адмінки",
        admin_gest_menu: "Управління Меню", admin_add_plate: "+ Додати Страву", admin_img: "Зображення", admin_name: "Назва", admin_price: "Ціна", admin_status: "Статус", admin_actions: "Дії",
        admin_active: "Активно", admin_inactive: "Неактивно", admin_edit: "Редагувати", admin_delete: "Видалити", admin_new_plate: "Нова Страва", admin_desc: "Опис", admin_img_file: "Зображення (файл)",
        admin_add: "Додати", admin_close: "Закрити", admin_ref: "№", admin_client: "Клієнт", admin_total: "Всього", admin_date: "Дата", admin_action: "Дія", admin_user: "Користувач",
        admin_nickname: "Нікнейм", admin_role: "Роль", admin_save: "Зберегти Зміни", admin_cancel: "Скасувати", admin_active_menu: "Активно в меню?",
        err_past_date: "Помилка: Не можна бронювати на минулу дату.", label_id: "ID", view_details: "Детальніше &rarr;", checkout_btn: "Замовити Зараз",
        current_basket: "Поточний Кошик", quantity_label: "Кількість", explore_menu: "Переглянути Меню", empty_basket: "Ваш кошик порожній.",
        receipt_order_id: "Замовлення №", receipt_total: "Разом:", receipt_date: "Дата:", receipt_items: "Товари:", receipt_thanks: "Дякуємо за візит!", receipt_keep_retro: "Залишайся в стилі Ретро.",
        item_retro_burger: "Ретро Бургер", desc_retro_burger: "Класична подвійна котлета з сиром, салатом та секретним соусом.",
        item_arcade_nachos: "Начос Аркада", desc_arcade_nachos: "Кукурудзяні чипси з халапеньйо, плавленим сиром та сальсою.",
        item_chicken_wrap: "Курячий Рол", desc_chicken_wrap: "Ніжна курка гриль зі свіжими овочами та часниковим соусом.",
        item_crispy_fries: "Хрустка Картопля", desc_crispy_fries: "Хрустка картопля фрі з нашими фірмовими ретро спеціями.",
        item_vintage_milkshake: "Вінтажний Мілкшейк", desc_vintage_milkshake: "Густий ванільно-полуничний шейк зі збитими вершками та вишнею.",
        item_classic_pizza: "Класична Піца", desc_classic_pizza: "Шматочок піци з пепероні, випеченої у класичній печі.",
        item_classic_lemonade: "Класичний Лимонад", desc_classic_lemonade: "Натуральний лимонад з льодом та свіжою часточкою лимона.",
        item_natural_orange_juice: "Натуральний Апельсиновий Сік", desc_natural_orange_juice: "100% натуральний апельсиновий сік без додавання цукру.",
        item_iced_tea: "Холодний Чай", desc_iced_tea: "Чорний чай з льодом, лимоном або персиком та свіжою м'ятою.",
        item_strawberry_milkshake: "Полуничний Мілкшейк", desc_strawberry_milkshake: "Смачний кремовий мілкшейк зі свіжої полуниці та незбираного молока.",
        item_americano_coffee: "Кава Американо", desc_americano_coffee: "Свіжообсмажена кава, що подається гарячою або з льодом.",
        item_sparkling_mineral_water: "Мінеральна Вода з Газом", desc_sparkling_mineral_water: "Газована мінеральна вода з часточкою лимона.",
        item_chicken_noodle_soup: "Курячий Суп з Локшиною", desc_chicken_noodle_soup: "Поживний курячий бульйон з локшиною, морквою та селерою.",
        item_vegetable_cream_soup: "Овочевий Крем-суп", desc_vegetable_cream_soup: "Ніжний крем-суп з кабачків, моркви та картоплі.",
        item_minestrone_soup: "Суп Мінестроне", desc_minestrone_soup: "Традиційний суп з пастою, томатами, квасолею та овочами.",
        item_beef_consomm_é: "Яловичий Консоме", desc_beef_consomm_é: "Традиційний яловичий бульйон з дрібно нарізаними овочами.",
        item_tomato_and_basil_soup: "Томатний Суп з Базиліком", desc_tomato_and_basil_soup: "Суп зі стиглих томатів та базиліку, подається з грінками.",
        item_homemade_lentil_soup: "Домашній Сочевичний Суп", desc_homemade_lentil_soup: "Густий суп із сочевиці з морквою, картоплею та спеціями.",
        item_classic_burger_combo: "Комбо Класичний Бургер", desc_classic_burger_combo: "Бургер з яловичини з сиром, салатом, картоплею та напоєм.",
        item_chicken_wings_box: "Курячі Крильця Бокс", desc_chicken_wings_box: "6 хрустких крилець з соусом барбекю та картоплею фрі.",
        item_chicken_sandwich_combo: "Комбо Курячий Сендвіч", desc_chicken_sandwich_combo: "Сендвіч з курячим філе, салатом, майонезом та картоплею.",
        item_vegetarian_box: "Вегетаріанський Бокс", desc_vegetarian_box: "Рол зі свіжих овочів з хумусом та авокадо, подається з салатом.",
        item_chicken_tenders_combo: "Комбо Курячі Тендери", desc_chicken_tenders_combo: "4 хрусткі курячі смужки з картоплею та соусом ранч.",
        item_club_sandwich_combo: "Комбо Клаб-сендвіч", desc_club_sandwich_combo: "Сендвіч з куркою, беконом, сиром, томатами та картоплею.",
        item_apple_tart: "Яблучний Тарт", desc_apple_tart: "Шматочок запеченого яблучного тарта з корицею.",
        item_cheesecake: "Чизкейк", desc_cheesecake: "Кремовий чизкейк на пісочній основі з полуничним джемом.",
        item_brownie_with_walnuts: "Брауні з Горіхами", desc_brownie_with_walnuts: "Насичений шоколадний брауні з волоськими горіхами.",
        item_fresh_fruit_salad: "Салат зі Свіжих Фруктів", desc_fresh_fruit_salad: "Боул сезонних фруктів з йогуртом.",
        item_vanilla_flan: "Ванільний Флан", desc_vanilla_flan: "Класичний десерт із яєчного крему з карамеллю.",
        item_waffle_with_fruits: "Вафлі з Фруктами", desc_waffle_with_fruits: "Хрусткі вафлі з сиропом та полуницею або бананом.",
        item_mediterranean_salad: "Середземноморський Салат", desc_mediterranean_salad: "Мікс салату, чері, огірків, оливок та сиру фета.",
        item_chickpea_veggie_burger: "Веганський Нутовий Бургер", desc_chickpea_veggie_burger: "Бургер з нуту на булочці бріош з авокадо та веганським майо.",
        item_halloumi_cheese_wrap: "Рол з Сиром Халумі", desc_halloumi_cheese_wrap: "Пшеничний рол з сиром халумі на грилі та перцем.",
        item_caprese_sandwich: "Сендвіч Капрезе", desc_caprese_sandwich: "Тост із хліба на заквасці з томатами, моцарелою та базиліком.",
        item_quinoa_bowl_with_vegetables: "Кіноа Боул з Овочами", desc_quinoa_bowl_with_vegetables: "Кіноа з авокадо, кабачками та печеним перцем.",
        item_pesto_pasta_with_cherry_tomatoes: "Паста Песто", desc_pesto_pasta_with_cherry_tomatoes: "Паста аль денте з соусом песто та томатами чері.",
        item_pumpkin_and_ginger_cream_soup: "Гарбузовий Крем-суп", desc_pumpkin_and_ginger_cream_soup: "Ніжний крем-суп із запеченого гарбуза з ноткою імбиру."
    }
};

// Clase para manejar las traducciones
class Translator {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'en';
        this.init();
    }

    init() {
        this.updateDOM();
        this.setupButtons();
    }

    // Cambia el idioma actual
    setLanguage(lang) {
        if (translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('language', lang);
            this.updateDOM();
            this.updateActiveButton();
        }
    }

    // Actualiza todos los elementos con data-i18n
    updateDOM() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = translations[this.currentLang][key];
            if (translation) {
                if (el.tagName === 'INPUT' && el.hasAttribute('placeholder')) {
                    el.setAttribute('placeholder', translation);
                } else {
                    el.innerHTML = translation;
                }
            }
        });
    }

    // Configura los botones de cambio de idioma
    setupButtons() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setLanguage(e.target.dataset.lang);
            });
        });
        this.updateActiveButton();
    }

    // Marca el botón del idioma activo
    updateActiveButton() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === this.currentLang);
        });
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    window.translator = new Translator();
});
