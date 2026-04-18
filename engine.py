class SupplyNode:
    def __init__(self, node_id, name, node_type, cost_per_unit, lead_time_days, carbon_score, capacity):
        self.node_id = node_id
        self.name = name
        self.node_type = node_type  # e.g., 'Primary', 'Backup', 'Assembly'
        
        # Core PM Metrics
        self.cost_per_unit = cost_per_unit
        self.lead_time_days = lead_time_days
        self.carbon_score = carbon_score  # measured in kg CO2 per unit
        self.capacity = capacity
        
        # The trigger for our simulator
        self.is_active = True 

    def __str__(self):
        status = "🟢 ACTIVE" if self.is_active else "🔴 OFFLINE"
        return f"{status} | {self.name} ({self.node_type}) | Cost: ${self.cost_per_unit} | Lead: {self.lead_time_days}d | Carbon: {self.carbon_score}kg"


def generate_synthetic_network():
    """Generates our baseline supply chain dataset."""
    network = {}

    # 1. Primary Suppliers (Highly optimized: Cheap, fast, low carbon)
    network['Supplier_A'] = SupplyNode(1, "Local Steel Corp", "Primary", cost_per_unit=50, lead_time_days=3, carbon_score=10, capacity=1000)
    network['Supplier_B'] = SupplyNode(2, "Regional Microchips", "Primary", cost_per_unit=120, lead_time_days=5, carbon_score=15, capacity=500)

    # 2. Backup Suppliers (The Trade-off: Expensive, slow, high carbon footprint due to air freight)
    network['Backup_A'] = SupplyNode(3, "Overseas Steel (Air Freight)", "Backup", cost_per_unit=95, lead_time_days=14, carbon_score=65, capacity=2000)

    # 3. The Assembly Plant
    network['Assembly_1'] = SupplyNode(4, "Main Assembly Hub", "Assembly", cost_per_unit=200, lead_time_days=2, carbon_score=40, capacity=1500)

    return network


# --- Run the Simulation Baseline ---
print("--- Baseline Supply Chain Status ---")
my_supply_chain = generate_synthetic_network()

for key, node in my_supply_chain.items():
    print(node)
    # --- STEP 2 & 3: THE DISRUPTION ENGINE ---

def calculate_metrics(network):
    """Calculates total cost, lead time, and carbon for the active path."""
    total_cost = 0
    total_carbon = 0
    
    # Assembly and Microchips are always required in this simple model
    total_cost += network['Assembly_1'].cost_per_unit + network['Supplier_B'].cost_per_unit
    total_carbon += network['Assembly_1'].carbon_score + network['Supplier_B'].carbon_score
    max_lead_time = network['Assembly_1'].lead_time_days + network['Supplier_B'].lead_time_days
    
    # Procedural Logic: Route based on active status
    if network['Supplier_A'].is_active:
        # Use Primary Steel
        total_cost += network['Supplier_A'].cost_per_unit
        total_carbon += network['Supplier_A'].carbon_score
        max_lead_time += network['Supplier_A'].lead_time_days
        steel_source = "Primary (Local Steel)"
    else:
        # Reroute to Backup Steel
        total_cost += network['Backup_A'].cost_per_unit
        total_carbon += network['Backup_A'].carbon_score
        max_lead_time += network['Backup_A'].lead_time_days
        steel_source = "Backup (Overseas Air Freight)"
        
    return {
        "cost": total_cost,
        "time": max_lead_time,
        "carbon": total_carbon,
        "routing": steel_source
    }

def trigger_disruption(network, node_key):
    """Simulates a node going offline."""
    if node_key in network:
        network[node_key].is_active = False
        print(f"\n🚨 SYSTEM ALERT: {network[node_key].name} has gone offline! 🚨")


# --- RUNNING THE SIMULATION ---

# 1. Calculate the baseline (Perfect conditions)
baseline = calculate_metrics(my_supply_chain)
print(f"\n--- 📊 Baseline Metrics (Normal Operations) ---")
print(f"Routing path: {baseline['routing']}")
print(f"Total Cost/Unit:  ${baseline['cost']}")
print(f"Total Lead Time:  {baseline['time']} days")
print(f"Total Carbon:     {baseline['carbon']} kg")

# 2. Trigger a supply chain shock!
trigger_disruption(my_supply_chain, 'Supplier_A')

# 3. Recalculate and find the Delta (The PM Value)
disrupted = calculate_metrics(my_supply_chain)
print(f"\n--- ⚠️ Disrupted Metrics (Emergency Rerouting) ---")
print(f"Routing path: {disrupted['routing']}")
print(f"Total Cost/Unit:  ${disrupted['cost']}   (Penalty: +${disrupted['cost'] - baseline['cost']})")
print(f"Total Lead Time:  {disrupted['time']} days  (Penalty: +{disrupted['time'] - baseline['time']} days)")
print(f"Total Carbon:     {disrupted['carbon']} kg  (Penalty: +{disrupted['carbon'] - baseline['carbon']} kg)")