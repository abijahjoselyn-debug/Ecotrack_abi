import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE SETUP
# -------------------------------

st.set_page_config(
    page_title="EcoTrack",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 EcoTrack")
st.subheader("Interactive Carbon Footprint Dashboard")

st.write(
    "Calculate your estimated carbon footprint, "
    "understand where it comes from, and explore ways to reduce it."
)

st.divider()

# -------------------------------
# CARBON EMISSION FACTORS
# Educational project values
# -------------------------------

CARBON_FACTORS = {
    "car": 0.17,
    "bus": 0.08,
    "train": 0.04,
    "electricity": 0.70,
    "vegetarian_meal": 0.70,
    "nonveg_meal": 2.50
}

# -------------------------------
# USER INPUTS
# -------------------------------

st.sidebar.header("📝 Enter Your Activities")

st.sidebar.subheader("🚗 Transport")

car_km = st.sidebar.number_input(
    "Car distance per month (km)",
    min_value=0.0,
    value=100.0,
    step=10.0
)

bus_km = st.sidebar.number_input(
    "Bus distance per month (km)",
    min_value=0.0,
    value=50.0,
    step=10.0
)

train_km = st.sidebar.number_input(
    "Train distance per month (km)",
    min_value=0.0,
    value=20.0,
    step=10.0
)

st.sidebar.subheader("⚡ Electricity")

electricity_kwh = st.sidebar.number_input(
    "Electricity consumption per month (kWh)",
    min_value=0.0,
    value=100.0,
    step=10.0
)

st.sidebar.subheader("🍽️ Food")

vegetarian_meals = st.sidebar.number_input(
    "Vegetarian meals per month",
    min_value=0,
    value=30,
    step=1
)

nonveg_meals = st.sidebar.number_input(
    "Non-vegetarian meals per month",
    min_value=0,
    value=15,
    step=1
)

st.sidebar.subheader("🎯 Reduction Goal")

reduction_goal = st.sidebar.slider(
    "Target reduction (%)",
    min_value=0,
    max_value=50,
    value=10,
    step=5
)

# -------------------------------
# CALCULATIONS
# -------------------------------

car_emission = car_km * CARBON_FACTORS["car"]

bus_emission = bus_km * CARBON_FACTORS["bus"]

train_emission = train_km * CARBON_FACTORS["train"]

electricity_emission = (
    electricity_kwh * CARBON_FACTORS["electricity"]
)

vegetarian_emission = (
    vegetarian_meals *
    CARBON_FACTORS["vegetarian_meal"]
)

nonveg_emission = (
    nonveg_meals *
    CARBON_FACTORS["nonveg_meal"]
)

transport_total = (
    car_emission +
    bus_emission +
    train_emission
)

energy_total = electricity_emission

food_total = (
    vegetarian_emission +
    nonveg_emission
)

total_emission = (
    transport_total +
    energy_total +
    food_total
)

# -------------------------------
# REDUCTION CALCULATION
# -------------------------------

possible_saving = (
    total_emission *
    reduction_goal /
    100
)

target_emission = (
    total_emission -
    possible_saving
)

# -------------------------------
# IMPACT LEVEL
# -------------------------------

if total_emission < 100:
    impact_level = "🌱 Low"

elif total_emission < 250:
    impact_level = "🌿 Moderate"

elif total_emission < 500:
    impact_level = "⚠️ High"

else:
    impact_level = "🔴 Very High"

# -------------------------------
# MAIN DASHBOARD
# -------------------------------

st.header("📊 Your Carbon Footprint")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total CO₂e",
        f"{total_emission:.1f} kg"
    )

with col2:
    st.metric(
        "Transport",
        f"{transport_total:.1f} kg"
    )

with col3:
    st.metric(
        "Energy",
        f"{energy_total:.1f} kg"
    )

with col4:
    st.metric(
        "Food",
        f"{food_total:.1f} kg"
    )

st.divider()

# -------------------------------
# IMPACT
# -------------------------------

st.header("🌱 Your Current Impact")

st.info(
    f"Your estimated monthly carbon footprint is "
    f"**{total_emission:.1f} kg CO₂e**."
)

st.success(
    f"Impact level: **{impact_level}**"
)

# -------------------------------
# DATA FOR CHARTS
# -------------------------------

