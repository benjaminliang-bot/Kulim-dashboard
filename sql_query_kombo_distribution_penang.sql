-- SQL Query to analyze Kombo Jimat order distribution across last 4 days of each month for Penang
-- Modified from user's provided query structure

with dis as (
	select
		fd.*,
		m.chain_id,
		m.is_bd_account
	from
		ocd_adw.f_food_discount fd
	inner join ocd_adw.d_merchant m on
		fd.merchant_id = m.merchant_id_nk
	where
		booking_state_simple = 'COMPLETED'
		and m.business_type = 0
),
-- MFC discount
mfc as (
	select
		*
	from
		ocd_adw.d_merchant_funded_campaign mfc
	where
		country_code = 'MY'
		and author_type = 'Operations'
		and merchant_campaign_name in ('Buy 1 Get 1 Free', 'Buy 1 Free 1', '50% Off 2nd meal', '50% Off 2nd item')
),
tc as (
	select
		*
	from
		temptables.my_cities
),
d as (
	select
		*,
		EXTRACT(DAY FROM DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d')) as day_of_month,
		EXTRACT(DAY FROM (DATE_ADD('day', -1, DATE_ADD('month', 1, DATE_TRUNC('month', DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d')))))) as last_day_of_month
	from
		ocd_adw.d_date
	where
		year >= 2024
		and year <= 2025
		-- Filter for last 4 days of each month
		and EXTRACT(DAY FROM DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d')) > (
			EXTRACT(DAY FROM (DATE_ADD('day', -1, DATE_ADD('month', 1, DATE_TRUNC('month', DATE_PARSE(CAST(date_id AS VARCHAR), '%Y%m%d')))))) - 4
		)
)
select 
	DATE_FORMAT(DATE_PARSE(CAST(dis.date_id AS VARCHAR), '%Y%m%d'), '%Y-%m-01') as month,
	EXTRACT(DAY FROM DATE_PARSE(CAST(dis.date_id AS VARCHAR), '%Y%m%d')) as day_of_month,
	(d.last_day_of_month - EXTRACT(DAY FROM DATE_PARSE(CAST(dis.date_id AS VARCHAR), '%Y%m%d')) + 1) as day_position,
	COUNT(distinct dis.order_id) as kombo_jimat_orders,
	SUM(fm.gross_merchandise_value) as kombo_jimat_gmv_myr
from
	dis
inner join ocd_adw.f_food_metrics fm on
	dis.order_id = fm.order_id
inner join mfc on
	dis.mfc_campaign_id = mfc.campaign_id
inner join tc on
	dis.city_id = tc.id
inner join ocd_adw.d_area a on
	fm.area_id = a.area_id
inner join d on
	dis.date_id = d.date_id
where
	fm.booking_state_simple = 'COMPLETED'
	and tc.name = 'Penang'  -- Filter for Penang
group by
	DATE_FORMAT(DATE_PARSE(CAST(dis.date_id AS VARCHAR), '%Y%m%d'), '%Y-%m-01'),
	EXTRACT(DAY FROM DATE_PARSE(CAST(dis.date_id AS VARCHAR), '%Y%m%d')),
	d.last_day_of_month
order by
	month DESC,
	day_of_month DESC

