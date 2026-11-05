import json
from datetime import datetime

import pandas as pd
import streamlit as st

from game_logic import (
    create_business,
    purchase_product,
    sell_product,
    business_summary,
    next_day,
    PRODUCTS,
    MARKETING_CHANNELS,
    launch_marketing,
    hire_employee,
    pay_salaries,
    generate_business_event,
    calculate_market_share,
    get_competitor_rankings,
    get_daily_missions,
    claim_daily_mission,
    get_achievements,
    calculate_profit,
)

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Business Tycoon Simulator",
    page_icon="🏢",
    layout="wide",
)

# =========================================================
# PREMIUM GAMING UI - ANIMATED DESIGN
# =========================================================

st.markdown(
    """
    <style>

    :root {
        --bg-deep: #080b18;
        --bg-panel: rgba(20, 25, 48, 0.88);
        --bg-card: rgba(28, 34, 63, 0.82);
        --purple: #9b6bff;
        --blue: #36c5ff;
        --gold: #f4c96b;
        --text-main: #f4f3ff;
        --text-muted: #a8acc8;
        --border: rgba(151, 120, 255, 0.25);
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 15% 15%,
                rgba(83, 48, 170, 0.20),
                transparent 35%
            ),
            radial-gradient(
                ellipse at 85% 75%,
                rgba(26, 128, 190, 0.16),
                transparent 38%
            ),
            linear-gradient(
                135deg,
                #080b18,
                #10142a,
                #0a1020
            );

        background-size: 150% 150%;
        animation: ambientDrift 22s ease-in-out infinite alternate;
        color: var(--text-main);
    }

    /* Moving background particles */

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: 0.42;

        background-image:
            radial-gradient(
                2px 2px at 12% 22%,
                rgba(160, 132, 255, .65),
                transparent 100%
            ),
            radial-gradient(
                2px 2px at 76% 18%,
                rgba(54, 197, 255, .65),
                transparent 100%
            ),
            radial-gradient(
                1.5px 1.5px at 42% 72%,
                rgba(160, 132, 255, .6),
                transparent 100%
            ),
            radial-gradient(
                2px 2px at 88% 82%,
                rgba(54, 197, 255, .55),
                transparent 100%
            ),
            radial-gradient(
                1.5px 1.5px at 25% 88%,
                rgba(244, 201, 107, .45),
                transparent 100%
            );

        background-size: 420px 420px;
        animation: particleFloat 34s linear infinite;
    }

    @keyframes ambientDrift {
        0% {
            background-position: 0% 30%;
        }

        100% {
            background-position: 100% 70%;
        }
    }

    @keyframes particleFloat {
        from {
            transform: translate3d(0, 0, 0);
        }

        to {
            transform: translate3d(-35px, -55px, 0);
        }
    }

    /* Keep app content above background */

    .stMainBlockContainer,
    [data-testid="stSidebar"] > div {
        position: relative;
        z-index: 1;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            rgba(16, 20, 42, .98),
            rgba(12, 16, 33, .98)
        );

        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #d8c7ff;
        letter-spacing: 0.4px;
    }

    /* Headings */

    h1, h2, h3 {
        color: #d0b7ff;
        letter-spacing: 0.3px;
    }

    h1 {
        text-shadow: 0 0 22px rgba(155, 107, 255, .28);
        animation: titlePulse 5s ease-in-out infinite;
    }

    @keyframes titlePulse {
        0%, 100% {
            text-shadow: 0 0 14px rgba(155, 107, 255, .18);
        }

        50% {
            text-shadow: 0 0 25px rgba(54, 197, 255, .34);
        }
    }

    p, label, [data-testid="stCaptionContainer"] {
        color: var(--text-muted);
    }

    /* Metric cards */

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(31, 38, 72, .92),
            rgba(17, 23, 48, .92)
        );

        border: 1px solid rgba(139, 112, 230, .30);
        border-radius: 16px;
        padding: 16px 18px;

        box-shadow: 0 8px 24px rgba(0, 0, 0, .18);

        transition:
            transform .22s ease,
            border-color .22s ease,
            box-shadow .22s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: rgba(54, 197, 255, .65);

        box-shadow: 0 12px 28px rgba(54, 120, 255, .13);
    }

    [data-testid="stMetricLabel"] {
        color: #aeb5d6 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 750;
    }

    /* Buttons */

    div.stButton > button,
    div.stDownloadButton > button {
        background: linear-gradient(
            105deg,
            #6937d5,
            #8d4df2 52%,
            #267fca
        );

        background-size: 200% 100%;
        color: white;

        border: 1px solid rgba(190, 165, 255, .32);
        border-radius: 11px;

        font-weight: 700;
        min-height: 44px;
        width: 100%;

        transition:
            transform .2s ease,
            box-shadow .2s ease,
            background-position .35s ease;

        box-shadow: 0 5px 18px rgba(102, 57, 210, .20);
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background-position: 100% 0;
        color: white;

        border-color: rgba(54, 197, 255, .75);
        transform: translateY(-2px);

        box-shadow: 0 8px 24px rgba(54, 130, 255, .28);
    }

    div.stButton > button:active,
    div.stDownloadButton > button:active {
        transform: scale(.98);
    }

    /* Sidebar navigation */

    section[data-testid="stSidebar"] [role="radiogroup"] > label {
        background: rgba(35, 41, 75, .48);
        border: 1px solid transparent;
        border-radius: 10px;

        padding: 8px 10px;
        margin: 3px 0;

        transition: all .18s ease;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {
        background: rgba(112, 77, 202, .25);
        border-color: rgba(155, 107, 255, .42);
        transform: translateX(3px);
    }

    /* Containers */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--border) !important;
        border-radius: 15px !important;
        background: rgba(20, 25, 48, .50);
    }

    /* Tables */

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* Inputs */

    input,
    textarea,
    [data-baseweb="select"] > div {
        background-color: #171d38 !important;
        color: white !important;
        border-color: rgba(155, 107, 255, .35) !important;
        border-radius: 9px !important;
    }

    /* Progress bars */

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #36c5ff
        );
    }

    /* Responsive design */

    @media (max-width: 768px) {
        .stMainBlockContainer {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.8rem;
        }
    }

    /* Respect reduced-motion settings */

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================

if "business" not in st.session_state:
    st.session_state.business = create_business()

business = st.session_state.business


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def show_message(result):
    """Display a message returned by game logic."""
    if result:
        st.info(result)


def money(value):
    """Format numbers as Indian Rupees."""
    return f"₹{value:,.0f}"


def make_business_report(data):
    """Create a downloadable text report."""

    lines = []

    lines.append("=" * 55)
    lines.append("          BUSINESS TYCOON SIMULATOR")
    lines.append("             FINAL BUSINESS REPORT")
    lines.append("=" * 55)

    lines.append("")
    lines.append(f"Report Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    lines.append(f"Business Name: {data.get('business_name', 'Business Empire')}")
    lines.append(f"Business Day: {data.get('day', 1)}")

    lines.append("")
    lines.append("-" * 55)
    lines.append("FINANCIAL SUMMARY")
    lines.append("-" * 55)

    lines.append(f"Cash Balance: {money(data.get('cash', 0))}")
    lines.append(f"Total Revenue: {money(data.get('revenue', 0))}")
    lines.append(f"Total Expenses: {money(data.get('expenses', 0))}")
    lines.append(f"Total Profit: {money(calculate_profit(data))}")

    lines.append("")
    lines.append("-" * 55)
    lines.append("INVENTORY")
    lines.append("-" * 55)

    for product, quantity in data.get("inventory", {}).items():
        lines.append(f"{product}: {quantity} units")

    lines.append("")
    lines.append("-" * 55)
    lines.append("SALES HISTORY")
    lines.append("-" * 55)

    for sale in data.get("sales_history", []):
        lines.append(str(sale))

    lines.append("")
    lines.append("-" * 55)
    lines.append("MARKETING CAMPAIGNS")
    lines.append("-" * 55)

    for campaign in data.get("marketing_campaigns", []):
        lines.append(str(campaign))

    lines.append("")
    lines.append("=" * 55)
    lines.append("                 END OF REPORT")
    lines.append("=" * 55)

    return "\n".join(lines)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
# =========================================================
# SIDEBAR NAVIGATION
with st.sidebar:

    st.markdown(
        """
        <h1 style="
            text-align:center;
            font-size:25px;
            color:#c8aaff;
            text-shadow:0 0 15px rgba(155,107,255,.6);
        ">
            🏢 BUSINESS TYCOON
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Build your business empire")

    st.markdown("---")

    pages = [
        "🏠 Empire Dashboard",
        "🛒 Marketplace",
        "💰 Sell Products",
        "📦 Inventory",
        "📢 Marketing Centre",
        "👥 Employee Headquarters",
        "🎲 Business Events",
        "📊 Statistics & Analytics",
        "🏢 Competitor Intelligence",
        "🎯 Daily Missions",
        "🏆 Achievements",
        "📄 Final Business Report",
    ]

    selected_page = st.radio(
        "NAVIGATION",
        pages,
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown("### 💰 Empire Status")

    st.metric(
        "Available Cash",
        money(business.get("cash", 0)),
    )

    st.metric(
        "Business Level",
        business.get("level", 1),
    )

    st.metric(
        "Current Day",
        business.get("day", 1),
    )

    st.markdown("---")

    # SAVE GAME

    st.markdown("### 💾 Save Your Game")

    save_data = json.dumps(
        business,
        indent=4,
        default=str,
    )

    st.download_button(
        label="⬇️ Download Save File",
        data=save_data,
        file_name="business_tycoon_save.json",
        mime="application/json",
        use_container_width=True,
    )

    # LOAD GAME

    st.markdown("### 📂 Load Saved Game")

    uploaded_file = st.file_uploader(
        "Upload your save file",
        type=["json"],
        key="load_game_file",
    )

    if uploaded_file is not None:

        try:
            loaded_data = json.load(uploaded_file)

            required_keys = [
                "cash",
                "revenue",
                "inventory",
                "sales_history",
                "day",
            ]

            if all(key in loaded_data for key in required_keys):

                if st.button(
                    "📂 Load Game",
                    use_container_width=True,
                ):

                    st.session_state.business = loaded_data

                    st.success("Game loaded successfully!")

                    st.rerun()

            else:
                st.error("Invalid save file format.")

        except Exception as error:
            st.error(f"Unable to load file: {error}")

    st.markdown("---")

    # RESTART GAME

    st.markdown("### 🔄 Restart")

    if st.button(
        "Start New Business",
        use_container_width=True,
    ):

        st.session_state.business = create_business()

        st.success("A new business empire has been created!")

        st.rerun()

    st.caption(
        "⚠️ Download your save file before restarting."
    )


# =========================================================
# MAIN APPLICATION HEADER
# =========================================================

st.markdown(
    """
<div style="padding:24px;border-radius:18px;margin-bottom:20px;background:linear-gradient(115deg,rgba(104,57,202,.30),rgba(34,119,183,.20));border:1px solid rgba(155,107,255,.35);box-shadow:0 8px 30px rgba(0,0,0,.18);">
<div style="color:#9cbdff;font-size:12px;letter-spacing:3px;font-weight:700;">THE ULTIMATE BUSINESS SIMULATION</div>
<h1 style="font-size:36px;margin:8px 0;color:#ffffff;">🏢 BUSINESS TYCOON SIMULATOR</h1>
<p style="font-size:15px;margin-bottom:0;">Build your company. Outsmart competitors. Create your business empire.</p>
</div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 1. EMPIRE DASHBOARD
# =========================================================

if selected_page == "🏠 Empire Dashboard":

    st.title("🏠 Empire Dashboard")

    st.caption(
        "Your business overview and financial performance."
    )

    summary = business_summary(business)

    # TOP METRICS

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Cash Balance",
            money(business.get("cash", 0)),
        )

    with col2:
        st.metric(
            "📈 Total Revenue",
            money(business.get("revenue", 0)),
        )

    with col3:
        st.metric(
            "🏆 Business Level",
            business.get("level", 1),
        )

    with col4:
        st.metric(
            "📅 Business Day",
            business.get("day", 1),
        )

    st.markdown("---")

    # BUSINESS PERFORMANCE

    st.subheader("📊 Business Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        inventory_units = sum(
            business.get("inventory", {}).values()
        )

        st.metric(
            "📦 Inventory Units",
            inventory_units,
        )

    with col2:
        employee_count = int(business.get("employees", 0))

        st.metric(
            "👥 Employees",
            employee_count,
        )

    with col3:
        profit = calculate_profit(business)

        st.metric(
            "💵 Total Profit",
            money(profit),
        )

    st.markdown("---")

    # MARKET SHARE

    market_share = calculate_market_share(business)

    st.subheader("🌍 Market Position")

    st.progress(
        min(max(float(market_share) / 100, 0.0), 1.0)
    )

    st.markdown(
        f"**Your Market Share:** {market_share:.2f}%"
    )

    st.markdown("---")

            # BUSINESS SUMMARY

    st.subheader("📋 Business Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        st.metric("💰 Available Cash", money(business.get("cash", 0)))
        st.metric("📈 Total Revenue", money(business.get("revenue", 0)))
        st.metric("📦 Cost of Goods Sold", money(business.get("cogs", 0)))
        st.metric("👥 Employees", business.get("employees", 0))

    with summary_col2:
        st.metric("💵 Net Profit", money(calculate_profit(business)))
        st.metric("🏢 Business Level", business.get("level", 1))
        st.metric("📅 Current Day", business.get("day", 1))
        st.metric("🌍 Market Share", f"{calculate_market_share(business):.2f}%")

    st.markdown("---")
    
    # NEXT DAY

    st.subheader("⏭️ Business Operations")

    st.info(
        "Ready to move to the next business day? "
        "Your business operations and competitors will progress."
    )

    if st.button(
        "⏭️ COMPLETE DAY & CONTINUE",
        use_container_width=True,
    ):

        result = next_day(business)

        show_message(result)

        st.success("Your business has moved to the next day!")

        st.rerun()


# =========================================================
# 2. MARKETPLACE
# =========================================================

elif selected_page == "🛒 Marketplace":

    st.title("🛒 Business Marketplace")

    st.caption(
        "Purchase products and build your inventory."
    )

    st.metric(
        "Available Cash",
        money(business.get("cash", 0)),
    )

    st.markdown("---")

    st.subheader("🛍️ Available Products")

    columns = st.columns(3)

    for index, (product_name, product_data) in enumerate(
        PRODUCTS.items()
    ):

        with columns[index % 3]:

            purchase_price = product_data["cost"]

            selling_price = product_data["selling_price"]

            gross_margin = selling_price - purchase_price

            margin_percentage = (
                (gross_margin / purchase_price) * 100
                if purchase_price > 0
                else 0
            )

            with st.container(border=True):

                st.markdown(
                    f"### 📦 {product_name}"
                )

                st.markdown(
                    f"**Purchase Price:** {money(purchase_price)}"
                )

                st.markdown(
                    f"**Selling Price:** {money(selling_price)}"
                )

                st.markdown(
                    f"**Potential Margin:** {money(gross_margin)}"
                )

                st.success(
                    f"Gross Margin: {margin_percentage:.1f}%"
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=100,
                    value=1,
                    step=1,
                    key=f"buy_{product_name}",
                )

                total_cost = purchase_price * quantity

                st.write(
                    f"**Total Cost: {money(total_cost)}**"
                )

                if st.button(
                    "🛒 PURCHASE",
                    key=f"purchase_{product_name}",
                    use_container_width=True,
                ):

                    result = purchase_product(
                        business,
                        product_name,
                        quantity,
                    )

                    show_message(result)

                    st.rerun()


# =========================================================
# 3. SELL PRODUCTS
# =========================================================

elif selected_page == "💰 Sell Products":

    st.title("💰 Sell Your Products")

    st.caption(
        "Convert your inventory into revenue."
    )

    inventory = business.get("inventory", {})

    available_products = {
        product: quantity
        for product, quantity in inventory.items()
        if quantity > 0
    }

    if not available_products:

        st.warning(
            "Your inventory is empty. Visit the Marketplace "
            "and purchase products before selling."
        )

    else:

        selected_product = st.selectbox(
            "Select Product",
            list(available_products.keys()),
        )

        available_quantity = available_products[
            selected_product
        ]

        product_price = PRODUCTS[
            selected_product
        ]["selling_price"]

        st.metric(
            "Available Stock",
            available_quantity,
        )

        quantity_to_sell = st.number_input(
            "Quantity to Sell",
            min_value=1,
            max_value=int(available_quantity),
            value=1,
            step=1,
        )

        expected_revenue = (
            product_price * quantity_to_sell
        )

        st.markdown("---")

        st.metric(
            "Expected Sales Revenue",
            money(expected_revenue),
        )

        st.caption(
            "Actual profit depends on your purchase cost "
            "and business expenses."
        )

        if st.button(
            "💰 SELL PRODUCTS",
            use_container_width=True,
        ):

            result = sell_product(
                business,
                selected_product,
                quantity_to_sell,
            )

            show_message(result)

            st.rerun()

            # =========================================================
# 4. INVENTORY
# =========================================================

elif selected_page == "📦 Inventory":

    st.title("📦 Inventory Management")

    st.caption(
        "Monitor stock levels and the value of your inventory."
    )

    inventory = business.get("inventory", {})

    inventory_data = []

    for product_name, quantity in inventory.items():

        product_data = PRODUCTS.get(product_name, {})

        purchase_price = product_data.get(
            "cost",
            0,
        )

        selling_price = product_data.get(
            "selling_price",
            0,
        )

        inventory_value = quantity * purchase_price

        potential_sales = quantity * selling_price

        inventory_data.append(
            {
                "Product": product_name,
                "Quantity": quantity,
                "Purchase Price": purchase_price,
                "Selling Price": selling_price,
                "Stock Value": inventory_value,
                "Potential Sales": potential_sales,
            }
        )

    if inventory_data:

        inventory_df = pd.DataFrame(inventory_data)

        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True,
        )

        total_units = inventory_df["Quantity"].sum()

        total_stock_value = inventory_df["Stock Value"].sum()

        total_potential_sales = inventory_df[
            "Potential Sales"
        ].sum()

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📦 Total Units",
                int(total_units),
            )

        with col2:
            st.metric(
                "💰 Stock Value",
                money(total_stock_value),
            )

        with col3:
            st.metric(
                "📈 Potential Sales",
                money(total_potential_sales),
            )

    else:

        st.info("No inventory data available.")


# =========================================================
# 5. MARKETING CENTRE
# =========================================================

elif selected_page == "📢 Marketing Centre":

    st.title("📢 Marketing Command Centre")

    st.caption(
        "Invest in marketing campaigns to increase customer demand "
        "and expand your brand reach."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Available Cash",
            money(business.get("cash", 0)),
        )

    with col2:
        st.metric(
            "👥 Customer Demand",
            business.get("customer_demand", 0),
        )

    st.markdown("---")

    st.subheader("🚀 Launch a Marketing Campaign")

    for index, (channel_name, channel_data) in enumerate(
        MARKETING_CHANNELS.items()
    ):

        with st.container(border=True):

            st.markdown(f"### 📣 {channel_name}")

            if isinstance(channel_data, dict):

                campaign_cost = channel_data.get("cost", 0)
                reach = channel_data.get("reach", 0)
                demand_increase = channel_data.get("demand", 0)

            else:
                campaign_cost = 0
                reach = 0
                demand_increase = 0

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Campaign Cost",
                    money(campaign_cost),
                )

            with col2:
                st.metric(
                    "Potential Reach",
                    f"{reach:,}",
                )

            with col3:
                st.metric(
                    "Demand Increase",
                    demand_increase,
                )

            if st.button(
                f"🚀 Launch {channel_name}",
                key=f"marketing_{index}",
                use_container_width=True,
            ):

                result = launch_marketing(
                    business,
                    campaign_cost,
                    channel_name,
                )

                show_message(result)

                st.rerun()

    st.markdown("---")

    st.subheader("📊 Marketing Campaign History")

    marketing_history = business.get(
        "marketing_campaigns",
        [],
    )

    if marketing_history:

        marketing_df = pd.DataFrame(
            marketing_history
        )

        st.dataframe(
            marketing_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "You haven't launched any marketing campaigns yet."
        )


# =========================================================
# 6. EMPLOYEE HEADQUARTERS
# =========================================================

elif selected_page == "👥 Employee Headquarters":

    st.title("👥 Employee Headquarters")

    st.caption(
        "Build your team and manage employee expenses."
    )

    employee_count = int(business.get("employees", 0))

    hiring_cost = 500

    daily_salary_per_employee = 100

    daily_salary_cost = (
        employee_count * daily_salary_per_employee
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👥 Total Employees",
            employee_count,
        )

    with col2:
        st.metric(
            "💵 Hiring Cost",
            money(hiring_cost),
        )

    with col3:
        st.metric(
            "📅 Daily Salary Expense",
            money(daily_salary_cost),
        )

    st.markdown("---")

    # HIRING

    st.subheader("➕ Hire a New Employee")

    st.write(
        f"Each new employee costs {money(hiring_cost)} to hire."
    )

    if st.button(
        "👤 HIRE EMPLOYEE",
        use_container_width=True,
    ):

        result = hire_employee(business)

        show_message(result)

        st.rerun()

    st.markdown("---")

    # WORKFORCE SUMMARY

    st.subheader("🏢 Your Workforce")

    if employee_count > 0:
        st.success(
            f"Your business has {employee_count} employee(s). "
            f"Daily salary cost: {money(daily_salary_cost)}."
        )

        workforce_df = pd.DataFrame([
            {
                "Workforce": "General Employees",
                "Employee Count": employee_count,
                "Daily Salary per Employee": money(daily_salary_per_employee),
                "Total Daily Salary": money(daily_salary_cost),
            }
        ])

        st.dataframe(
            workforce_df,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info(
            "Your company currently has no employees. "
            "Hire employees to grow your workforce."
        )

    st.markdown("---")

    # PAY SALARIES

    st.subheader("💳 Salary Management")

    st.warning(
        f"Estimated daily salary expense: "
        f"{money(daily_salary_cost)}"
    )

    if st.button(
        "💳 PAY EMPLOYEE SALARIES",
        use_container_width=True,
    ):

        result = pay_salaries(business)

        show_message(result)

        st.rerun()


# =========================================================
# 7. BUSINESS EVENTS
# =========================================================

elif selected_page == "🎲 Business Events":

    st.title("🎲 Business Events")

    st.caption(
        "Unexpected events can create opportunities or challenges."
    )

    st.markdown(
        """
        <div style="
            padding:20px;
            border-radius:15px;
            background:linear-gradient(
                120deg,
                rgba(112,67,205,.22),
                rgba(35,130,190,.16)
            );
            border:1px solid rgba(155,107,255,.35);
        ">
            <h3>🎯 The Business World Is Unpredictable</h3>
            <p>
                Every business faces unexpected opportunities,
                market changes and financial challenges.
                Generate an event and see how your business responds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Current Cash",
            money(business.get("cash", 0)),
        )

    with col2:
        st.metric(
            "📅 Current Day",
            business.get("day", 1),
        )

    st.markdown("---")

    st.subheader("🎲 Generate a Random Business Event")

    if st.button(
        "🎲 GENERATE BUSINESS EVENT",
        use_container_width=True,
    ):

        result = generate_business_event(business)

        if result:
            st.success(str(result))
        else:
            st.info("A business event has been generated.")

        st.rerun()

# =========================================================
# 8. STATISTICS & ANALYTICS - CEO DASHBOARD
# =========================================================

elif selected_page == "📊 Statistics & Analytics":

    st.title("📊 CEO Business Analytics Dashboard")

    st.caption(
        "Track financial performance, sales growth and business trends."
    )

    revenue = business.get("revenue", 0)
    expenses = business.get("expenses", 0)
    cogs = business.get("cogs", 0)
    profit = calculate_profit(business)

    sales_history = business.get("sales_history", [])

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    st.subheader("💼 Business Performance")

    margin = (profit / revenue * 100) if revenue > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Revenue",
        money(revenue)
    )

    col2.metric(
        "💵 Net Profit",
        money(profit)
    )

    col3.metric(
        "📦 Units Sold",
        f"{business.get('total_units_sold', 0):,}"
    )

    col4.metric(
        "📊 Profit Margin",
        f"{margin:.2f}%"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # FINANCIAL OVERVIEW
    # -----------------------------------------------------

    st.subheader("💹 Financial Overview")

    finance_col1, finance_col2 = st.columns(2)

    with finance_col1:

        st.metric(
            "Operating Expenses",
            money(expenses)
        )

    with finance_col2:

        st.metric(
            "Cost of Goods Sold",
            money(cogs)
        )

    st.markdown("---")

    # -----------------------------------------------------
    # PREPARE DAILY SALES DATA
    # -----------------------------------------------------

    if sales_history:

        sales_df = pd.DataFrame(sales_history)

        required_columns = {
            "Day",
            "Product",
            "Quantity",
            "Revenue"
        }

        if required_columns.issubset(sales_df.columns):

            sales_df["Day"] = pd.to_numeric(
                sales_df["Day"],
                errors="coerce"
            )

            sales_df["Quantity"] = pd.to_numeric(
                sales_df["Quantity"],
                errors="coerce"
            )

            sales_df["Revenue"] = pd.to_numeric(
                sales_df["Revenue"],
                errors="coerce"
            )

            sales_df = sales_df.dropna(
                subset=["Day", "Quantity", "Revenue"]
            )

            sales_df["Day"] = sales_df["Day"].astype(int)

            if not sales_df.empty:

                current_day = int(business.get("day", 1))

                daily_data = (
                    sales_df.groupby("Day")
                    .agg(
                        Revenue=("Revenue", "sum"),
                        Units_Sold=("Quantity", "sum"),
                        Transactions=("Revenue", "count")
                    )
                )

                daily_data = daily_data.reindex(
                    range(
                        int(daily_data.index.min()),
                        current_day + 1
                    ),
                    fill_value=0
                )

                daily_data.index.name = "Day"

                daily_data["Cumulative_Revenue"] = (
                    daily_data["Revenue"].cumsum()
                )

                # -------------------------------------------------
                # REVENUE TREND
                # -------------------------------------------------

                st.subheader("📈 Daily Revenue Growth")

                st.line_chart(
                    daily_data[["Revenue"]],
                    height=350,
                    use_container_width=True
                )

                st.markdown("---")

                # -------------------------------------------------
                # CUMULATIVE REVENUE
                # -------------------------------------------------

                st.subheader("💰 Cumulative Revenue Growth")

                st.line_chart(
                    daily_data[["Cumulative_Revenue"]],
                    height=300,
                    use_container_width=True
                )

                st.markdown("---")

                # -------------------------------------------------
                # UNITS SOLD
                # -------------------------------------------------

                st.subheader("📦 Daily Units Sold")

                st.line_chart(
                    daily_data[["Units_Sold"]],
                    height=300,
                    use_container_width=True
                )

                st.markdown("---")

                # -------------------------------------------------
                # TRANSACTIONS
                # -------------------------------------------------

                st.subheader("🛒 Daily Sales Transactions")

                st.line_chart(
                    daily_data[["Transactions"]],
                    height=300,
                    use_container_width=True
                )

                st.markdown("---")

                # -------------------------------------------------
                # PRODUCT PERFORMANCE
                # -------------------------------------------------

                st.subheader("🏆 Product Performance")

                product_data = (
                    sales_df.groupby("Product")
                    .agg(
                        Units_Sold=("Quantity", "sum"),
                        Revenue=("Revenue", "sum"),
                        Transactions=("Revenue", "count")
                    )
                    .sort_values(
                        "Revenue",
                        ascending=False
                    )
                )

                product_col1, product_col2 = st.columns(2)

                with product_col1:

                    st.write("Revenue by Product")

                    st.bar_chart(
                        product_data[["Revenue"]],
                        height=300
                    )

                with product_col2:

                    st.write("Units Sold by Product")

                    st.bar_chart(
                        product_data[["Units_Sold"]],
                        height=300
                    )

                st.dataframe(
                    product_data,
                    use_container_width=True
                )

                st.markdown("---")

                # -------------------------------------------------
                # DAILY PERFORMANCE TABLE
                # -------------------------------------------------

                st.subheader("📋 Day-wise Performance Report")

                display_data = daily_data.reset_index()

                display_data.columns = [
                    "Business Day",
                    "Daily Revenue",
                    "Units Sold",
                    "Transactions",
                    "Cumulative Revenue"
                ]

                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "⬇️ Download Analytics Report",
                    data=display_data.to_csv(index=False),
                    file_name="business_analytics.csv",
                    mime="text/csv"
                )

            else:

                st.info(
                    "No valid sales records are available yet."
                )

        else:

            st.warning(
                "Sales history is missing required information."
            )

    else:

        st.info(
            "📊 Your analytics dashboard will populate "
            "after you complete your first product sale."
        )

        st.write(
            "Visit Marketplace, purchase products, "
            "and sell them to generate business data."
        )

    st.markdown("---")

    # -----------------------------------------------------
    # BUSINESS PERFORMANCE SCORE
    # -----------------------------------------------------

    st.subheader("🏆 Business Performance Score")

    market_share = calculate_market_share(business)

    achievements = get_achievements(business)

    unlocked_achievements = sum(
        1
        for achievement in achievements
        if achievement.get("unlocked", False)
    )

    total_sales = len(sales_history)

    revenue_score = min(revenue / 100000 * 30, 30)

    profit_score = min(
        max(profit / 50000 * 30, 0),
        30
    )

    market_score = min(market_share / 5 * 20, 20)

    sales_score = min(total_sales / 20 * 10, 10)

    achievement_score = min(
        unlocked_achievements,
        10
    )

    total_score = min(
        max(
            revenue_score
            + profit_score
            + market_score
            + sales_score
            + achievement_score,
            0
        ),
        100
    )

    st.metric(
        "⭐ Overall Business Score",
        f"{total_score:.1f}/100"
    )

    st.progress(total_score / 100)

    if total_score >= 80:

        st.success(
            "Excellent! Your business is performing strongly."
        )

    elif total_score >= 50:

        st.info(
            "Good progress. Keep improving your business."
        )

    else:

        st.warning(
            "Your business needs more growth and better performance."
        )
# =========================================================
# 9. COMPETITOR INTELLIGENCE
# =========================================================

elif selected_page == "🏢 Competitor Intelligence":

    st.title("🏢 Competitor Intelligence")

    st.caption(
        "Monitor your competitors, compare performance "
        "and understand your market position."
    )

    market_share = calculate_market_share(business)

    rankings = get_competitor_rankings(business)

    st.subheader("🌍 Your Market Position")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📊 Your Market Share",
            f"{market_share:.2f}%",
        )

    with col2:
        st.metric(
            "💰 Your Revenue",
            money(business.get("revenue", 0)),
        )

    st.markdown("---")

    st.subheader("🏆 Competitor Rankings")

    if rankings:

        rankings_df = pd.DataFrame(rankings)

        st.dataframe(
            rankings_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")

        st.subheader("📈 Competitor Revenue Comparison")

        if "revenue" in rankings_df.columns:

            chart_df = rankings_df.copy()

            if "name" in chart_df.columns:

                chart_df = chart_df.set_index("name")

                st.bar_chart(
                    chart_df["revenue"]
                )

            else:

                st.bar_chart(
                    chart_df["revenue"]
                )

    else:

        st.info(
            "Competitor rankings are not available yet."
        )

    st.markdown("---")

    st.subheader("🔍 Competitor Details")

    if rankings:

        for index, competitor in enumerate(rankings):

            if isinstance(competitor, dict):

                competitor_name = competitor.get(
                    "name",
                    f"Competitor {index + 1}",
                )

                with st.expander(
                    f"🏢 {competitor_name}"
                ):

                    for key, value in competitor.items():

                        if key.lower() in [
                            "cash",
                            "revenue",
                            "strength",
                        ]:

                            if isinstance(value, (int, float)):

                                st.write(
                                    f"**{key.title()}:** {money(value)}"
                                )

                            else:

                                st.write(
                                    f"**{key.title()}:** {value}"
                                )

                        else:

                            st.write(
                                f"**{key.replace('_', ' ').title()}:** {value}"
                            )

    else:

        st.info(
            "No competitor details are currently available."
        )

        # =========================================================
# 10. DAILY MISSIONS
# =========================================================

elif selected_page == "🎯 Daily Missions":

    st.title("🎯 Daily Business Missions")

    st.caption(
        "Complete business challenges and earn rewards."
    )

    missions = get_daily_missions(business)

    st.subheader("📋 Available Missions")

    if missions:

        completed_missions = 0

        for index, mission in enumerate(missions):

            if not isinstance(mission, dict):
                continue

            mission_name = mission.get(
                "name",
                f"Mission {index + 1}",
            )

            description = mission.get(
                "description",
                "Complete this business challenge.",
            )

            reward = mission.get(
                "reward",
                0,
            )

            progress = mission.get(
                "progress",
                0,
            )

            target = mission.get(
                "target",
                1,
            )

            claimed = mission.get(
                "claimed",
                False,
            )

            completed = mission.get(
                "completed",
                False,
            )

            if target > 0:

                progress_percentage = min(
                    max(progress / target, 0),
                    1,
                )

            else:

                progress_percentage = 0

            with st.container(border=True):

                st.markdown(
                    f"### 🎯 {mission_name}"
                )

                st.write(description)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Progress",
                        f"{progress}/{target}",
                    )

                with col2:
                    st.metric(
                        "Reward",
                        money(reward),
                    )

                st.progress(
                    progress_percentage
                )

                if completed:
                    st.success("Mission completed!")

                    completed_missions += 1

                if claimed:

                    st.info(
                        "Reward already claimed."
                    )

                elif completed:

                    if st.button(
                        "🎁 CLAIM REWARD",
                        key=f"claim_mission_{index}",
                        use_container_width=True,
                    ):

                        result = claim_daily_mission(
                            business,
                            mission.get("id"),
                        )

                        show_message(result)

                        st.rerun()

                else:

                    st.warning(
                        "Complete the mission to unlock your reward."
                    )

        st.markdown("---")

        st.subheader("📊 Mission Progress")

        st.metric(
            "Completed Missions",
            completed_missions,
        )

        st.progress(
            completed_missions / len(missions)
        )

    else:

        st.info(
            "No daily missions are available right now."
        )


