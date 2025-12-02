#!/usr/bin/env python3
"""
Sales Team Responsibility Planner
A comprehensive tool for managing sales team responsibilities across multiple products
with quarterly priority planning and overlap detection.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass, asdict
from enum import Enum
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Quarter(Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"

@dataclass
class Product:
    id: str
    name: str
    category: str
    revenue_target: float
    market_size: float
    growth_potential: float

@dataclass
class SalesPerson:
    id: str
    name: str
    department: str
    experience_years: int
    max_products: int
    specializations: List[str]

@dataclass
class Responsibility:
    sales_person_id: str
    product_id: str
    quarter: Quarter
    priority: Priority
    time_allocation_percent: float
    revenue_target: float
    notes: str = ""

class SalesTeamPlanner:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.sales_people: Dict[str, SalesPerson] = {}
        self.responsibilities: List[Responsibility] = []
        
    def add_product(self, product: Product):
        """Add a product to the planner"""
        self.products[product.id] = product
        
    def add_sales_person(self, sales_person: SalesPerson):
        """Add a sales person to the planner"""
        self.sales_people[sales_person.id] = sales_person
        
    def assign_responsibility(self, responsibility: Responsibility):
        """Assign a responsibility to a sales person for a product in a quarter"""
        self.responsibilities.append(responsibility)
        
    def get_overlaps(self) -> Dict[str, List[Dict]]:
        """Detect overlapping responsibilities"""
        overlaps = defaultdict(list)
        
        for i, resp1 in enumerate(self.responsibilities):
            for j, resp2 in enumerate(self.responsibilities[i+1:], i+1):
                if (resp1.sales_person_id == resp2.sales_person_id and 
                    resp1.quarter == resp2.quarter):
                    
                    overlap_info = {
                        'sales_person': self.sales_people[resp1.sales_person_id].name,
                        'quarter': resp1.quarter.value,
                        'product1': self.products[resp1.product_id].name,
                        'product2': self.products[resp2.product_id].name,
                        'priority1': resp1.priority.value,
                        'priority2': resp2.priority.value,
                        'allocation1': resp1.time_allocation_percent,
                        'allocation2': resp2.time_allocation_percent,
                        'total_allocation': resp1.time_allocation_percent + resp2.time_allocation_percent
                    }
                    overlaps[f"{resp1.sales_person_id}_{resp1.quarter.value}"].append(overlap_info)
        
        return dict(overlaps)
    
    def get_workload_summary(self) -> pd.DataFrame:
        """Get workload summary for each sales person by quarter"""
        data = []
        for resp in self.responsibilities:
            sales_person = self.sales_people[resp.sales_person_id]
            product = self.products[resp.product_id]
            
            data.append({
                'Sales Person': sales_person.name,
                'Department': sales_person.department,
                'Quarter': resp.quarter.value,
                'Product': product.name,
                'Priority': resp.priority.value,
                'Time Allocation %': resp.time_allocation_percent,
                'Revenue Target': resp.revenue_target,
                'Product Category': product.category
            })
        
        return pd.DataFrame(data)
    
    def get_product_coverage(self) -> pd.DataFrame:
        """Get product coverage analysis"""
        data = []
        for product_id, product in self.products.items():
            product_responsibilities = [r for r in self.responsibilities if r.product_id == product_id]
            
            if product_responsibilities:
                total_allocation = sum(r.time_allocation_percent for r in product_responsibilities)
                priority_values = [Priority.HIGH.value, Priority.MEDIUM.value, Priority.LOW.value]
                avg_priority = np.mean([priority_values.index(r.priority.value) + 1 
                                     for r in product_responsibilities])
                priority_score = {1: "High", 2: "Medium", 3: "Low"}[int(round(avg_priority))]
                
                data.append({
                    'Product': product.name,
                    'Category': product.category,
                    'Total Allocation %': total_allocation,
                    'Avg Priority': priority_score,
                    'Sales People Count': len(set(r.sales_person_id for r in product_responsibilities)),
                    'Revenue Target': product.revenue_target,
                    'Market Size': product.market_size
                })
            else:
                data.append({
                    'Product': product.name,
                    'Category': product.category,
                    'Total Allocation %': 0,
                    'Avg Priority': "Unassigned",
                    'Sales People Count': 0,
                    'Revenue Target': product.revenue_target,
                    'Market Size': product.market_size
                })
        
        return pd.DataFrame(data)
    
    def create_matrix_view(self) -> pd.DataFrame:
        """Create a matrix view of sales people vs products"""
        sales_people = list(self.sales_people.keys())
        products = list(self.products.keys())
        
        matrix = pd.DataFrame(index=sales_people, columns=products, dtype=object)
        
        for resp in self.responsibilities:
            sales_person_name = self.sales_people[resp.sales_person_id].name
            product_name = self.products[resp.product_id].name
            
            if pd.isna(matrix.loc[resp.sales_person_id, resp.product_id]):
                matrix.loc[resp.sales_person_id, resp.product_id] = []
            
            if isinstance(matrix.loc[resp.sales_person_id, resp.product_id], list):
                matrix.loc[resp.sales_person_id, resp.product_id].append({
                    'quarter': resp.quarter.value,
                    'priority': resp.priority.value,
                    'allocation': resp.time_allocation_percent
                })
        
        # Replace list indices with names for display
        matrix.index = [self.sales_people[sp_id].name for sp_id in sales_people]
        matrix.columns = [self.products[p_id].name for p_id in products]
        
        return matrix
    
    def plot_workload_heatmap(self, quarter: Optional[Quarter] = None):
        """Create a heatmap of sales person workload by product"""
        plt.figure(figsize=(12, 8))
        
        if quarter:
            filtered_resp = [r for r in self.responsibilities if r.quarter == quarter]
        else:
            filtered_resp = self.responsibilities
        
        # Create matrix for heatmap
        sales_people = list(self.sales_people.keys())
        products = list(self.products.keys())
        
        matrix = np.zeros((len(sales_people), len(products)))
        
        for resp in filtered_resp:
            sp_idx = sales_people.index(resp.sales_person_id)
            p_idx = products.index(resp.product_id)
            matrix[sp_idx, p_idx] = resp.time_allocation_percent
        
        # Create heatmap
        sns.heatmap(matrix, 
                   xticklabels=[self.products[p_id].name for p_id in products],
                   yticklabels=[self.sales_people[sp_id].name for sp_id in sales_people],
                   annot=True, 
                   fmt='.1f',
                   cmap='YlOrRd')
        
        quarter_title = f" - {quarter.value}" if quarter else ""
        plt.title(f'Sales Team Workload Heatmap{quarter_title}')
        plt.xlabel('Products')
        plt.ylabel('Sales People')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    
    def export_to_excel(self, filename: str):
        """Export all data to Excel with multiple sheets"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Workload summary
            self.get_workload_summary().to_excel(writer, sheet_name='Workload Summary', index=False)
            
            # Product coverage
            self.get_product_coverage().to_excel(writer, sheet_name='Product Coverage', index=False)
            
            # Matrix view
            matrix = self.create_matrix_view()
            matrix.to_excel(writer, sheet_name='Matrix View')
            
            # Overlaps
            overlaps = self.get_overlaps()
            if overlaps:
                overlap_data = []
                for overlap_group in overlaps.values():
                    overlap_data.extend(overlap_group)
                pd.DataFrame(overlap_data).to_excel(writer, sheet_name='Overlaps', index=False)
    
    def suggest_optimizations(self) -> List[str]:
        """Suggest optimizations based on current assignments"""
        suggestions = []
        
        # Check for overloaded sales people
        workload_by_person = defaultdict(float)
        for resp in self.responsibilities:
            workload_by_person[resp.sales_person_id] += resp.time_allocation_percent
        
        for sp_id, total_workload in workload_by_person.items():
            sales_person = self.sales_people[sp_id]
            if total_workload > 100:
                suggestions.append(f"WARNING: {sales_person.name} is overloaded at {total_workload:.1f}% capacity")
            elif total_workload > 80:
                suggestions.append(f"WARNING: {sales_person.name} is near capacity at {total_workload:.1f}%")
        
        # Check for unassigned products
        assigned_products = set(resp.product_id for resp in self.responsibilities)
        unassigned = set(self.products.keys()) - assigned_products
        if unassigned:
            suggestions.append(f"INFO: Unassigned products: {', '.join([self.products[p_id].name for p_id in unassigned])}")
        
        # Check for single-person products
        product_assignments = defaultdict(list)
        for resp in self.responsibilities:
            product_assignments[resp.product_id].append(resp.sales_person_id)
        
        for p_id, assignees in product_assignments.items():
            if len(set(assignees)) == 1:
                product = self.products[p_id]
                suggestions.append(f"INFO: {product.name} has only one sales person assigned")
        
        return suggestions

