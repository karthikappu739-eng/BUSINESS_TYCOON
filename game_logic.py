import random

# ==========================================
# PRODUCTS
# ==========================================

PRODUCTS = {
    "Rice": {"cost": 40, "selling_price": 60},
    "Shirts": {"cost": 200, "selling_price": 350},
    "Headphones": {"cost": 500, "selling_price": 750},
    "Shoes": {"cost": 600, "selling_price": 900},
    "Water Bottles": {"cost": 50, "selling_price": 90},
    "Watches": {"cost": 800, "selling_price": 1200}
}


# ==========================================
# MARKETING CHANNELS
# ==========================================

MARKETING_CHANNELS = {
    "Social Media": {"cost": 1000, "reach": 1000, "demand": 10},
    "Newspaper": {"cost": 2000, "reach": 2000, "demand": 15},
    "Television": {"cost": 5000, "reach": 6000, "demand": 30}
}


# ==========================================
# COMPETITORS
# ==========================================

def create_competitors():

    return {
        "Alpha Enterprises": {
            "cash": 15000,
            "revenue": 0,
            "strength": 35,
            "multiplier": 1.0,
            "marketing": 1000,
            "strategy": "Balanced",
            "daily_sales": 0
        },
        "MegaMart": {
            "cash": 25000,
            "revenue": 0,
            "strength": 45,
            "multiplier": 0.95,
            "marketing": 2000,
            "strategy": "Low Price",
            "daily_sales": 0
        },
        "Prime Retail": {
            "cash": 20000,
            "revenue": 0,
            "strength": 40,
            "multiplier": 1.10,
            "marketing": 1500,
            "strategy": "Premium",
            "daily_sales": 0
        }
    }


# ==========================================
# CREATE BUSINESS
# ==========================================

def create_business():

    return {
        "business_name": "Karthik Enterprises",
        "cash": 10000,
        "revenue": 0,
        "cogs": 0,
        "expenses": 0,
        "inventory": {},
        "sales_history": [],
        "day": 1,
        "level": 1,
        "employees": 0,
        "marketing_budget": 0,
        "customer_demand": 20,
        "marketing_campaigns": [],
        "marketing_reach": 0,
        "competitors": create_competitors(),
        "competitor_history": [],
        "market_share": 0,
        "daily_missions_claimed": {},
        "total_units_purchased": 0,
        "total_units_sold": 0,
        "achievements_unlocked": []
    }


# ==========================================
# PURCHASE PRODUCTS
# ==========================================

def purchase_product(business, product, quantity):

    if product not in PRODUCTS:
        return "Product not found."

    if quantity <= 0:
        return "Enter a valid quantity."

    cost = PRODUCTS[product]["cost"] * quantity

    if business["cash"] < cost:
        return "Insufficient cash to purchase this product."

    business["cash"] -= cost

    business["inventory"][product] = (
        business["inventory"].get(product, 0) + quantity
    )

    business["cogs"] += cost

    business["total_units_purchased"] = (
        business.get("total_units_purchased", 0) + quantity
    )

    return f"Successfully purchased {quantity} units of {product}."


# ==========================================
# SELL PRODUCTS
# ==========================================

def sell_product(business, product, quantity):

    if product not in PRODUCTS:
        return "Product not found."

    if quantity <= 0:
        return "Enter a valid quantity."

    available = business["inventory"].get(product, 0)

    if available < quantity:
        return "Not enough inventory."

    selling_price = PRODUCTS[product]["selling_price"]
    revenue = selling_price * quantity

    business["inventory"][product] -= quantity
    business["cash"] += revenue
    business["revenue"] += revenue

    business["total_units_sold"] = (
        business.get("total_units_sold", 0) + quantity
    )

    business["sales_history"].append({
        "Day": business["day"],
        "Product": product,
        "Quantity": quantity,
        "Revenue": revenue
    })

    update_level(business)

    return f"Successfully sold {quantity} units of {product} for ₹{revenue:,}."


# ==========================================
# PROFIT CALCULATION
# ==========================================

def calculate_profit(business):

    return (
        business["revenue"]
        - business["cogs"]
        - business["expenses"]
    )


# ==========================================
# UPDATE BUSINESS LEVEL
# ==========================================

def update_level(business):

    profit = calculate_profit(business)

    if profit >= 50000:
        business["level"] = 5
    elif profit >= 25000:
        business["level"] = 4
    elif profit >= 10000:
        business["level"] = 3
    elif profit >= 5000:
        business["level"] = 2
    else:
        business["level"] = 1


# ==========================================
# BUSINESS SUMMARY
# ==========================================

def business_summary(business):

    profit = calculate_profit(business)

    return {
        "Business Name": business["business_name"],
        "Cash": f"₹{business['cash']:,}",
        "Revenue": f"₹{business['revenue']:,}",
        "Expenses": f"₹{business['expenses']:,}",
        "Cost of Goods Sold": f"₹{business['cogs']:,}",
        "Net Profit": f"₹{profit:,}",
        "Business Level": business["level"],
        "Employees": business["employees"],
        "Day": business["day"]
    }


