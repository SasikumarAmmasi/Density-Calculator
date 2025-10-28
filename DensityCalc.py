import streamlit as st
import math

# ====================================================================
# 1. UNIT CONVERTER CLASS - Required for pressure/temperature conversion steps
# (Copied from the previous successful Streamlit code)
# ====================================================================
class UnitConverter:
    def convert_pressure(self, value, from_unit, to_unit):
        # 1. Convert to base unit (kPa)
        if from_unit == 'barg':
            base_value = value * 100 + 101.325
        elif from_unit == 'kg/cm2':
            base_value = value * 98.0665
        elif from_unit == 'pasig':
            base_value = value * 0.00689476
        elif from_unit == 'kPa':
            base_value = value
        elif from_unit == 'pascal':
            base_value = value / 1000
        elif from_unit == 'mmH2O':
            base_value = value * 0.00980638
        else:
            raise ValueError(f"Unknown pressure unit: {from_unit}")

        # 2. Convert from base unit (kPa) to target unit
        if to_unit == 'barg':
            return (base_value - 101.325) / 100
        elif to_unit == 'kg/cm2':
            return base_value / 98.0665
        elif to_unit == 'pasig':
            return base_value / 0.00689476
        elif to_unit == 'kPa':
            return base_value
        elif to_unit == 'pascal':
            return base_value * 1000
        elif to_unit == 'mmH2O':
            return base_value / 0.00980638
        else:
            raise ValueError(f"Unknown pressure unit: {to_unit}")

    def convert_temperature(self, value, from_unit, to_unit):
        # 1. Convert to base unit (Kelvin)
        if from_unit == 'C':
            base_value = value + 273.15
        elif from_unit == 'F':
            base_value = (value - 32) * (5/9) + 273.15
        elif from_unit == 'K':
            base_value = value
        elif from_unit == 'R':
            base_value = value * (5/9)
        else:
            raise ValueError(f"Unknown temperature unit: {from_unit}")

        # 2. Convert from base unit (Kelvin) to target unit
        if to_unit == 'C':
            return base_value - 273.15
        elif to_unit == 'F':
            return (base_value - 273.15) * (9/5) + 32
        elif to_unit == 'K':
            return base_value
        elif to_unit == 'R':
            return base_value * (9/5)
        else:
            raise ValueError(f"Unknown temperature unit: {to_unit}")

    # Density conversion is not needed here, but keeping structure for completeness
    def convert_density(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
        raise ValueError("Density conversion not implemented for this context.")

# ====================================================================

converter = UnitConverter() # Instantiate the converter

# Universal gas constant in J/(mol·K)
UNIVERSAL_GAS_CONSTANT = 8.314

def density_calculation_app():
    st.title("Ideal Gas Density Calculator 💨")
    st.markdown("---")
    st.header("Input Parameters")

    # --- Input Widgets for Pressure and Temperature ---
    pressure_units = ['barg', 'kg/cm2', 'pasig', 'kPa', 'pascal', 'mmH2O']
    temp_units = ['C', 'F', 'K', 'R']

    col_p_value, col_p_unit = st.columns(2)
    with col_p_value:
        pressure_value = st.number_input("Pressure Value:", value=100.0, format="%f", key="calc_p_value")
    with col_p_unit:
        pressure_unit = st.selectbox("Pressure Unit:", options=pressure_units, index=3, key="calc_p_unit")

    col_t_value, col_t_unit = st.columns(2)
    with col_t_value:
        temperature_value = st.number_input("Temperature Value:", value=298.15, format="%f", key="calc_t_value")
    with col_t_unit:
        temperature_unit = st.selectbox("Temperature Unit:", options=temp_units, index=2, key="calc_t_unit") # Default K

    # --- Input Widgets for Molecular Weight and Z-Factor ---
    col_mw, col_z = st.columns(2)
    with col_mw:
        molecular_weight = st.number_input("Molecular Weight (g/mol):", value=28.01, format="%f", key="calc_mw")
    with col_z:
        compressibility_factor = st.number_input("Compressibility Factor (Z):", value=1.0, format="%f", key="calc_z", min_value=0.0)

    st.markdown("---")

    # --- Calculation Button ---
    if st.button('Calculate Density', key="calc_density_btn"):
        try:
            # Check for zero inputs that cause division by zero
            if compressibility_factor <= 0 or temperature_value <= 0:
                st.error("Error: Compressibility Factor (Z) and Temperature must be greater than zero.")
                return

            # 1. Convert pressure to kPa (as required by the original logic for the next step)
            pressure_kpa = converter.convert_pressure(
                pressure_value,
                pressure_unit,
                'kPa'
            )

            # 2. Convert temperature to Kelvin (K)
            temperature_k = converter.convert_temperature(
                temperature_value,
                temperature_unit,
                'K'
            )

            # Convert kPa to Pa (1 kPa = 1000 Pa) for use in the ideal gas density formula:
            # Density (kg/m³) = (P * MW) / (Z * R * T)
            # P is in Pa (N/m²), MW is in kg/mol (convert g/mol to kg/mol), R is in J/(mol·K), T is in K
            pressure_pa = pressure_kpa * 1000
            molecular_weight_kg_mol = molecular_weight / 1000 # Convert g/mol to kg/mol

            # Calculate density (in kg/m³)
            density = (
                pressure_pa * molecular_weight_kg_mol
            ) / (
                compressibility_factor * UNIVERSAL_GAS_CONSTANT * temperature_k
            )

            # --- Display Output ---
            st.success(f"**Calculated Density:** **{density:.3f}** kg/m³")
            st.info(f"""
            **Inputs Converted to SI Units:**
            - Pressure (P): {pressure_pa:.2f} Pa
            - Temperature (T): {temperature_k:.2f} K
            - Molecular Weight (MW): {molecular_weight_kg_mol:.4f} kg/mol
            - Gas Constant (R): {UNIVERSAL_GAS_CONSTANT} J/(mol·K)
            """)

        except ValueError as e:
            st.error(f"Error in Unit Conversion: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during calculation: {e}")


if __name__ == "__main__":
    density_calculation_app()