# =========================================================
# 11. ACHIEVEMENTS
# =========================================================

elif selected_page == "🏆 Achievements":

    st.title("🏆 Business Achievements")

    st.caption(
        "Unlock achievements as you build your business empire."
    )

    achievements = get_achievements(business)

    if achievements:

        unlocked_count = sum(
            1
            for achievement in achievements
            if achievement.get("unlocked", False)
        )

        total_achievements = len(achievements)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🏆 Unlocked",
                unlocked_count,
            )

        with col2:
            st.metric(
                "🎯 Total Achievements",
                total_achievements,
            )

        st.progress(
            unlocked_count / total_achievements
            if total_achievements > 0
            else 0
        )

        st.markdown("---")

        st.subheader("🌟 Achievement Collection")

        columns = st.columns(2)

        for index, achievement in enumerate(achievements):

            if not isinstance(achievement, dict):
                continue

            achievement_name = achievement.get(
                "name",
                f"Achievement {index + 1}",
            )

            description = achievement.get(
                "description",
                "Business achievement",
            )

            unlocked = achievement.get(
                "unlocked",
                False,
            )

            with columns[index % 2]:

                with st.container(border=True):

                    if unlocked:

                        st.markdown(
                            f"### 🏆 {achievement_name}"
                        )

                        st.success("UNLOCKED")

                    else:

                        st.markdown(
                            f"### 🔒 {achievement_name}"
                        )

                        st.warning("LOCKED")

                    st.write(description)

    else:

        st.info(
            "Start growing your business to unlock achievements."
        )


