CREATE DATABASE IF NOT EXISTS restaurant_bot;

USE restaurant_bot;


-- Restaurant details table
CREATE TABLE IF NOT EXISTS restaurants(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    location VARCHAR(100),
    cuisine VARCHAR(50),
    rating FLOAT,
    opening_time VARCHAR(50),
    menu TEXT,
    parking VARCHAR(20)
);


INSERT INTO restaurants
(name, location, cuisine, rating, opening_time, menu, parking)
VALUES

('Spice Garden',
'Madurai',
'South Indian',
4.5,
'9 AM - 10 PM',
'Idly, Dosa, Biryani, Meals',
'Available'),

('Food Palace',
'Madurai',
'Chinese',
4.3,
'10 AM - 11 PM',
'Noodles, Fried Rice, Manchurian',
'Available'),

('Pizza World',
'Chennai',
'Italian',
4.6,
'11 AM - 12 AM',
'Pizza, Pasta, Garlic Bread',
'Available');



-- Restaurant tables availability
CREATE TABLE IF NOT EXISTS restaurant_tables(
    id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    capacity INT,
    status VARCHAR(20)
);


INSERT INTO restaurant_tables
(restaurant_id, capacity, status)
VALUES
(1, 4, 'Available'),
(2, 2, 'Available'),
(3, 6, 'Available');



-- Customer bookings
CREATE TABLE IF NOT EXISTS bookings(
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_code VARCHAR(20) UNIQUE,
    restaurant VARCHAR(100),
    booking_date VARCHAR(30),
    time VARCHAR(30),
    guests INT,
    status VARCHAR(30)
);