# ==========================================
# MARKETING
# ==========================================

def launch_marketing(business, budget, channel="Social Media"):

    if channel not in MARKETING_CHANNELS:
        return "Invalid marketing channel."

    details = MARKETING_CHANNELS[channel]

    if budget != details["cost"]:
        return "Invalid marketing budget."

    if business["cash"] < budget:
        return "Insufficient cash for marketing."

    business["cash"] -= budget
    business["expenses"] += budget
    business["marketing_budget"] += budget

    business["customer_demand"] = min(
        100,
        business["customer_demand"] + details["demand"]
    )

    business["marketing_reach"] += details["reach"]

    business["marketing_campaigns"].append({
        "Day": business["day"],
        "Channel": channel,
        "Cost": budget,
        "Reach": details["reach"]
    })

    return f"{channel} campaign launched successfully!"


# ==========================================
# EMPLOYEE MANAGEMENT
# ==========================================

def hire_employee(business):

    hiring_cost = 500

    if business["cash"] < hiring_cost:
        return "Insufficient cash to hire an employee."

    business["cash"] -= hiring_cost
    business["expenses"] += hiring_cost
    business["employees"] += 1

    return "Employee hired successfully!"


def pay_salaries(business):

    salary = business["employees"] * 500

    if business["cash"] < salary:
        return "Insufficient cash to pay salaries."

    business["cash"] -= salary
    business["expenses"] += salary

    return f"Salaries paid successfully: ₹{salary:,}"


# ==========================================
# COMPETITOR STRATEGIES
# ==========================================

def update_competitor_strategies(business):

    competitors = business.get("competitors", {})

    strategies = [
        "Balanced",
        "Low Price",
        "Premium",
        "Aggressive Marketing"
    ]

    for competitor in competitors.values():

        if random.random() < 0.25:
            competitor["strategy"] = random.choice(strategies)

        if competitor["strategy"] == "Low Price":
            competitor["multiplier"] = 0.95

        elif competitor["strategy"] == "Premium":
            competitor["multiplier"] = 1.10

        elif competitor["strategy"] == "Aggressive Marketing":
            competitor["marketing"] += 200

        else:
            competitor["multiplier"] = 1.0


# ==========================================
# AI COMPETITOR SALES
# ==========================================

def simulate_competitor_sales(business):

    competitors = business.get("competitors", {})

    for competitor in competitors.values():

        strategy = competitor.get("strategy", "Balanced")

        if strategy == "Low Price":
            units = random.randint(15, 30)

        elif strategy == "Premium":
            units = random.randint(5, 15)

        elif strategy == "Aggressive Marketing":
            units = random.randint(20, 40)

        else:
            units = random.randint(10, 25)

        average_price = random.randint(100, 500)

        daily_revenue = units * average_price

        competitor["revenue"] += daily_revenue
        competitor["cash"] += daily_revenue
        competitor["daily_sales"] = daily_revenue

    return competitors


# ==========================================
# MARKET SHARE
# ==========================================

def calculate_market_share(business):

    competitors = business.get("competitors", {})

    player_strength = (
        business["customer_demand"]
        + min(business["marketing_reach"] / 100, 50)
        + min(business["revenue"] / 1000, 100)
    )

    competitor_strengths = []

    for competitor in competitors.values():

        strength = (
            competitor["strength"]
            + competitor["marketing"] / 100
            + competitor["revenue"] / 1000
        )

        competitor_strengths.append(strength)

    total_strength = player_strength + sum(competitor_strengths)

    if total_strength <= 0:
        business["market_share"] = 0
    else:
        business["market_share"] = (
            player_strength / total_strength
        ) * 100

    return round(business["market_share"], 2)


# ==========================================
# COMPETITOR RANKINGS
# ==========================================

def get_competitor_rankings(business):

    rankings = [{
        "name": business["business_name"],
        "revenue": business["revenue"],
        "type": "Player"
    }]

    for name, details in business["competitors"].items():

        rankings.append({
            "name": name,
            "revenue": details["revenue"],
            "type": "Competitor"
        })

    rankings.sort(
        key=lambda x: x["revenue"],
        reverse=True
    )

    return rankings


# ==========================================
# COMPETITOR SUMMARY
# ==========================================

def get_competitor_summary(business):

    return {
        "Market Share": calculate_market_share(business),
        "Competitor Count": len(business["competitors"]),
        "Rankings": get_competitor_rankings(business)
    }


# ==========================================
# BUSINESS EVENTS
# ==========================================

