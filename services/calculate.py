from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Cars, Profits
import pandas as pd

# Функции расчета для одной машины
def calculate_age(inventoried_date):
    return (date.today() - inventoried_date).days if inventoried_date else None

def calculate_payback(breakevendate, inventoried_date):
    return (breakevendate - inventoried_date).days if breakevendate and inventoried_date else None

def calculate_profit(session, stockn, cost):
    if cost is None or pd.isna(cost):
        print(f"Cost is missing for stockn: {stockn}")
        return None

    last_cumulative_amount = (
        session.query(Profits.cumulative_amount)
        .filter(Profits.stockn == stockn)
        .order_by(Profits.date.desc())
        .first()
    )

    if last_cumulative_amount is None or pd.isna(last_cumulative_amount[0]):
        print(f"Cumulative amount is missing for stockn: {stockn}")
        return None

    profit = int(last_cumulative_amount[0] - cost)
    print(f"Calculated profit for stockn {stockn}: {profit}")
    return profit

def calculate_xs(session, stockn, cost):
    if cost is None or pd.isna(cost):
        print(f"Cost is missing for stockn: {stockn}")
        return None

    last_cumulative_amount = (
        session.query(Profits.cumulative_amount)
        .filter(Profits.stockn == stockn)
        .order_by(Profits.date.desc())
        .first()
    )

    if last_cumulative_amount is None or pd.isna(last_cumulative_amount[0]):
        print(f"Cumulative amount is missing for stockn: {stockn}")
        return None

    xs = round(last_cumulative_amount[0] / cost, 2)
    print(f"Calculated xs for stockn {stockn}: {xs}")
    return xs

# Агрегационные функции
def get_min_max_avg_sum(session, field, make=None, model=None, status=["active"]):
    query = session.query(
        func.min(getattr(Cars, field)),
        func.max(getattr(Cars, field)),
        func.avg(getattr(Cars, field)),
        func.sum(getattr(Cars, field))
    ).filter(Cars.status.in_(status))

    if make:
        query = query.filter(Cars.make == make)
    if model:
        query = query.filter(Cars.model == model)

    return query.first()

# Пример агрегации для конкретных полей
def get_aggregated_data(session, make=None, model=None, include_scrap=False):
    status_filter = ["active"]
    if include_scrap:
        status_filter.append("scrap")

    results = {
        "age": get_min_max_avg_sum(session, "age", make, model, status_filter),
        "payback": get_min_max_avg_sum(session, "payback", make, model, status_filter),
        "profit": get_min_max_avg_sum(session, "profit", make, model, status_filter),
        "xs": get_min_max_avg_sum(session, "xs", make, model, status_filter),
        "cost_sum": get_min_max_avg_sum(session, "cost", make, model, status_filter)[3],
        "profit_sum": get_min_max_avg_sum(session, "profit", make, model, status_filter)[3],
    }
    return results

# Функция для подсчета количества машин
def calculate_stock_count(filtered_df):
    return len(filtered_df)

# Функция для подсчета общей стоимости
def calculate_total_cost(filtered_df):
    """Вычисление общей стоимости автомобилей, игнорируя NaN значения."""
    return filtered_df['cost'].dropna().sum() or 0

# Функция для подсчета общей прибыли
def calculate_total_profit(filtered_df):
    return filtered_df['profit'].dropna().sum() or 0

# Функция для подсчета среднего значения xs
def calculate_average_xs(filtered_df):
    return filtered_df['xs'].dropna().mean() or 0

# Функция для подсчета среднего значения payback, игнорируя отрицательные значения
def calculate_average_until_payback(filtered_df):
    positive_payback = filtered_df['payback'].dropna()  # Убираем NaN значения
    positive_payback = positive_payback[positive_payback > 0]  # Оставляем только положительные значения
    return positive_payback.mean() if not positive_payback.empty else 0

# Функция для получения динамики прибыли
def get_profit_dynamics(session, stockn):
    profit_changes = session.query(Profits.change_amount).filter(Profits.stockn == stockn).order_by(
        Profits.date.desc()).all()

    formatted_changes = [
        f"⬆️ (+{int(change[0])})" if change[0] > 0 else f"⬇️ ({int(change[0])})" if change[0] < 0 else "0"
        for change in profit_changes
    ]

    return formatted_changes

def calculate_change_amount(session, profit_id, stockn, new_cumulative_amount, new_date):
    previous_profit = (
        session.query(Profits.cumulative_amount)
        .filter(Profits.stockn == stockn, Profits.date < new_date, Profits.id != profit_id)
        .order_by(Profits.date.desc())
        .first()
    )

    if previous_profit:
        return new_cumulative_amount - previous_profit[0]
    else:
        return new_cumulative_amount