category_data = pd.DataFrame({
    "Category": [
        "Transport",
        "Electricity",
        "Food"
    ],
    "Emissions": [
        transport_total,
        energy_total,
        food_total
    ]
})

# -------------------------------
# CHARTS
# -------------------------------

st.header("📈 Understand Your Footprint")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.subheader("Carbon by Category")

    fig_bar = px.bar(
        category_data,
        x="Category",
        y="Emissions",
        title="Monthly CO₂e by Category",
        labels={
            "Emissions": "CO₂e (kg)"
        }
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

with chart_col2:

    st.subheader("Contribution Breakdown")

    fig_pie = px.pie(
        category_data,
        names="Category",
        values="Emissions",
        title="Share of Total Carbon Footprint"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# -------------------------------
# DETAILED CALCULATION
# -------------------------------

st.header("🧮 Detailed Calculation")

detail_data = pd.DataFrame({

    "Activity": [
        "Car",
        "Bus",
        "Train",
        "Electricity",
        "Vegetarian meals",
        "Non-vegetarian meals"
    ],

    "Amount": [
        car_km,
        bus_km,
        train_km,
        electricity_kwh,
        vegetarian_meals,
        nonveg_meals
    ],

    "Emission (kg CO₂e)": [
        car_emission,
        bus_emission,
        train_emission,
        electricity_emission,
        vegetarian_emission,
        nonveg_emission
    ]
})

st.dataframe(
    detail_data,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# WHAT-IF SIMULATOR
# -------------------------------

st.divider()

st.header("🔮 What-If Reduction Simulator")

st.write(
    "See what your footprint could look like "
    "if you achieved your selected reduction target."
)

sim_col1, sim_col2, sim_col3 = st.columns(3)

with sim_col1:

    st.metric(
        "Current",
        f"{total_emission:.1f} kg"
    )

with sim_col2:

    st.metric(
        "Possible Saving",
        f"{possible_saving:.1f} kg"
    )

with sim_col3:

    st.metric(
        "After Reduction",
        f"{target_emission:.1f} kg"
    )

comparison_data = pd.DataFrame({

    "Scenario": [
        "Current",
        "After Reduction"
    ],

    "CO₂e": [
        total_emission,
        target_emission
    ]
})

fig_comparison = px.bar(
    comparison_data,
    x="Scenario",
    y="CO₂e",
    title="Current vs Target Footprint",
    labels={
        "CO₂e": "CO₂e (kg)"
    }
)

st.plotly_chart(
    fig_comparison,
    use_container_width=True
)

# -------------------------------
# PERSONALIZED SUGGESTIONS
# -------------------------------

st.header("💡 Suggestions to Reduce Your Footprint")

if (
    transport_total >= energy_total
    and transport_total >= food_total
):

    st.warning(
        "🚗 Transport is your largest category. "
        "Consider walking, cycling, public transport, "
        "carpooling, or reducing unnecessary trips."
    )

elif (
    energy_total >= transport_total
    and energy_total >= food_total
):

    st.warning(
        "⚡ Electricity is your largest category. "
        "Try reducing unnecessary electricity use "
        "and switching off devices when they are not needed."
    )

else:

    st.warning(
        "🍽️ Food is your largest category. "
        "Consider reducing food waste and choosing "
        "lower-impact meals more often."
    )

# -------------------------------
# ECO CHALLENGE
# -------------------------------

st.header("🏆 Eco Challenge")

if reduction_goal >= 30:

    st.success(
        "🏆 Green Champion — "
        "You selected an ambitious reduction target!"
    )

elif reduction_goal >= 15:

    st.success(
        "🌿 Eco Explorer — "
        "You are actively planning to reduce your footprint!"
    )

else:

    st.info(
        "🌱 Eco Starter — "
        "Try increasing your reduction target "
        "as your next challenge."
    )

# -------------------------------
# ABOUT PROJECT
# -------------------------------

with st.expander("ℹ️ About this project"):

    st.write(
        """
        EcoTrack is an educational carbon-footprint
        dashboard created as a school Computer Science project.

        The program demonstrates:

        • Python variables
        • User input
        • Arithmetic calculations
        • Conditional statements
        • Dictionaries
        • Data processing
        • Data visualization
        • Interactive application design
        • Sustainability awareness

        CO₂e means carbon-dioxide equivalent.
        """
    )

# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "EcoTrack 🌍 | Educational Computer Science Project"
)