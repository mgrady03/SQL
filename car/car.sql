
CREATE TABLE Cars (
    car_id INT PRIMARY KEY,
    make VARCHAR(255),
    model VARCHAR(255),
    year INT,
    current_mileage INT
);


INSERT INTO Cars (car_id, make, model, year, current_mileage)
VALUES (1, 'Toyota', 'Camry', 2020, 0);


UPDATE Cars
SET current_mileage = current_mileage + 50
WHERE car_id = 1;


SELECT current_mileage
FROM Cars
WHERE car_id = 1;
