CREATE VIEW DeviceStatus AS
SELECT device.device_id, device_name, device_type, os_type, os_version, grade, first_name, location
FROM device 
LEFT JOIN deviceloan on device.device_id = deviceloan.device_id
LEFT JOIN employee on employee.employee_id = deviceloan.employee_id;