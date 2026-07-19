def generate_recommendations(
    risk_level: str,
    supplier_risk: float,
    overstock_risk: bool,
    transfer_available: bool,
) -> list[str]:
    recommendations = []

    if risk_level == "Critical":
        recommendations.append("Create an urgent purchase order and expedite supplier delivery.")
    elif risk_level == "High":
        recommendations.append("Place a replenishment order and increase monitoring frequency.")
    elif risk_level == "Medium":
        recommendations.append("Review reorder timing and confirm near-term demand assumptions.")
    else:
        recommendations.append("Maintain the standard replenishment schedule.")

    if supplier_risk >= 0.35:
        recommendations.append("Engage a backup supplier or renegotiate lead-time commitments.")

    if overstock_risk:
        recommendations.append("Reduce future purchase quantities or reallocate stock to higher-demand locations.")

    if transfer_available:
        recommendations.append("Transfer inventory from an overstocked location before creating a new purchase order.")

    return recommendations
