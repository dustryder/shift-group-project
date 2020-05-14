CREATE VIEW DeviceHistory as
SELECT device.device_id, device_name, first_name, loan_start, loan_end, returned_date
FROM device JOIN deviceloan ON device.device_id = deviceloan.device_id
JOIN employee ON deviceloan.employee_id = employee.employee_id;

CREATE VIEW DeviceTable as
SELECT device.device_id, employee.employee_id, loan_start, device_name, first_name, device_type, os_type, os_version, grade, IFNULL(Location, 'DeviceVault') AS Location
FROM device
LEFT OUTER JOIN (SELECT * FROM deviceloan WHERE returned_date is NULL) as deviceloan ON device.device_id = deviceloan.device_id 
LEFT OUTER JOIN employee ON employee.employee_id = deviceloan.employee_id
ORDER BY Location DESC;

CREATE VIEW DeviceInfo as
SELECT device.device_id, device_name, device_type, os_type, os_version, ram, device_cpu, device_bit, resolution, grade, uuid, acquisition_date, loan_end
FROM device
LEFT OUTER JOIN (SELECT * FROM deviceloan WHERE returned_date is NULL) as deviceloan ON device.device_id = deviceloan.device_id;