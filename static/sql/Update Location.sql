SELECT IFNULL(Location, "DeviceVault") AS Location
FROM Device
LEFT JOIN deviceloan on device.device_id = deviceloan.device_id
LEFT JOIN employee on employee.employee_id = deviceloan.employee_id;