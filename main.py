from sqlmodel import Field, Session, SQLModel, select, or_
from models import Client, Car, Order, Work, Employee, Part, Payment
from models import engine
from fastapi import FastAPI
app=FastAPI()

@app.get("аll_walkers")
def select_all_workers():
    with Session(engine) as session:
        workers = session.exec(select(Employee)).all()
        result = ""
        for worker in workers:
            result = f"ID: {worker.employee_id}, Имя: {worker.first_name} {worker.last_name}, Пост: {worker.position}"
            print(result)

@app.get("all_client")
def select_all_clients():
    with Session(engine) as session:
        clients = session.exec(select(Client)).all()
        result = ""
        for client in clients:
            result = f"ID: {client.client_id}, Имя: {client.first_name} {client.last_name}"
            print(result)

@app.get("аll_products")
def select_all_products():
    with Session(engine) as session:
        products = session.exec(select(Part)).all()
        result = ""
        for product in products:
            result = f"ID: {product.part_id}, Название: {product.name}"
            print(result)

@app.get("аll_walkers")
# Вывод тех клиентов, у которых следующая покупка будет кратна 10 (для учёта скидок)
def select_client10():
    with Session(engine) as session:
       # Здесь нужно переделать логику
       print("Функция select_client10 не реализована под новую структуру")

@app.get("epmty_product")
# Вывод продуктов, которые закончились
def select_empty_product():
    with Session(engine) as session:
        products = session.exec(select(Part).where(Part.quantity_in_stock == 0)).all()
        result = ""
        if not products:
            print("На складе имеются все продукты")
        else:
            for product in products:
                result = f"ID: {product.part_id}, Название: {product.name}"
                print(result)

@app.get("order of client")
# Вывод всех заказов определённого клиента
def select_order_of_client(client_id: int):
    with Session(engine) as session:
        client = session.get(Client, client_id)
        if not client:
            print("Клиента с таким id не найдено")
        else:
            print(f"Клиент: ID: {client.client_id}, Имя: {client.first_name} {client.last_name}")
            orders = session.exec(select(Order).where(Order.client_id == client_id)).all()
            if not orders:
                print("У этого клиента нет ни одного заказа")
            else:
                for order in orders:
                    print(f"  Заказ ID: {order.order_id}, Дата заказа: {order.order_date}, Общая сумма: {order.total_amount}")

@app.get("product of order")
# Вывод всех позиций в заказе
def select_products_of_order(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            print("Заказа с таким id не найдено")
        else:
            print(f"Заказ: {order.order_id}, Дата: {order.order_date}, Общая сумма: {order.total_amount}")
            if not order.work_orders:
                 print("В этом заказе нет работ")
            else:
                print("  Работы в заказе:")
                for work in order.work_orders:
                    print(f"    - ID работы: {work.work_id}, Название: {work.work_name}, Цена: {work.price}")
            if not order.payments:
                print("В этом заказе нет платежей")
            else:
                print("  Платежи в заказе:")
                for payment in order.payments:
                    print(f"   - ID платежа: {payment.payment_id}, Дата: {payment.payment_date}, Сумма: {payment.amount}")