def create_sample_data():
    """Create sample data for demonstration"""
    planner = SalesTeamPlanner()
    
    # Add sample products
    products = [
        Product("prod1", "Enterprise CRM", "Software", 500000, 2000000, 0.8),
        Product("prod2", "Mobile Analytics", "Analytics", 300000, 1500000, 0.9),
        Product("prod3", "Cloud Storage", "Infrastructure", 400000, 3000000, 0.7),
        Product("prod4", "AI Chatbot", "AI/ML", 250000, 1000000, 0.95),
        Product("prod5", "Data Visualization", "Analytics", 200000, 800000, 0.6)
    ]
    
    for product in products:
        planner.add_product(product)
    
    # Add sample sales people
    sales_people = [
        SalesPerson("sp1", "Alice Johnson", "Enterprise", 5, 3, ["Software", "Enterprise"]),
        SalesPerson("sp2", "Bob Smith", "SMB", 3, 4, ["Analytics", "Mobile"]),
        SalesPerson("sp3", "Carol Davis", "Enterprise", 7, 2, ["Infrastructure", "Cloud"]),
        SalesPerson("sp4", "David Wilson", "SMB", 2, 5, ["AI/ML", "Analytics"]),
        SalesPerson("sp5", "Eva Brown", "Enterprise", 4, 3, ["Software", "AI/ML"])
    ]
    
    for sp in sales_people:
        planner.add_sales_person(sp)
    
    # Add sample responsibilities
    responsibilities = [
        # Q1 assignments
        Responsibility("sp1", "prod1", Quarter.Q1, Priority.HIGH, 60, 300000),
        Responsibility("sp1", "prod2", Quarter.Q1, Priority.MEDIUM, 40, 120000),
        Responsibility("sp2", "prod2", Quarter.Q1, Priority.HIGH, 50, 150000),
        Responsibility("sp2", "prod4", Quarter.Q1, Priority.MEDIUM, 30, 75000),
        Responsibility("sp3", "prod3", Quarter.Q1, Priority.HIGH, 70, 280000),
        Responsibility("sp4", "prod4", Quarter.Q1, Priority.HIGH, 40, 100000),
        Responsibility("sp4", "prod5", Quarter.Q1, Priority.LOW, 20, 40000),
        Responsibility("sp5", "prod1", Quarter.Q1, Priority.MEDIUM, 30, 150000),
        
        # Q2 assignments
        Responsibility("sp1", "prod1", Quarter.Q2, Priority.HIGH, 50, 250000),
        Responsibility("sp1", "prod3", Quarter.Q2, Priority.MEDIUM, 30, 120000),
        Responsibility("sp2", "prod2", Quarter.Q2, Priority.HIGH, 60, 180000),
        Responsibility("sp2", "prod5", Quarter.Q2, Priority.MEDIUM, 25, 50000),
        Responsibility("sp3", "prod3", Quarter.Q2, Priority.HIGH, 60, 240000),
        Responsibility("sp3", "prod4", Quarter.Q2, Priority.LOW, 20, 50000),
        Responsibility("sp4", "prod4", Quarter.Q2, Priority.HIGH, 50, 125000),
        Responsibility("sp5", "prod1", Quarter.Q2, Priority.MEDIUM, 40, 200000),
        Responsibility("sp5", "prod2", Quarter.Q2, Priority.LOW, 20, 60000),
    ]
    
    for resp in responsibilities:
        planner.assign_responsibility(resp)
    
    return planner

