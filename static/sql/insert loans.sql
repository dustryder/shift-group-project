USE devices;
INSERT INTO deviceloan (device_id, employee_id, loan_start, loan_end, returned_date) VALUES
(3,1,'2020-05-10', '2020-06-10', NULL),
(6,1,'2020-01-01', '2020-03-01', '2020-02-02'),
(1,1,'2020-01-01', '2020-02-02', '2020-01-03'), 
(13,1,'2020-05-03', '2020-06-03', NULL),
(26,1,'2020-04-09', '2020-04-11', NULL),
(1,2,'2020-05-02', '2020-05-09', NULL), 
(46,3,'2020-03-26', '2020-05-26', '2020-04-01'),
(47,3,'2020-04-19', '2020-04-26', '2020-04-21')
