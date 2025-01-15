Ecommerce project in django framework using class based views:

Apps Created:
1) Users: Basic stuff like name, email, password using default django.contrib.auth and also added
custom classes and methods for forgot password such that user inputs a security question and its 
corresponding answer that will be the key for resetting the password.
Also then categorized users into two types: Sellers and Customers, where Sellers can place items to be
sold and Customers can place orders.
2) Products: Sellers can create categories, subcategories and with them both of being foreign key to 
the items(products) along with other attributes of products being price, discount, stock etc.
Also has an entity review for the products, one to many fields for users(one review per each product
per user).
3) Orders: Customers place orders from here, either using order now or add to art facility (done
primarily using get and post methods and class based views).

Templates primarily styled using Bootstrap 5 and CSS. 

Views Overview:

Below is a detailed description of each view and its functionality:
1)Order-Related Views

    OrderConfirmView (class-based)
        Purpose: Confirms an order for a specific item.
        Key Actions:
            Adds the selected item to the order list.
            Updates or creates the order for the current user.
            Deletes items from the cart once added to the order.
        Redirects to: order.

    OrderLView (class-based)
        Purpose: Displays a summary of the user's current orders.
        Template Used: order_summary.html
        Key Actions:
            Fetches all current orders for the logged-in user.
            Calculates the total price of the orders.
        Context Variables: cart_items, total_price.

    OrderIncreaseQuantityView (class-based)
        Purpose: Increases the quantity of an ordered item.
        Key Actions:
            Updates the order by incrementing the item quantity.

    OrderDecreaseQuantityView (class-based)
        Purpose: Decreases the quantity of an ordered item.
        Key Actions:
            Reduces the quantity of the item, or removes the item if the quantity is 1.

    OrderView (class-based)
        Purpose: Handles order creation.
        Template Used: order_form.html
        Key Actions:
            Displays a form to gather order details (e.g., address, phone).
            Processes the order and deducts stock from the items.
        Redirects to: my_orders.

    UserOrderBillView (class-based)
        Purpose: Displays a detailed bill for a specific order.
        Template Used: userorder_bill.html
        Context Variables: order.

    PreviousOrderListView (class-based)
        Purpose: Displays the list of all previous orders for the user.
        Template Used: userorder_list.html
        Key Actions:
            Fetches and sorts previous orders by date.

2)Cart-Related Views

    AddToCartView (class-based)
        Purpose: Adds an item to the user's cart.
        Key Actions:
            Creates or updates a Cart object for the user.
            Increments the item quantity if it already exists in the cart.

    CartListView (class-based)
        Purpose: Displays the current cart items.
        Template Used: cart_list.html
        Key Actions:
            Fetches all items in the user's cart.
            Calculates the total price of the cart.

    IncreaseQuantityView (class-based)
        Purpose: Increases the quantity of an item in the cart.
        Key Actions:
            Updates the cart item by incrementing its quantity.

    DecreaseQuantityView (class-based)
        Purpose: Decreases the quantity of an item in the cart.
        Key Actions:
            Reduces the quantity or removes the item if the quantity is 1.

    CartDeleteView (class-based)
        Purpose: Deletes an item from the cart.
        Key Actions:
            Removes the specified cart item for the user.

    CartOrderView (class-based)
        Purpose: Allows users to place orders directly from the cart.
        Template Used: cart_order.html
        Key Actions:
            Validates the order form and processes each cart item as an order.
            Deducts stock from the items and clears the cart.
        Redirects to: my_orders.
3)Category-Related Views

    CategoryCreateView (class-based)
        Purpose: Allows the creation of product categories.
        Template Used: category_create.html
        Key Features:
            Displays a form for adding a new category.
            Redirects to home upon successful submission.

    SubcategoryCreateView (class-based)
        Purpose: Allows the creation of subcategories under a category.
        Template Used: subcategory_create.html
        Key Features:
            Displays a form for adding subcategories.
            Redirects to home after successful submission.

4)Product-Related Views

    ItemCreateView (class-based)
        Purpose: Allows the creation of products under specific categories and subcategories.
        Template Used: item_create.html
        Key Features:
            Dynamically filters subcategories based on the selected category.
            Validates and adds subcategories to the product.
            Displays a success message upon successful creation.

    ItemListView (class-based)
        Purpose: Displays a list of all products.
        Template Used: home.html
        Context Variables: items (all products in the database).

    ItemDetailView (class-based)
        Purpose: Displays detailed information about a specific product.
        Template Used: product_detail.html
        Key Features:
            Fetches and displays reviews for the selected product.
            Context variable: reviews (all reviews for the product).

5)Search-Related Views

    SearchResultsListView (class-based)
        Purpose: Displays search results based on a query.
        Template Used: search_results.html
        Key Features:
            Filters products by name, category, or subcategories using case-insensitive matching.
            Displays a warning message if no products match the query.
            Redirects to home if the query is invalid or empty.

6)Review-Related Views

    ReviewView (class-based)
        Purpose: Handles the creation of reviews for products.
        Template Used: review_form.html
        Key Features:
            Ensures the user has purchased the product before allowing a review.
            Prevents duplicate reviews for the same product by the same user.
            Displays appropriate success or error messages.
            Redirects to home or the review form upon submission.



