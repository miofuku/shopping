from app.models import Item
from sqlalchemy import or_


def find_deals(budget, items):
    query = Item.query.filter(or_(*[Item.title.ilike(f'%{item}%') for item in items]))
    results = query.order_by(Item.price).all()

    # Find the best combination of items within budget
    selected_items = []
    total_cost = 0

    for item in results:
        if total_cost + item.price <= budget:
            selected_items.append({
                "name": item.title,
                "price": item.price,
                "stars": item.stars
            })
            total_cost += item.price

        if len(selected_items) == len(items):
            break

    return selected_items, total_cost

