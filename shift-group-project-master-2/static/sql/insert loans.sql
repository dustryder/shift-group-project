USE devices;
INSERT INTO deviceloan (device_id, employee_id)
SELECT device_id, employee_id
FROM device JOIN employee ON device.status = employee.first_name;