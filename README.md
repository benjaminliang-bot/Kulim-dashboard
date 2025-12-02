# Sales Team Responsibility Planner

A comprehensive tool for managing sales team responsibilities across multiple products with quarterly priority planning and overlap detection.

## Features

### 🎯 Core Functionality
- **Matrix View**: Visual representation of sales people vs products
- **Quarterly Planning**: Plan responsibilities by quarter with priority levels
- **Overlap Detection**: Automatically identify conflicting assignments
- **Workload Analysis**: Track capacity and allocation percentages
- **Product Coverage**: Analyze which products are covered and by whom

### 📊 Analytics & Reporting
- **Workload Heatmaps**: Visual representation of team workload distribution
- **Excel Export**: Multi-sheet export with all data and analysis
- **Optimization Suggestions**: AI-powered recommendations for better resource allocation
- **Priority Management**: Track and balance high/medium/low priority assignments

### 🔧 Key Components

1. **Product Management**
   - Product details (name, category, revenue targets, market size)
   - Growth potential tracking
   - Revenue target management

2. **Sales Team Management**
   - Sales person profiles with experience and specializations
   - Capacity limits (max products per person)
   - Department-based organization

3. **Responsibility Assignment**
   - Quarterly assignment planning
   - Priority levels (High/Medium/Low)
   - Time allocation percentages
   - Revenue target distribution

4. **Conflict Resolution**
   - Overlap detection across quarters
   - Workload balancing recommendations
   - Capacity constraint warnings

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Setup

```python
from sales_team_planner import SalesTeamPlanner, Product, SalesPerson, Responsibility, Priority, Quarter

# Initialize planner
planner = SalesTeamPlanner()

# Add products
product = Product(
    id="prod1",
    name="Enterprise CRM",
    category="Software",
    revenue_target=500000,
    market_size=2000000,
    growth_potential=0.8
)
planner.add_product(product)

# Add sales people
sales_person = SalesPerson(
    id="sp1",
    name="Alice Johnson",
    department="Enterprise",
    experience_years=5,
    max_products=3,
    specializations=["Software", "Enterprise"]
)
planner.add_sales_person(sales_person)

# Assign responsibilities
responsibility = Responsibility(
    sales_person_id="sp1",
    product_id="prod1",
    quarter=Quarter.Q1,
    priority=Priority.HIGH,
    time_allocation_percent=60,
    revenue_target=300000
)
planner.assign_responsibility(responsibility)
```

### Key Methods

#### 1. Matrix View
```python
matrix = planner.create_matrix_view()
print(matrix)
```

#### 2. Overlap Detection
```python
overlaps = planner.get_overlaps()
for overlap_group in overlaps.values():
    for overlap in overlap_group:
        print(f"Conflict: {overlap['sales_person']} - {overlap['product1']} vs {overlap['product2']}")
```

#### 3. Workload Analysis
```python
workload_df = planner.get_workload_summary()
print(workload_df)
```

#### 4. Product Coverage
```python
coverage_df = planner.get_product_coverage()
print(coverage_df)
```

#### 5. Visualizations
```python
# Overall workload heatmap
planner.plot_workload_heatmap()

# Quarterly workload heatmap
planner.plot_workload_heatmap(Quarter.Q1)
```

#### 6. Export Data
```python
planner.export_to_excel("sales_plan.xlsx")
```

#### 7. Optimization Suggestions
```python
suggestions = planner.suggest_optimizations()
for suggestion in suggestions:
    print(suggestion)
```

## Sample Data

The tool includes sample data with:
- 5 products across different categories
- 5 sales people with varying experience levels
- Quarterly assignments with different priorities
- Realistic workload distributions

Run the script directly to see the sample data in action:

```bash
python sales_team_planner.py
```

## Output Files

- **Excel Export**: Multi-sheet workbook with:
  - Workload Summary
  - Product Coverage Analysis
  - Matrix View
  - Overlap Detection
- **Visualizations**: Interactive heatmaps showing workload distribution

## Use Cases

### 1. Quarterly Planning
- Plan sales team assignments for each quarter
- Balance workload across team members
- Ensure all products have adequate coverage

### 2. Resource Optimization
- Identify overloaded team members
- Find underutilized resources
- Optimize product-sales person matches

### 3. Conflict Resolution
- Detect overlapping responsibilities
- Resolve capacity conflicts
- Balance priorities across products

### 4. Performance Tracking
- Monitor revenue targets by person and product
- Track time allocation efficiency
- Analyze quarterly performance trends

## Customization

The tool is designed to be easily customizable:

- Add new product categories
- Modify priority levels
- Adjust capacity constraints
- Add custom metrics and KPIs
- Integrate with existing CRM systems

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical operations
- matplotlib: Basic plotting
- seaborn: Statistical data visualization
- openpyxl: Excel file handling
