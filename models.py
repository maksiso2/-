from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session
from datetime import datetime

# Модели данных

class Client(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    phone_number: str
    orders: List["Order"] = Relationship(back_populates="client")

class Car(SQLModel, table=True):
    car_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    make: str = Field(index=True)
    model: str = Field(index=True)
    year: int
    orders: List["Order"] = Relationship(back_populates="car")

class Order(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    client_id: int = Field(foreign_key="client.client_id")
    car_id: int = Field(foreign_key="car.car_id")
    order_date: str
    total_amount: float
    client: Client = Relationship(back_populates="orders")
    car: Car = Relationship(back_populates="orders")
    work_orders: List["Work"] = Relationship(back_populates="order")
    payments: List["Payment"] = Relationship(back_populates="order")


class Work(SQLModel, table=True):
    work_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    order_id: int = Field(foreign_key="order.order_id")
    employee_id: int = Field(foreign_key="employee.employee_id")
    work_name: str
    price: float
    order: Order = Relationship(back_populates="work_orders")
    employee: "Employee" = Relationship(back_populates="work_orders")

class Employee(SQLModel, table=True):
    employee_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    position: str
    work_orders: List["Work"] = Relationship(back_populates="employee")


class Part(SQLModel, table=True):
    part_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str
    price: float
    quantity_in_stock: int


class Payment(SQLModel, table=True):
    payment_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    order_id: int = Field(foreign_key="order.order_id")
    payment_date: str
    amount: float
    order: Order = Relationship(back_populates="payments")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def populate_database():
    with Session(engine) as session:
         # Создаем клиентов
        client1 = Client(first_name="Иван", last_name="Иванов", phone_number="8-900-123-45-67")
        client2 = Client(first_name="Петр", last_name="Петров", phone_number="8-900-765-43-21")
        session.add(client1)
        session.add(client2)

        # Создаем машины
        car1 = Car(make="Toyota", model="Camry", year=2020)
        car2 = Car(make="BMW", model="X5", year=2021)
        session.add(car1)
        session.add(car2)

        # Создаем заказы
        order1 = Order(client_id=2, car_id=3, order_date=str(datetime.now().date()), total_amount=5000.00)
        order2 = Order(client_id=2, car_id=3, order_date=str(datetime.now().date()), total_amount=12000.00)
        session.add(order1)
        session.add(order2)

        # Создаем сотрудников
        employee1 = Employee(first_name="Сергей", last_name="Сидоров", position="Механик")
        employee2 = Employee(first_name="Алексей", last_name="Смирнов", position="Диагност")
        session.add(employee1)
        session.add(employee2)

        # Создаем работы
        work1 = Work(order_id=3, employee_id=3, work_name="Замена масла", price=1500.00)
        work2 = Work(order_id=3, employee_id=3, work_name="Диагностика двигателя", price=2500.00)
        session.add(work1)
        session.add(work2)

         # Создаем запчасти
        part1 = Part(name="Масло моторное", price=1000.00, quantity_in_stock=100)
        part2 = Part(name="Фильтр маслянный", price=500.00, quantity_in_stock=150)
        session.add(part1)
        session.add(part2)
         # Создаем платежи
        payment1 = Payment(order_id=3, payment_date=str(datetime.now().date()), amount=5000.00)
        payment2 = Payment(order_id=3, payment_date=str(datetime.now().date()), amount=12000.00)
        session.add(payment1)
        session.add(payment2)


        session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    populate_database()