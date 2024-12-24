from sqlmodel import Field, Session, SQLModel, select, or_
from models import Client, Car, Order, Work, Employee, Part, Payment
from models import engine, create_db_and_tables, populate_database
from fastapi import FastAPI

app = FastAPI()

# Создание базы данных
create_db_and_tables()
# Заполнение базы данных начальными значениями
populate_database()

@app.get("/all_workers")
def select_all_workers():
    with Session(engine) as session:
        workers = session.exec(select(Employee)).all()
        result = ""
        for worker in workers:
            result = f"ID: {worker.employee_id}, Имя: {worker.first_name} {worker.last_name}, Пост: {worker.position}"
            print(result)

@app.get("/all_clients")
def select_all_clients():
    with Session(engine) as session:
        clients = session.exec(select(Client)).all()
        result = ""
        for client in clients:
            result = f"ID: {client.client_id}, Имя: {client.first_name} {client.last_name}"
            print(result)

@app.get("/all_products")
def select_all_products():
    with Session(engine) as session:
        products = session.exec(select(Part)).all()
        result = ""
        for product in products:
            result = f"ID: {product.part_id}, Название: {product.name}"
            print(result)

@app.get("/empty_product")
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

@app.get("/order_of_client")
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

@app.get("/product_of_order")
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


@app.get("/find_work")
# Поиск работ по имени
def find_work_by_name(name: str):
    with Session(engine) as session:
        works = session.exec(select(Work).where(Work.work_name == name)).all()
        result = ""
        if not works:
             print("Работы с таким названием нет")
        else:
            for work in works:
                result = f"ID: {work.work_id}, Название: {work.work_name}"
                print(result)

@app.get("/find_client")
# Поиск клиентов по фамилии или имени
def find_client_by_name(name: str):
   with Session(engine) as session:
        clients = session.exec(select(Client).where(or_(Client.first_name == name, Client.last_name == name))).all()
        result = ""
        if not clients:
            print("Клиента с таким именем или фамилией нет")
        else:
            for client in clients:
                result = f"ID: {client.client_id}, Имя: {client.first_name} {client.last_name}"
                print(result)