if __name__ == "__main__":
    # Create sample data and demonstrate the planner
    planner = create_sample_data()
    
    print("=== Sales Team Responsibility Planner ===\n")
    
    # Show workload summary
    print("1. Workload Summary:")
    print(planner.get_workload_summary().to_string(index=False))
    print("\n" + "="*80 + "\n")
    
    # Show product coverage
    print("2. Product Coverage Analysis:")
    print(planner.get_product_coverage().to_string(index=False))
    print("\n" + "="*80 + "\n")
    
    # Show overlaps
    print("3. Overlap Detection:")
    overlaps = planner.get_overlaps()
    if overlaps:
        for overlap_group in overlaps.values():
            for overlap in overlap_group:
                print(f"WARNING: {overlap['sales_person']} has overlapping responsibilities in {overlap['quarter']}:")
                print(f"   - {overlap['product1']} ({overlap['priority1']}, {overlap['allocation1']}%)")
                print(f"   - {overlap['product2']} ({overlap['priority2']}, {overlap['allocation2']}%)")
                print(f"   Total allocation: {overlap['total_allocation']}%")
                print()
    else:
        print("No overlaps detected.")
    print("="*80 + "\n")
    
    # Show optimization suggestions
    print("4. Optimization Suggestions:")
    suggestions = planner.suggest_optimizations()
    for suggestion in suggestions:
        print(suggestion)
    print("\n" + "="*80 + "\n")
    
    # Show matrix view
    print("5. Matrix View (Sales People vs Products):")
    matrix = planner.create_matrix_view()
    print(matrix.to_string())
    
    # Export to Excel
    planner.export_to_excel("sales_team_plan.xlsx")
    print(f"\nData exported to 'sales_team_plan.xlsx'")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    planner.plot_workload_heatmap()
    planner.plot_workload_heatmap(Quarter.Q1)
