SET search_path TO raw_data, public;

INSERT INTO products (product_name, category, manufacturer, unit_price)
VALUES
-- Oxygen Supplies
('Oxygen Supplies', 'Medical Equipment', 'MedAir', 1450.00),
('Oxygen Supplies', 'Medical Equipment', 'LifeGas', 1500.00),

-- Masks
('Masks', 'Medical Consumables', 'SafeCare', 10.00),
('Masks', 'Medical Consumables', 'HealthShield', 12.00),

-- Airways
('Airways', 'Respiratory Devices', 'MedTech', 250.00),
('Airways', 'Respiratory Devices', 'RespiraPlus', 270.00),

-- Walkers
('Walkers', 'Mobility Aids', 'HealthMove', 3200.00),
('Walkers', 'Mobility Aids', 'CareStep', 3400.00),

-- Electrosurgical
('Electrosurgical Products', 'Surgical Equipment', 'SurgiTech', 45000.00),
('Electrosurgical Products', 'Surgical Equipment', 'ElectroMed', 47000.00),

-- Ventilators
('Ventilators', 'Critical Care Equipment', 'LifeSupport Systems', 250000.00),
('Ventilators', 'Critical Care Equipment', 'AirCare Medical', 265000.00),

-- Gloves
('Gloves', 'Medical Consumables', 'SafeCare', 5.00),
('Gloves', 'Medical Consumables', 'MediHands', 6.00),

-- Bandages
('Bandages', 'Medical Consumables', 'HealFast', 15.00),
('Bandages', 'Medical Consumables', 'QuickHeal', 18.00),

-- Injectables
('Injectables', 'Pharmaceutical', 'PharmaCorp', 120.00),
('Injectables', 'Pharmaceutical', 'Cipla', 115.00),
('Injectables', 'Pharmaceutical', 'Sun Pharma', 118.00);
  