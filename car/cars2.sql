
CREATE TABLE Cars (
    car_id INT PRIMARY KEY,
    make VARCHAR(255),
    model VARCHAR(255),
    year INT,
    current_mileage INT
);


INSERT INTO Cars (car_id, make, model, year, current_mileage)
VALUES (1, 'Toyota', 'Camry', 2020, 0),
       (2, 'Honda', 'Civic', 2018, 10),
       (3, 'Ford', 'Mustang', 2015, 20);


CREATE TABLE Drives (
    drive_id INT PRIMARY KEY,
    car_id INT,
    start_mileage INT,
    end_mileage INT,
    drive_date DATE,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id)
);


INSERT INTO Drives (drive_id, car_id, start_mileage, end_mileage, drive_date)
VALUES (1, 1, 0, 50, '2022-01-01'),
       (2, 2, 10, 60, '2022-01-02'),
       (3, 3, 20, 70, '2022-01-03');


CREATE VIEW CarDrives AS
SELECT car_id, SUM(end_mileage - start_mileage) as distance_driven
FROM Drives
GROUP BY car_id;

SELECT Cars.make, Cars.model, CarDrives.distance_driven
FROM Cars
JOIN CarDrives ON Cars.car_id = CarDrives.car_id;
