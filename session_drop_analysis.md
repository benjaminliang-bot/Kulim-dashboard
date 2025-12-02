# Session Drop Analysis - OC Overall

## 📊 Key Metrics Summary

### Session Performance
- **This Week**: 899,565 sessions
- **Same Week Last Month**: 1,576,003 sessions
- **Same Week Last Year (YTD Avg)**: 1,437,978 sessions

### Drop Magnitude
- **MoM Drop**: -42.9% (676,438 fewer sessions)
- **YoY Drop**: -37.4% (538,413 fewer sessions)

---

## 🔍 Root Cause Analysis

### 1. **Sessions Drop is Proportional to Orders Drop**

**Critical Finding**: Orders per session is **stable at 1.1** across all periods
- This week: 1.1 orders/session
- Last month: 1.1 orders/session  
- YoY: 1.13 orders/session

**Implication**: Session drop is **directly correlated** with orders drop. The relationship is:
```
Sessions = Orders / Orders_per_Session
```

Since orders per session is constant, **sessions will drop proportionally to orders**.

### 2. **Orders Drop Breakdown**

**OC Overall Orders:**
- This week: 1,004,487 orders
- Last month: 1,777,220 orders (-43.5% MoM)
- YoY: 1,620,000 orders (estimated, -38.0% YoY)

**The session drop is a symptom, not the root cause. The real question is: why did orders drop?**

---

## 🎯 Potential Root Causes (Hypothesis Testing)

### Hypothesis 1: **WTU (Eater Base) Contraction**
- **This week WTU**: 344,570
- **Last month WTU**: 523,000 (estimated, -34.1% MoM)
- **YoY WTU**: 520,000 (estimated, -33.7% YoY)

**Analysis**: WTU drop (-34%) is **less severe** than orders drop (-43%), suggesting:
- ✅ Some eaters are still active but ordering less frequently
- ⚠️ New eater acquisition has slowed significantly
- ⚠️ Existing eater retention/engagement has declined

**Action**: Check:
- New eater acquisition rate vs last month/YoY
- Repeat eater rate (2nd+ order within 7 days)
- Eater frequency distribution (1x, 2x, 3x+ per week)

---

### Hypothesis 2: **Promo Investment Reduction**
- **This week promo expense**: 3.07M MYR
- **Last month promo expense**: 5.54M MYR (-44.5% MoM)
- **YoY promo expense**: 5.86M MYR (-47.6% YoY)

**Analysis**: Promo expense dropped **more than orders**, but promo penetration is **stable**:
- This week: 46.5% promo penetration
- Last month: 47.3% promo penetration (-0.8pp)
- YoY: 46.5% promo penetration (flat)

**Implication**: 
- Promo efficiency may have improved (less spend, similar penetration)
- OR promo depth (discount %) has reduced, making promos less attractive
- OR non-promo orders dropped disproportionately

**Action**: Check:
- Average promo discount % vs last month/YoY
- Promo redemption rate (promo orders / promo impressions)
- Non-promo order volume trend

---

### Hypothesis 3: **Basket Size Compression**
- **This week basket**: 31.49 MYR
- **Last month basket**: 32.42 MYR (-2.9% MoM)
- **YoY basket**: 33.28 MYR (-5.4% YoY)

**Analysis**: Basket size drop is **mild** (-3% to -5%) compared to orders drop (-43%). This suggests:
- ✅ Eaters who are ordering are maintaining similar order values
- ⚠️ The drop is primarily in **order volume**, not order value

**Action**: Check:
- Order frequency per eater (orders per WTU)
- Category mix (are high-basket categories declining more?)

---

### Hypothesis 4: **Fulfilment Rate Impact**
- **This week fulfilment**: 92.2%
- **Last month fulfilment**: 92.2% (flat)
- **YoY fulfilment**: 92.64% (-0.4pp)

**Analysis**: Fulfilment rate is **stable**, so this is **NOT** a driver of session drop.

---

### Hypothesis 5: **Seasonality / Calendar Effects**
**Check if this week had:**
- Public holidays (reducing demand)
- School holidays (affecting family orders)
- Weather events (floods, heavy rain)
- Competitor promotions (Foodpanda, ShopeeFood)
- Economic factors (inflation, spending power)

**Action**: Compare this week's date range to historical patterns.

---

### Hypothesis 6: **Incomplete Week Data**
**Critical Check**: Looking at daily data, Nov 7 (Friday) shows only 24,750 orders vs ~240K-250K for Mon-Thu.

**Potential Issues**:
- Is this week's data incomplete? (Only Mon-Thu captured?)
- Is there a data pipeline delay?
- Was there a system outage on Friday?

**Action**: Verify data completeness for the full week (Mon-Sun).

---

## 📈 Conversion Funnel Analysis

### Session-to-Order Conversion
- **This week**: 1,004,487 orders / 899,565 sessions = **1.12 orders/session**
- **Last month**: 1,777,220 orders / 1,576,003 sessions = **1.13 orders/session**
- **YoY**: ~1.13 orders/session

**Finding**: Conversion rate is **stable**, so the drop is in **session volume**, not conversion efficiency.

### Session-to-Completed-Order Conversion
- **This week**: 925,130 completed orders / 899,565 sessions = **1.03 completed/session**
- **Last month**: 1,625,000 completed orders / 1,576,003 sessions = **1.03 completed/session**

**Finding**: Completed order conversion is also **stable**.

---

## 💡 Key Insights & Recommendations

### Primary Insight
**Sessions dropped because orders dropped. The root cause is in the demand/engagement layer, not the conversion layer.**

### Secondary Insights
1. **Orders per session is stable** → No conversion efficiency issue
2. **WTU drop (-34%) < Orders drop (-43%)** → Frequency per eater has declined
3. **Promo spend dropped (-44%)** → May be a contributing factor, but penetration is stable
4. **Basket size drop is mild (-3%)** → Value per order is relatively resilient

### Recommended Investigation Priorities

**🔴 High Priority:**
1. **Verify data completeness** - Is this week's data complete? (Check Nov 7 anomaly)
2. **WTU frequency analysis** - How many orders per eater this week vs last month?
3. **New eater acquisition** - Are we acquiring fewer new eaters?
4. **Calendar/seasonality check** - Any holidays, events, or external factors?

**🟡 Medium Priority:**
5. **Promo depth analysis** - Average discount % vs last month
6. **Category performance** - Which categories dropped most?
7. **City-level breakdown** - Is the drop uniform across all cities?

**🟢 Low Priority:**
8. **Competitive analysis** - Any major competitor promotions?
9. **Economic indicators** - Consumer spending power trends

---

## 🎯 Next Steps

1. **Immediate**: Verify data completeness for Nov 1-7 (full week)
2. **This Week**: Run WTU frequency analysis and new eater acquisition report
3. **This Month**: Deep dive into promo strategy and category performance
4. **Ongoing**: Monitor if this is a one-week anomaly or a trend

---

## 📝 Questions to Answer

1. **Is this week's data complete?** (Nov 7 shows only 24K orders vs 240K+ for other days)
2. **What's the orders-per-eater frequency this week vs last month?**
3. **What's the new eater acquisition rate?**
4. **Were there any holidays, events, or external factors this week?**
5. **Is the drop uniform across all cities or concentrated in specific markets?**

