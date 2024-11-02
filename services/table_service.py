
from sqlalchemy.orm import Session
from database.models import Cars
import pandas as pd

def fetch_cars_data(session: Session) -> pd.DataFrame:
    """
    Извлекает все данные из таблицы Cars и возвращает их в формате DataFrame для дальнейшей обработки.
    """
    query = session.query(
        Cars.stockn,
        Cars.make,
        Cars.model,
        Cars.year,
        Cars.color,
        Cars.milage,
        Cars.engine,
        Cars.location,
        Cars.cost,
        Cars.inventoried,
        Cars.breakevendate,
        Cars.dismantled,
        Cars.purchesdate,
        Cars.age,
        Cars.payback,
        Cars.profit,
        Cars.xs,
        Cars.status,
        Cars.import_id
    ).all()

    # Преобразуем результат запроса в DataFrame
    columns = [
        "stockn", "make", "model", "year", "color", "milage", "engine", "location",
        "cost", "inventoried", "breakevendate", "dismantled", "purchesdate", "age",
        "payback", "profit", "xs", "status", "import_id"
    ]
    df = pd.DataFrame(query, columns=columns)
    return df
