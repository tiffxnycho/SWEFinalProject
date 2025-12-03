from . import orders, order_details, menu, manager_menu_items, reviews, manager_promos



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu.router)
    app.include_router(manager_menu_items.router)
    app.include_router(manager_promos.router)
    app.include_router(orders.employee_router)
    app.include_router(reviews.router)