def generate_business_event(business):

    events = [
        {
            "name": "Unexpected Customer Demand",
            "message": "A sudden increase in customer demand!",
            "cash": 1000
        },
        {
            "name": "Equipment Repair",
            "message": "Your business needs unexpected repairs.",
            "cash": -1000
        },
        {
            "name": "New Customer",
            "message": "You received a new customer bonus!",
            "cash": 2000
        },
        {
            "name": "Market Slowdown",
            "message": "Market conditions are unfavourable.",
            "cash": -500
        },
        {
            "name": "Business Opportunity",
            "message": "You discovered a profitable opportunity!",
            "cash": 1500
        }
    ]

    event = random.choice(events)
    amount = event["cash"]

    if amount < 0:
        business["cash"] += amount
        business["expenses"] += abs(amount)
    else:
        business["cash"] += amount
        business["revenue"] += amount

    return f"{event['name']}: {event['message']} (₹{amount:+,})"


def random_business_event(business):

    return generate_business_event(business)


# ==========================================
# DAILY MISSIONS
# ==========================================

def get_daily_missions(business):

    current_day = business["day"]

    today_sales = [
        sale for sale in business["sales_history"]
        if sale["Day"] == current_day
    ]

    units_sold = sum(
        sale["Quantity"] for sale in today_sales
    )

    today_revenue = sum(
        sale["Revenue"] for sale in today_sales
    )

    today_campaigns = [
        campaign for campaign in business["marketing_campaigns"]
        if campaign["Day"] == current_day
    ]

    claimed = business.setdefault("daily_missions_claimed", {})
    day_claimed = claimed.setdefault(str(current_day), [])

    missions = [
        {
            "id": "sell_5",
            "name": "Product Seller",
            "description": "Sell 5 products today.",
            "progress": min(units_sold, 5),
            "target": 5,
            "reward": 500
        },
        {
            "id": "marketing",
            "name": "Marketing Champion",
            "description": "Launch one marketing campaign today.",
            "progress": min(len(today_campaigns), 1),
            "target": 1,
            "reward": 750
        },
        {
            "id": "revenue",
            "name": "Revenue Master",
            "description": "Generate ₹2,000 revenue today.",
            "progress": min(today_revenue, 2000),
            "target": 2000,
            "reward": 1000
        }
    ]

    for mission in missions:
        mission["completed"] = mission["progress"] >= mission["target"]
        mission["claimed"] = mission["id"] in day_claimed

    return missions


def claim_daily_mission(business, mission_id):

    missions = get_daily_missions(business)

    for mission in missions:

        if mission["id"] == mission_id:

            if not mission["completed"]:
                return "Mission not completed yet."

            if mission["claimed"]:
                return "You have already claimed this reward."

            business["cash"] += mission["reward"]

            business["daily_missions_claimed"].setdefault(
                str(business["day"]), []
            ).append(mission_id)

            return f"Mission completed! You earned ₹{mission['reward']:,}."

    return "Mission not found."


# ==========================================
# ACHIEVEMENT SYSTEM
# ==========================================

def get_achievements(business):

    achievements = [
        {
            "id": "first_sale",
            "name": "First Sale",
            "description": "Complete your first sale.",
            "icon": "🛍️",
            "target": 1,
            "progress": min(business.get("total_units_sold", 0), 1)
        },
        {
            "id": "smart_shopper",
            "name": "Smart Shopper",
            "description": "Purchase 10 products.",
            "icon": "🛒",
            "target": 10,
            "progress": min(business.get("total_units_purchased", 0), 10)
        },
        {
            "id": "marketing_expert",
            "name": "Marketing Expert",
            "description": "Launch 5 marketing campaigns.",
            "icon": "📢",
            "target": 5,
            "progress": min(len(business.get("marketing_campaigns", [])), 5)
        },
        {
            "id": "hiring_manager",
            "name": "Hiring Manager",
            "description": "Hire 5 employees.",
            "icon": "👥",
            "target": 5,
            "progress": min(business.get("employees", 0), 5)
        },
        {
            "id": "business_tycoon",
            "name": "Business Tycoon",
            "description": "Reach ₹50,000 total revenue.",
            "icon": "👑",
            "target": 50000,
            "progress": min(business.get("revenue", 0), 50000)
        }
    ]

    unlocked = business.setdefault("achievements_unlocked", [])

    for achievement in achievements:

        achievement["completed"] = (
            achievement["progress"] >= achievement["target"]
        )

        if achievement["completed"] and achievement["id"] not in unlocked:
            unlocked.append(achievement["id"])

        achievement["unlocked"] = achievement["id"] in unlocked

    return achievements


# ==========================================
# NEXT DAY
# ==========================================

def next_day(business):

    business["day"] += 1

    business["customer_demand"] = max(
        20,
        business["customer_demand"] - 2
    )

    daily_salary = business["employees"] * 100

    if business["cash"] >= daily_salary:
        business["cash"] -= daily_salary
        business["expenses"] += daily_salary

    update_competitor_strategies(business)

    simulate_competitor_sales(business)

    calculate_market_share(business)

    event = generate_business_event(business)

    business["competitor_history"].append({
        "Day": business["day"],
        "Market Share": business["market_share"],
        "Event": event,
        "Competitor Revenue": {
            name: details["revenue"]
            for name, details in business["competitors"].items()
        }
    })

    update_level(business)

    return f"Day {business['day']} started! {event}"