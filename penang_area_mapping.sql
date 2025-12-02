-- Penang Island vs Mainland Area Mapping
-- Based on user's QGIS classification

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Kepala Batas', 'Prai', 'Tasek Gelugor', 'Bandar Cassia',
            'Bukit Mertajam', 'Penaga', 'Kubang Semang', 'Simpang Ampat',
            'Bukit Tengah', 'Kws Perusahaan Bebas Perai', 'Batu Kawan Industrial Park',
            'Sungai Bakap', 'Padang Serai', 'Bandar Tasek Mutiara', 'Parit Buntar',
            'Bukit Minyak', 'Permatang Pauh', 'Seberang Jaya', 'Kulim',
            'Sungai Jawi', 'Taman Widuri', 'Bagan Serai', 'Telok Air Tawar',
            'Nibong Tebal', 'Alma Jaya', 'Beringin', 'Kuala Kurau',
            'Karangan', 'Gurun_Sala Besar', 'Butterworth'
        )
),
island_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Bayan Lepas', 'Gelugor', 'Air Itam', 'Jelutong',
            'Georgetown', 'Tanjung Bungah', 'Desa Ria', 'Bayan Baru',
            'Sungai Dua', 'Teluk Kumbar', 'Batu Feringgi', 'Balik Pulau',
            'Gurney', 'Teluk Bahang', 'Gertak Sanggul'
        )
)