# =========================================================
# 12. FINAL BUSINESS REPORT
# =========================================================

elif selected_page == "📄 Final Business Report":

    st.title("📄 Final Business Report")

    st.caption(
        "A complete overview of your business performance, "
        "financial position and competitive standing."
    )

    # FINANCIAL DATA

    revenue = business.get("revenue", 0)

    expenses = business.get("expenses", 0)

    profit = calculate_profit(business)

    market_share = calculate_market_share(business)

    rankings = get_competitor_rankings(business)

    # REPORT METRICS

    st.subheader("💼 Executive Financial Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📈 Total Revenue",
            money(revenue),
        )

    with col2:
        st.metric(
            "💸 Total Expenses",
            money(expenses),
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "💰 Net Profit",
            money(profit),
        )

    with col4:
        st.metric(
            "🌍 Market Share",
            f"{market_share:.2f}%",
        )

    st.markdown("---")

    # MANAGEMENT SUMMARY

    st.subheader("📋 Management Summary")

    business_name = business.get("business_name", "Business Empire")
    current_day = business.get("day", 1)

    inventory_units = sum(
        business.get("inventory", {}).values()
    )

    employee_count = int(business.get("employees", 0))
    total_sales = len(business.get("sales_history", []))

    st.markdown(
        f"""<div style="padding:22px;border-radius:15px;background:linear-gradient(120deg,rgba(104,57,202,.20),rgba(34,119,183,.15));border:1px solid rgba(155,107,255,.35);">
<h3>🏢 {business_name}</h3>
<p>This report presents the current performance of your business empire.</p>
<p><b>Business Day:</b> {current_day}</p>
<p><b>Total Revenue:</b> {money(revenue)}</p>
<p><b>Total Expenses:</b> {money(expenses)}</p>
<p><b>Net Profit:</b> {money(profit)}</p>
<p><b>Inventory Units:</b> {inventory_units}</p>
<p><b>Employees:</b> {employee_count}</p>
<p><b>Sales Transactions:</b> {total_sales}</p>
<p><b>Market Share:</b> {market_share:.2f}%</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # COMPETITOR RANKING

    st.subheader("🏆 Competitive Position")

    if rankings:

        rankings_df = pd.DataFrame(rankings)

        st.dataframe(
            rankings_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Competitor ranking information is not available."
        )

    st.markdown("---")

    # PROFIT STATUS

    st.subheader("💹 Financial Performance Assessment")

    if profit > 0:

        st.success(
            f"Your business is profitable. "
            f"Current calculated profit: {money(profit)}."
        )

    elif profit == 0:

        st.info(
            "Your business is currently at the break-even point."
        )

    else:

        st.error(
            f"Your business is operating at a loss of "
            f"{money(abs(profit))}."
        )

    st.markdown("---")

    # DOWNLOAD REPORT

    st.subheader("📥 Download Your Business Report")

    report_text = make_business_report(business)

    st.download_button(
        label="📄 DOWNLOAD FINAL BUSINESS REPORT",
        data=report_text,
        file_name="Business_Tycoon_Final_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )


# =========================================================
# APPLICATION FOOTER
# =========================================================

st.markdown(
    """
<br><br>
<div style="text-align:center;padding:22px;border-top:1px solid rgba(155,107,255,.25);color:#9da6c9;">
<h3 style="color:#c7a8ff;letter-spacing:2px;">🏢 BUSINESS TYCOON SIMULATOR</h3>
<p>Think Like an Entrepreneur. Build Like a Leader.</p>
<p style="font-size:12px;">Premium Gaming Experience | Business Strategy | Financial Intelligence</p>
</div>
    """,
    unsafe_allow_html=True,
)
